import torch
import time
from testing.evaluator import Evaluator

class Trainer:
    def __init__(self, model, train_loader, test_loader, optimizer, device):
        """Initialize trainer.
        
        Args:
            model: Model to train
            train_loader: Training data loader
            test_loader: Test data loader
            optimizer: Optimizer for training
            device: Device to train on
        """
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.device = device
        self.evaluator = Evaluator(model, test_loader, device)
        
    def train_epoch(self, epoch):
        """Train for one epoch.
        
        Args:
            epoch: Current epoch number
            
        Returns:
            dict: Dictionary containing training metrics
        """
        self.model.train()
        
        total_loss = 0
        total_recon_loss = 0
        total_quant_loss = 0
        start_time = time.time()
        
        for batch_idx, batch in enumerate(self.train_loader):
            # CIFAR10 returns (images, labels), we only need images
            if isinstance(batch, (list, tuple)):
                batch = batch[0]
            batch = batch.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            output = self.model(batch)
            
            # Backward pass
            output['loss'].backward()
            # Gradient clipping to prevent explosion
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            # Accumulate losses
            total_loss += output['loss'].item()
            total_recon_loss += output['recon_loss'].item()
            total_quant_loss += output['quant_loss'].item()
            
            if (batch_idx + 1) % 100 == 0:
                print(f'Epoch {epoch} [{batch_idx+1}/{len(self.train_loader)}] '
                      f'Loss: {output["loss"].item():.4f} '
                      f'Recon: {output["recon_loss"].item():.4f} '
                      f'Quant: {output["quant_loss"].item():.4f}')
        
        avg_loss = total_loss / len(self.train_loader)
        avg_recon_loss = total_recon_loss / len(self.train_loader)
        avg_quant_loss = total_quant_loss / len(self.train_loader)
        epoch_time = time.time() - start_time
        
        return {
            'loss': avg_loss,
            'recon_loss': avg_recon_loss,
            'quant_loss': avg_quant_loss,
            'time': epoch_time
        }
    
    def train(self, num_epochs=2):
        """Train for specified number of epochs.
        
        Args:
            num_epochs: Number of epochs to train for
            
        Returns:
            dict: Dictionary containing training history
        """
        history = {
            'train_loss': [],
            'train_recon_loss': [],
            'train_quant_loss': [],
            'test_loss': [],
            'test_recon_loss': [],
            'test_quant_loss': [],
            'fid': []
        }
        
        for epoch in range(num_epochs):
            print(f'\nEpoch {epoch+1}/{num_epochs}')
            
            # Train for one epoch
            train_metrics = self.train_epoch(epoch)
            
            # Evaluate on test set
            test_metrics = self.evaluator.evaluate()
            
            # Store metrics
            history['train_loss'].append(train_metrics['loss'])
            history['train_recon_loss'].append(train_metrics['recon_loss'])
            history['train_quant_loss'].append(train_metrics['quant_loss'])
            history['test_loss'].append(test_metrics['loss'])
            history['test_recon_loss'].append(test_metrics['recon_loss'])
            history['test_quant_loss'].append(test_metrics['quant_loss'])
            history['fid'].append(test_metrics['fid'])
            
            print(f'Train Loss: {train_metrics["loss"]:.4f} '
                  f'Test Loss: {test_metrics["loss"]:.4f} '
                  f'FID: {test_metrics["fid"]:.4f} '
                  f'Time: {train_metrics["time"]:.2f}s')
            
        return history