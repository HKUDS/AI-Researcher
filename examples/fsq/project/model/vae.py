import torch
import torch.nn as nn
import torch.nn.functional as F
from .quantization import FiniteScalarQuantization

class Encoder(nn.Module):
    def __init__(self, in_channels=3, latent_dim=64, hidden_dim=64):
        """Encoder network for VAE.
        
        Args:
            in_channels (int): Number of input channels
            latent_dim (int): Dimension of latent space
            hidden_dim (int): Number of hidden channels
        """
        super().__init__()
        
        self.conv1 = nn.Conv2d(in_channels, hidden_dim, 4, stride=2, padding=1)
        self.conv2 = nn.Conv2d(hidden_dim, hidden_dim, 4, stride=2, padding=1)
        self.conv3 = nn.Conv2d(hidden_dim, hidden_dim, 4, stride=2, padding=1)
        self.conv4 = nn.Conv2d(hidden_dim, hidden_dim, 4, stride=2, padding=1)
        
        # Project to latent dimension
        self.fc = nn.Linear(hidden_dim * 4, latent_dim)
        
    def forward(self, x):
        """Forward pass of encoder.
        
        Args:
            x (torch.Tensor): Input tensor [B, C, H, W]
        Returns:
            torch.Tensor: Encoded representation
        """
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        
        # Flatten spatial dimensions
        x = x.view(x.size(0), -1)
        
        # Project to latent space - use tanh to bound output for stable quantization
        z = torch.tanh(self.fc(x)) * 5  # Scale to [-5, 5] to match quantization range
        return z

class Decoder(nn.Module):
    def __init__(self, out_channels=3, latent_dim=64, hidden_dim=64):
        """Decoder network for VAE.
        
        Args:
            out_channels (int): Number of output channels
            latent_dim (int): Dimension of latent space
            hidden_dim (int): Number of hidden channels
        """
        super().__init__()
        
        self.fc = nn.Linear(latent_dim, hidden_dim * 4)
        
        self.deconv1 = nn.ConvTranspose2d(hidden_dim, hidden_dim, 4, stride=2, padding=1)
        self.deconv2 = nn.ConvTranspose2d(hidden_dim, hidden_dim, 4, stride=2, padding=1)
        self.deconv3 = nn.ConvTranspose2d(hidden_dim, hidden_dim, 4, stride=2, padding=1)
        self.deconv4 = nn.ConvTranspose2d(hidden_dim, out_channels, 4, stride=2, padding=1)
        
    def forward(self, z):
        """Forward pass of decoder.
        
        Args:
            z (torch.Tensor): Latent vector [B, D]
        Returns:
            torch.Tensor: Reconstructed image
        """
        # Project and reshape
        x = self.fc(z)
        x = x.view(x.size(0), -1, 2, 2)
        
        # Deconvolution layers
        x = F.relu(self.deconv1(x))
        x = F.relu(self.deconv2(x))
        x = F.relu(self.deconv3(x))
        x = torch.sigmoid(self.deconv4(x))
        
        return x

class FiniteScalarQuantizedVAE(nn.Module):
    def __init__(self, in_channels=3, latent_dim=64, hidden_dim=64, num_levels=10):
        """VAE with Finite Scalar Quantization.
        
        Args:
            in_channels (int): Number of input channels
            latent_dim (int): Dimension of latent space
            hidden_dim (int): Number of hidden channels
            num_levels (int): Number of quantization levels
        """
        super().__init__()
        
        self.encoder = Encoder(in_channels, latent_dim, hidden_dim)
        self.quantizer = FiniteScalarQuantization(num_levels, latent_dim)
        self.decoder = Decoder(in_channels, latent_dim, hidden_dim)
        
    def forward(self, x):
        """Forward pass combining encoder, quantizer and decoder.
        
        Args:
            x (torch.Tensor): Input image [B, C, H, W]
        Returns:
            Dict: Contains reconstructed image and losses
        """
        # Encode
        z = self.encoder(x)
        
        # Quantize
        quantized_z, quant_loss = self.quantizer(z)
        
        # Decode
        recon_x = self.decoder(quantized_z)
        
        # Calculate reconstruction loss
        recon_loss = F.binary_cross_entropy(recon_x, x, reduction='sum')
        
        # Total loss is reconstruction + quantization loss
        loss = recon_loss + quant_loss
        
        return {
            'recon_x': recon_x,
            'loss': loss,
            'recon_loss': recon_loss,
            'quant_loss': quant_loss
        }