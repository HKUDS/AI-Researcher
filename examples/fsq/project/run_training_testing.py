import torch
import torch.optim as optim
from model.vae import FiniteScalarQuantizedVAE
from data_processing.dataset import get_data_loaders
from training.trainer import Trainer
import json

def main():
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Set hyperparameters
    config = {
        'batch_size': 64,  # Reduced batch size
        'num_workers': 4,
        'latent_dim': 64,
        'hidden_dim': 64,
        'num_levels': 10,
        'learning_rate': 1e-3,
        'num_epochs': 5  # Quick demo - increase to 50 for full training
    }

    # Create data loaders
    print("Loading CIFAR-10 dataset...")
    train_loader, test_loader = get_data_loaders(
        data_dir='data',
        batch_size=config['batch_size'],
        num_workers=config['num_workers']
    )

    # Initialize model
    print("Initializing model...")
    model = FiniteScalarQuantizedVAE(
        latent_dim=config['latent_dim'],
        hidden_dim=config['hidden_dim'],
        num_levels=config['num_levels']
    ).to(device)

    # Initialize optimizer
    optimizer = optim.Adam(model.parameters(), lr=config['learning_rate'])

    # Initialize trainer
    trainer = Trainer(model, train_loader, test_loader, optimizer, device)

    # Train model
    print("Starting training...")
    history = trainer.train(num_epochs=config['num_epochs'])

    # Save training history
    with open('training_history.json', 'w') as f:
        json.dump({k: [float(v) for v in vals] for k, vals in history.items()}, f)
    print("Training history saved to training_history.json")

    # Save model
    torch.save(model.state_dict(), 'model.pt')
    print("Model saved to model.pt")

    # Final evaluation
    print("\nFinal Evaluation:")
    final_metrics = trainer.evaluator.evaluate(num_samples=200)  # Reduced for quick demo
    print(f"Test Loss: {final_metrics['loss']:.4f}")
    print(f"FID Score: {final_metrics['fid']:.4f}")

if __name__ == '__main__':
    main()