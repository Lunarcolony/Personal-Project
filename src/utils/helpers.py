"""
Utility functions for nanopore basecalling.
"""

import numpy as np
import matplotlib.pyplot as plt


def generate_synthetic_signal(sequence, signal_length_per_base=50, noise_level=0.1):
    """
    Generate a synthetic nanopore signal from a DNA sequence.
    Useful for testing and demonstration.
    
    Args:
        sequence (str): DNA sequence (A, C, G, T)
        signal_length_per_base (int): Number of signal points per base
        noise_level (float): Amount of noise to add
        
    Returns:
        np.ndarray: Synthetic signal
    """
    # Base-specific signal levels (simplified model)
    base_signals = {
        'A': 0.5,
        'C': 0.8,
        'G': 0.3,
        'T': 0.6
    }
    
    signal = []
    for base in sequence:
        if base in base_signals:
            level = base_signals[base]
            # Create signal segment for this base
            segment = np.ones(signal_length_per_base) * level
            # Add noise
            segment += np.random.normal(0, noise_level, signal_length_per_base)
            signal.extend(segment)
    
    return np.array(signal)


def plot_signal(signal, title="Nanopore Signal", save_path=None):
    """
    Plot a nanopore signal.
    
    Args:
        signal (np.ndarray): Signal to plot
        title (str): Plot title
        save_path (str): Path to save plot (optional)
    """
    plt.figure(figsize=(12, 4))
    plt.plot(signal)
    plt.title(title)
    plt.xlabel('Time (samples)')
    plt.ylabel('Signal Amplitude')
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def plot_training_history(history, save_path=None):
    """
    Plot training history.
    
    Args:
        history (dict): Training history with 'train_loss' and 'val_loss'
        save_path (str): Path to save plot (optional)
    """
    plt.figure(figsize=(10, 6))
    
    epochs = range(1, len(history['train_loss']) + 1)
    plt.plot(epochs, history['train_loss'], 'b-', label='Training Loss')
    
    if 'val_loss' in history and history['val_loss']:
        plt.plot(epochs, history['val_loss'], 'r-', label='Validation Loss')
    
    plt.title('Training History')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def calculate_accuracy(predicted, actual):
    """
    Calculate base-level accuracy between predicted and actual sequences.
    
    Args:
        predicted (str): Predicted DNA sequence
        actual (str): Actual DNA sequence
        
    Returns:
        float: Accuracy (0-1)
    """
    min_len = min(len(predicted), len(actual))
    if min_len == 0:
        return 0.0
    
    matches = sum(1 for i in range(min_len) if predicted[i] == actual[i])
    accuracy = matches / max(len(predicted), len(actual))
    
    return accuracy


def edit_distance(s1, s2):
    """
    Calculate Levenshtein edit distance between two sequences.
    
    Args:
        s1 (str): First sequence
        s2 (str): Second sequence
        
    Returns:
        int: Edit distance
    """
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer than s2
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
