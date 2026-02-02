"""
Script for training a nanopore basecaller model.
"""

import argparse
import numpy as np
import torch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nanopore_basecaller.model import NanoporeBasecaller
from nanopore_basecaller.data_processor import SignalProcessor, NanoporeDataset
from nanopore_basecaller.trainer import Trainer
from utils.helpers import plot_training_history


def load_data(data_dir):
    """
    Load training data from directory.
    Replace this with your actual data loading logic.
    """
    # This is a placeholder - implement based on your data format
    print(f"Loading data from {data_dir}...")
    raise NotImplementedError(
        "Please implement data loading for your specific format.\n"
        "See examples/basic_usage.py for synthetic data generation."
    )


def main():
    parser = argparse.ArgumentParser(description='Train Nanopore Basecaller')
    parser.add_argument('--data-dir', type=str, help='Directory containing training data')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--lr', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--hidden-size', type=int, default=256, help='Hidden layer size')
    parser.add_argument('--num-layers', type=int, default=3, help='Number of LSTM layers')
    parser.add_argument('--save-dir', type=str, default='models', help='Directory to save models')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Training Nanopore Basecaller")
    print("=" * 60)
    
    # Load data (implement this based on your data format)
    if args.data_dir:
        train_signals, train_sequences, val_signals, val_sequences = load_data(args.data_dir)
    else:
        print("\nNo data directory provided. Use --data-dir to specify training data.")
        print("For a quick example with synthetic data, run: python examples/basic_usage.py")
        return
    
    # Create datasets
    processor = SignalProcessor(normalize=True, filter_signal=True)
    train_dataset = NanoporeDataset(train_signals, train_sequences, processor)
    val_dataset = NanoporeDataset(val_signals, val_sequences, processor)
    
    print(f"\nDataset sizes:")
    print(f"  Training: {len(train_dataset)}")
    print(f"  Validation: {len(val_dataset)}")
    
    # Create model
    model = NanoporeBasecaller(
        input_size=1,
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        num_classes=5,
        dropout=0.1
    )
    
    print(f"\nModel parameters:")
    print(f"  Hidden size: {args.hidden_size}")
    print(f"  Num layers: {args.num_layers}")
    print(f"  Total params: {sum(p.numel() for p in model.parameters()):,}")
    
    # Create trainer
    trainer = Trainer(
        model=model,
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        batch_size=args.batch_size,
        learning_rate=args.lr
    )
    
    print(f"\nTraining configuration:")
    print(f"  Device: {trainer.device}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Epochs: {args.epochs}")
    
    # Train
    print("\nStarting training...")
    trainer.train(num_epochs=args.epochs, save_dir=args.save_dir)
    
    # Plot history
    print("\nSaving training history plot...")
    plot_training_history(trainer.history, save_path=f'{args.save_dir}/training_history.png')
    
    print("\nTraining completed!")
    print(f"Models saved in: {args.save_dir}")


if __name__ == "__main__":
    main()
