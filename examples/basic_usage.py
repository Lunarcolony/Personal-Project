"""
Example script demonstrating how to use the nanopore basecaller.
This script shows how to:
1. Generate synthetic data
2. Create and train a model
3. Make predictions
"""

import numpy as np
import torch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nanopore_basecaller.model import NanoporeBasecaller
from nanopore_basecaller.data_processor import SignalProcessor, NanoporeDataset
from nanopore_basecaller.trainer import Trainer
from nanopore_basecaller.inference import predict_sequence
from utils.helpers import generate_synthetic_signal, plot_signal, calculate_accuracy


def main():
    print("=" * 60)
    print("Nanopore Signal to DNA Sequence Basecaller - Example")
    print("=" * 60)
    
    # Generate synthetic training data
    print("\n1. Generating synthetic training data...")
    sequences = [
        "ACGTACGTACGT",
        "GGTTAACCGGTT",
        "ATATATATATAT",
        "CCCCGGGGAAAA",
        "TACGTACGTACG",
    ]
    
    signals = []
    for seq in sequences:
        signal = generate_synthetic_signal(seq, signal_length_per_base=50, noise_level=0.1)
        signals.append(signal)
    
    print(f"   Generated {len(signals)} training signals")
    print(f"   Example sequence: {sequences[0]}")
    print(f"   Signal length: {len(signals[0])} samples")
    
    # Create datasets
    print("\n2. Creating datasets...")
    processor = SignalProcessor(normalize=True, filter_signal=True)
    train_dataset = NanoporeDataset(signals[:4], sequences[:4], processor)
    val_dataset = NanoporeDataset(signals[4:], sequences[4:], processor)
    
    print(f"   Training samples: {len(train_dataset)}")
    print(f"   Validation samples: {len(val_dataset)}")
    
    # Create model
    print("\n3. Creating model...")
    model = NanoporeBasecaller(
        input_size=1,
        hidden_size=128,
        num_layers=2,
        num_classes=5,
        dropout=0.1
    )
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   Model created with {total_params:,} parameters")
    
    # Create trainer
    print("\n4. Setting up trainer...")
    trainer = Trainer(
        model=model,
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        batch_size=2,
        learning_rate=1e-3
    )
    print(f"   Training on device: {trainer.device}")
    
    # Train model
    print("\n5. Training model...")
    print("   (This is a quick demo with few epochs)")
    trainer.train(num_epochs=5, save_dir='models')
    
    # Make predictions
    print("\n6. Making predictions...")
    test_sequence = "ACGTACGT"
    test_signal = generate_synthetic_signal(test_sequence, noise_level=0.05)
    
    predicted_seq = predict_sequence(model, test_signal, processor)
    
    print(f"\n   Original sequence:  {test_sequence}")
    print(f"   Predicted sequence: {predicted_seq}")
    
    accuracy = calculate_accuracy(predicted_seq, test_sequence)
    print(f"   Accuracy: {accuracy:.2%}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    print("\nNote: This is a demonstration with synthetic data.")
    print("For real nanopore data, you would need:")
    print("  - Actual nanopore signal files (e.g., FAST5 format)")
    print("  - Corresponding reference sequences")
    print("  - More training data and epochs")
    print("  - Hyperparameter tuning")


if __name__ == "__main__":
    main()
