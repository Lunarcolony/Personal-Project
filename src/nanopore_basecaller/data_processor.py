"""
Data processing utilities for nanopore signals.
"""

import numpy as np
import torch
from torch.utils.data import Dataset
from scipy import signal


class SignalProcessor:
    """
    Process raw nanopore signals for input to the neural network.
    """
    
    def __init__(self, normalize=True, filter_signal=True):
        """
        Initialize signal processor.
        
        Args:
            normalize (bool): Whether to normalize signals
            filter_signal (bool): Whether to apply filtering
        """
        self.normalize = normalize
        self.filter_signal = filter_signal
        
    def process(self, raw_signal):
        """
        Process a raw nanopore signal.
        
        Args:
            raw_signal (np.ndarray): Raw signal values
            
        Returns:
            np.ndarray: Processed signal
        """
        signal_data = raw_signal.copy()
        
        # Apply filtering to reduce noise
        if self.filter_signal:
            signal_data = self._apply_filter(signal_data)
        
        # Normalize signal
        if self.normalize:
            signal_data = self._normalize(signal_data)
            
        return signal_data
    
    def _apply_filter(self, signal_data, cutoff=0.1):
        """
        Apply low-pass filter to reduce high-frequency noise.
        
        Args:
            signal_data (np.ndarray): Input signal
            cutoff (float): Cutoff frequency
            
        Returns:
            np.ndarray: Filtered signal
        """
        # Design a Butterworth low-pass filter
        b, a = signal.butter(4, cutoff, btype='low')
        filtered = signal.filtfilt(b, a, signal_data)
        return filtered
    
    def _normalize(self, signal_data):
        """
        Normalize signal to zero mean and unit variance.
        
        Args:
            signal_data (np.ndarray): Input signal
            
        Returns:
            np.ndarray: Normalized signal
        """
        mean = np.mean(signal_data)
        std = np.std(signal_data)
        if std > 0:
            normalized = (signal_data - mean) / std
        else:
            normalized = signal_data - mean
        return normalized


class NanoporeDataset(Dataset):
    """
    PyTorch Dataset for nanopore signals and DNA sequences.
    """
    
    def __init__(self, signals, sequences=None, processor=None):
        """
        Initialize dataset.
        
        Args:
            signals (list): List of signal arrays
            sequences (list): List of DNA sequences (optional, for training)
            processor (SignalProcessor): Signal processor instance
        """
        self.signals = signals
        self.sequences = sequences
        self.processor = processor if processor else SignalProcessor()
        
        # Base to index mapping
        self.base_to_idx = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'blank': 4}
        self.idx_to_base = {v: k for k, v in self.base_to_idx.items()}
        
    def __len__(self):
        return len(self.signals)
    
    def __getitem__(self, idx):
        """
        Get a single data sample.
        
        Args:
            idx (int): Index
            
        Returns:
            dict: Dictionary containing signal and optionally sequence
        """
        # Process signal
        signal_data = self.processor.process(self.signals[idx])
        signal_tensor = torch.FloatTensor(signal_data).unsqueeze(-1)  # Add feature dim
        
        item = {'signal': signal_tensor}
        
        # Add sequence if available (for training)
        if self.sequences is not None:
            sequence = self.sequences[idx]
            seq_encoded = [self.base_to_idx[base] for base in sequence if base in self.base_to_idx]
            item['sequence'] = torch.LongTensor(seq_encoded)
            item['seq_length'] = len(seq_encoded)
            
        return item
    
    def decode_sequence(self, indices):
        """
        Decode sequence indices back to DNA bases.
        
        Args:
            indices (list or torch.Tensor): Sequence indices
            
        Returns:
            str: DNA sequence
        """
        if isinstance(indices, torch.Tensor):
            indices = indices.cpu().numpy()
        
        # Remove blanks and consecutive duplicates (CTC decoding)
        decoded = []
        prev_idx = None
        for idx in indices:
            if idx != 4 and idx != prev_idx:  # 4 is blank
                decoded.append(self.idx_to_base[int(idx)])
            prev_idx = idx
            
        return ''.join(decoded)


def collate_fn(batch):
    """
    Custom collate function for variable length sequences.
    
    Args:
        batch (list): List of samples
        
    Returns:
        dict: Batched data
    """
    signals = [item['signal'] for item in batch]
    
    # Pad signals to same length
    max_len = max(s.size(0) for s in signals)
    padded_signals = torch.zeros(len(signals), max_len, signals[0].size(1))
    signal_lengths = []
    
    for i, sig in enumerate(signals):
        length = sig.size(0)
        padded_signals[i, :length, :] = sig
        signal_lengths.append(length)
    
    result = {
        'signal': padded_signals,
        'signal_lengths': torch.LongTensor(signal_lengths)
    }
    
    # Add sequences if present
    if 'sequence' in batch[0]:
        sequences = [item['sequence'] for item in batch]
        seq_lengths = [item['seq_length'] for item in batch]
        
        result['sequences'] = sequences  # Keep as list for CTC loss
        result['seq_lengths'] = torch.LongTensor(seq_lengths)
    
    return result
