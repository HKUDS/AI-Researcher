import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class FiniteScalarQuantization(nn.Module):
    def __init__(self, num_levels=10, embedding_dim=64):
        """Initialize Finite Scalar Quantization module.

        Args:
            num_levels (int): Number of quantization levels
            embedding_dim (int): Dimension of embeddings
        """
        super().__init__()
        self.num_levels = num_levels
        self.embedding_dim = embedding_dim

        # Initialize codebook
        self.codebook = nn.Parameter(
            torch.randn(num_levels, embedding_dim) * 0.1  # Reduced initialization scale
        )

        # Bounding levels for tanh projection
        self.bound_levels = int(num_levels / 2)

        # Initialize EMA registers
        self.register_buffer('N', torch.zeros(num_levels))
        self.register_buffer('m', torch.zeros(num_levels, embedding_dim))
        self.gamma = 0.99  # EMA decay rate
        
        # Temperature parameter for annealing
        self.register_buffer('temperature', torch.tensor(1.0))

        # Track utilization
        self.register_buffer('usage_count', torch.zeros(num_levels))

    def bounding_function(self, z):
        """Project encoder output to bounded range using temperature-scaled tanh.

        Args:
            z (torch.Tensor): Encoder output tensor
        Returns:
            torch.Tensor: Bounded representation
        """
        return self.bound_levels * torch.tanh(z / self.temperature)
        
    def set_temperature(self, temp):
        """Set temperature value for annealing.

        Args:
            temp (float): New temperature value
        """
        self.temperature.fill_(temp)

    def quantize(self, z):
        """Quantize input using scalar quantization with STE.

        Args:
            z (torch.Tensor): Input tensor to quantize
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Quantized representation and assignments
        """
        # Apply bounding function
        bounded_z = self.bounding_function(z)

        # Round to nearest integer levels with temperature scaling
        quantized_z = torch.round(bounded_z) * self.temperature

        # Get cluster assignments for EMA updates
        distances = torch.cdist(quantized_z.view(-1, self.embedding_dim), self.codebook)
        assignments = torch.argmin(distances, dim=1)

        # Update usage statistics
        if self.training:
            for k in range(self.num_levels):
                self.usage_count[k] += (assignments == k).sum().item()

        # Straight-Through Estimator: Forward = round, Backward = identity
        quantized_z = z + (quantized_z - z).detach()

        return quantized_z, assignments

    def update_codebook(self, z, assignments):
        """Update codebook using Exponential Moving Average.

        Args:
            z (torch.Tensor): Original input tensor
            assignments (torch.Tensor): Cluster assignments
        """
        if self.training:
            with torch.no_grad():
                for k in range(self.num_levels):
                    mask = (assignments == k)
                    cluster_size = mask.sum().item()

                    if cluster_size > 0:
                        # Update cluster size
                        self.N[k] = self.gamma * self.N[k] + (1 - self.gamma) * cluster_size

                        # Update cluster mean
                        cluster_sum = z[mask].sum(dim=0)
                        self.m[k] = self.gamma * self.m[k] + (1 - self.gamma) * cluster_sum

                        # Update codebook with scaled updates
                        self.codebook[k] = self.m[k] / (self.N[k].clamp(min=1e-6))

    def get_codebook_utilization(self):
        """Calculate codebook utilization.

        Returns:
            float: Percentage of codebook entries being used
        """
        total_usage = self.usage_count.sum()
        if total_usage > 0:
            probs = self.usage_count / total_usage
            entropy = -(probs * torch.log2(probs + 1e-10)).sum()
            normalized_entropy = entropy / np.log2(self.num_levels)
            return normalized_entropy.item()
        return 0.0

    def get_active_levels(self):
        """Get number of active quantization levels.

        Returns:
            int: Number of active levels
        """
        return (self.usage_count > 0).sum().item()

    def compute_entropy_rate(self):
        """Compute entropy rate of quantized representations.

        Returns:
            float: Entropy rate in bits
        """
        total_usage = self.usage_count.sum()
        if total_usage > 0:
            probs = self.usage_count / total_usage
            entropy = -(probs * torch.log2(probs + 1e-10)).sum()
            return entropy.item()
        return 0.0

    def forward(self, z):
        """Forward pass combining quantization and codebook update.

        Args:
            z (torch.Tensor): Input tensor
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Quantized output and loss components
        """
        # Quantize inputs
        quantized_z, assignments = self.quantize(z)

        # Update codebook with EMA
        if self.training:
            self.update_codebook(z, assignments)

        # Calculate losses - use mean reduction and scale to prevent explosion
        # Commitment: encourage encoder output to match quantized
        # Codebook: encourage quantized to match encoder (STE passes grad to encoder)
        commitment_loss = F.mse_loss(z, quantized_z.detach(), reduction='mean')
        codebook_loss = F.mse_loss(quantized_z, z.detach(), reduction='mean')
        
        # Scale down quantization losses to balance with reconstruction
        commitment_loss = commitment_loss * 0.25
        codebook_loss = codebook_loss * 0.25
        
        # Add entropy regularization (scalar, no grad)
        entropy_loss = -self.compute_entropy_rate() * 0.01
        
        total_loss = commitment_loss + codebook_loss + entropy_loss

        return quantized_z, total_loss