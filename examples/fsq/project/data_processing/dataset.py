import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import os


def get_data_loaders(data_dir, batch_size=128, num_workers=4):
    """Create data loaders for training and testing.
    
    Args:
        data_dir (str): Directory containing dataset (CIFAR-10 will be downloaded here if not present)
        batch_size (int): Batch size
        num_workers (int): Number of worker threads
        
    Returns:
        tuple: Training and test data loaders
    """
    transform = transforms.Compose([
        transforms.ToTensor(),  # Converts PIL to [0, 1] tensor, shape [C, H, W]
    ])
    # Use torchvision CIFAR10 which auto-downloads if not present
    train_dataset = datasets.CIFAR10(
        root=data_dir,
        train=True,
        download=True,
        transform=transform
    )
    test_dataset = datasets.CIFAR10(
        root=data_dir,
        train=False,
        download=True,
        transform=transform
    )
    
    # Create data loaders
    # Disable pin_memory when no GPU to avoid warning
    use_pin_memory = torch.cuda.is_available()
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=use_pin_memory
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=use_pin_memory
    )
    
    return train_loader, test_loader