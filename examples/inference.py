"""
Script for running inference with a trained model.
"""

import argparse
import numpy as np
import torch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nanopore_basecaller.model import NanoporeBasecaller
from nanopore_basecaller.inference import load_model, predict_sequence, batch_predict
from nanopore_basecaller.data_processor import SignalProcessor
from utils.helpers import plot_signal


def load_signal_from_file(file_path):
    """
    Load signal from file.
    Implement based on your data format (e.g., FAST5, NPY, etc.)
    """
    # Example for numpy format
    if file_path.endswith('.npy'):
        return np.load(file_path)
    else:
        raise NotImplementedError(
            f"File format not supported: {file_path}\n"
            "Implement loading for your specific format."
        )


def main():
    parser = argparse.ArgumentParser(description='Run inference with Nanopore Basecaller')
    parser.add_argument('--model', type=str, required=True, help='Path to trained model')
    parser.add_argument('--signal', type=str, help='Path to signal file')
    parser.add_argument('--signal-dir', type=str, help='Directory containing multiple signal files')
    parser.add_argument('--output', type=str, help='Output file for predictions')
    parser.add_argument('--plot', action='store_true', help='Plot the signal')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Nanopore Basecaller Inference")
    print("=" * 60)
    
    # Load model
    print(f"\nLoading model from {args.model}...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model = NanoporeBasecaller()
    checkpoint = torch.load(args.model, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    print(f"Model loaded successfully (device: {device})")
    
    # Create processor
    processor = SignalProcessor()
    
    # Single signal inference
    if args.signal:
        print(f"\nLoading signal from {args.signal}...")
        signal = load_signal_from_file(args.signal)
        print(f"Signal length: {len(signal)}")
        
        if args.plot:
            plot_signal(signal, title="Input Nanopore Signal")
        
        print("\nPredicting sequence...")
        sequence = predict_sequence(model, signal, processor, device)
        
        print(f"\nPredicted sequence ({len(sequence)} bases):")
        print(sequence)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(f">prediction\n{sequence}\n")
            print(f"\nSequence saved to: {args.output}")
    
    # Batch inference
    elif args.signal_dir:
        print(f"\nLoading signals from {args.signal_dir}...")
        
        # Load all signal files
        signal_files = [f for f in os.listdir(args.signal_dir) if f.endswith('.npy')]
        signals = [load_signal_from_file(os.path.join(args.signal_dir, f)) 
                   for f in signal_files]
        
        print(f"Loaded {len(signals)} signals")
        
        print("\nRunning batch prediction...")
        sequences = batch_predict(model, signals, processor, device)
        
        print(f"\nPredicted {len(sequences)} sequences")
        
        if args.output:
            with open(args.output, 'w') as f:
                for i, seq in enumerate(sequences):
                    f.write(f">prediction_{i}\n{seq}\n")
            print(f"Sequences saved to: {args.output}")
        else:
            for i, seq in enumerate(sequences[:5]):  # Show first 5
                print(f"  {signal_files[i]}: {seq[:50]}...")
    
    else:
        print("\nError: Please provide either --signal or --signal-dir")
        return
    
    print("\nInference completed!")


if __name__ == "__main__":
    main()
