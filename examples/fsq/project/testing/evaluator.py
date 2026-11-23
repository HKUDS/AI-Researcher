import torch
import numpy as np
from scipy import linalg
from torch.nn.functional import adaptive_avg_pool2d
from torchvision.models import inception_v3, Inception_V3_Weights
import torch.nn.functional as F

class InceptionScore:
    def __init__(self, device):
        """Initialize Inception Score calculator.
        
        Args:
            device: Device to run calculations on
        """
        self.device = device
        self.model = inception_v3(weights=Inception_V3_Weights.IMAGENET1K_V1, transform_input=False).to(device)
        self.model.eval()
        
    @torch.no_grad()
    def calculate_activation_statistics(self, images):
        """Calculate activation statistics for FID score.
        
        Args:
            images: Batch of images
        Returns:
            tuple: Mean and covariance of activations
        """
        self.model.eval()
        
        # Ensure images are properly sized for Inception
        if images.shape[2] != 299 or images.shape[3] != 299:
            images = F.interpolate(images, size=(299, 299), mode='bilinear', align_corners=True)
            
        # Get activations (logits from Inception - used for FID feature statistics)
        act = self.model(images)
        
        # Calculate statistics
        mu = torch.mean(act, dim=0).cpu().numpy()
        sigma = torch.cov(act.t()).cpu().numpy()
        
        return mu, sigma
        
    def calculate_fid(self, real_images, generated_images, eps=1e-6):
        """Calculate FID score between real and generated images.
        
        Args:
            real_images: Batch of real images
            generated_images: Batch of generated images
            eps: Small constant for numerical stability
            
        Returns:
            float: FID score
        """
        mu1, sigma1 = self.calculate_activation_statistics(real_images)
        mu2, sigma2 = self.calculate_activation_statistics(generated_images)
        
        # Calculate FID score
        mu1 = np.atleast_1d(mu1)
        mu2 = np.atleast_1d(mu2)
        
        sigma1 = np.atleast_2d(sigma1)
        sigma2 = np.atleast_2d(sigma2)
        
        diff = mu1 - mu2
        
        # Product might be almost singular
        sqrtm_result = linalg.sqrtm(sigma1.dot(sigma2))
        covmean = sqrtm_result[0] if isinstance(sqrtm_result, tuple) else sqrtm_result
        if not np.isfinite(covmean).all():
            offset = np.eye(sigma1.shape[0]) * eps
            sqrtm_result = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))
            covmean = sqrtm_result[0] if isinstance(sqrtm_result, tuple) else sqrtm_result
            
        # Numerical error might give slight imaginary component
        if np.iscomplexobj(covmean):
            covmean = covmean.real
            
        tr_covmean = np.trace(covmean)
        
        fid = diff.dot(diff) + np.trace(sigma1) + np.trace(sigma2) - 2 * tr_covmean
        
        return fid
        
class Evaluator:
    def __init__(self, model, test_loader, device):
        """Initialize evaluator.
        
        Args:
            model: Model to evaluate
            test_loader: Test data loader
            device: Device to run evaluation on
        """
        self.model = model
        self.test_loader = test_loader
        self.device = device
        self.inception_score = InceptionScore(device)
        
    @torch.no_grad()
    def evaluate(self, num_samples=1000):
        """Evaluate model performance.
        
        Args:
            num_samples: Number of samples for FID calculation
            
        Returns:
            dict: Dictionary containing evaluation metrics
        """
        self.model.eval()
        
        total_loss = 0
        total_recon_loss = 0
        total_quant_loss = 0
        
        real_images = []
        generated_images = []
        
        for batch in self.test_loader:
            # CIFAR10 returns (images, labels), we only need images
            if isinstance(batch, (list, tuple)):
                batch = batch[0]
            batch = batch.to(self.device)
            
            # Forward pass
            output = self.model(batch)
            
            # Accumulate losses
            total_loss += output['loss'].item()
            total_recon_loss += output['recon_loss'].item()
            total_quant_loss += output['quant_loss'].item()
            
            # Collect images for FID score
            real_images.append(batch)
            generated_images.append(output['recon_x'])
            
            if len(real_images) * batch.size(0) >= num_samples:
                break
                
        # Calculate average losses
        num_batches = len(real_images)
        avg_loss = total_loss / num_batches
        avg_recon_loss = total_recon_loss / num_batches
        avg_quant_loss = total_quant_loss / num_batches
        
        # Concatenate images for FID calculation
        real_images = torch.cat(real_images, dim=0)[:num_samples]
        generated_images = torch.cat(generated_images, dim=0)[:num_samples]
        
        # Calculate FID score
        fid_score = self.inception_score.calculate_fid(real_images, generated_images)
        
        return {
            'loss': avg_loss,
            'recon_loss': avg_recon_loss,
            'quant_loss': avg_quant_loss,
            'fid': fid_score
        }