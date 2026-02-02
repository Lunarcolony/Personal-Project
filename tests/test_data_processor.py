"""
Tests for data processing functionality.
"""

import unittest
import numpy as np
import torch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nanopore_basecaller.data_processor import SignalProcessor, NanoporeDataset


class TestSignalProcessor(unittest.TestCase):
    """Test signal processing functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = SignalProcessor(normalize=True, filter_signal=True)
    
    def test_process_signal(self):
        """Test basic signal processing."""
        signal = np.random.randn(1000)
        processed = self.processor.process(signal)
        
        self.assertEqual(len(processed), len(signal))
        self.assertIsInstance(processed, np.ndarray)
    
    def test_normalization(self):
        """Test that normalization works correctly."""
        signal = np.random.randn(1000) * 10 + 5
        processed = self.processor.process(signal)
        
        # Check that mean is close to 0 and std close to 1
        self.assertAlmostEqual(np.mean(processed), 0.0, places=1)
        self.assertAlmostEqual(np.std(processed), 1.0, places=1)
    
    def test_filter_signal(self):
        """Test signal filtering."""
        processor_filtered = SignalProcessor(normalize=False, filter_signal=True)
        processor_unfiltered = SignalProcessor(normalize=False, filter_signal=False)
        
        signal = np.random.randn(1000)
        
        filtered = processor_filtered.process(signal)
        unfiltered = processor_unfiltered.process(signal)
        
        # Filtered and unfiltered should be different
        self.assertFalse(np.allclose(filtered, unfiltered))


class TestNanoporeDataset(unittest.TestCase):
    """Test dataset functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.signals = [np.random.randn(100) for _ in range(5)]
        self.sequences = ['ACGT', 'GGTA', 'CCAA', 'TATA', 'GCGC']
        self.dataset = NanoporeDataset(self.signals, self.sequences)
    
    def test_dataset_length(self):
        """Test dataset length."""
        self.assertEqual(len(self.dataset), 5)
    
    def test_dataset_getitem(self):
        """Test getting items from dataset."""
        item = self.dataset[0]
        
        self.assertIn('signal', item)
        self.assertIn('sequence', item)
        self.assertIn('seq_length', item)
        
        self.assertIsInstance(item['signal'], torch.Tensor)
        self.assertIsInstance(item['sequence'], torch.Tensor)
    
    def test_base_encoding(self):
        """Test base to index encoding."""
        self.assertEqual(self.dataset.base_to_idx['A'], 0)
        self.assertEqual(self.dataset.base_to_idx['C'], 1)
        self.assertEqual(self.dataset.base_to_idx['G'], 2)
        self.assertEqual(self.dataset.base_to_idx['T'], 3)
    
    def test_sequence_decoding(self):
        """Test sequence decoding."""
        # Encode and decode
        encoded = [0, 1, 2, 3]  # A, C, G, T
        decoded = self.dataset.decode_sequence(encoded)
        
        self.assertEqual(decoded, 'ACGT')
    
    def test_ctc_decoding(self):
        """Test CTC decoding (removing blanks and duplicates)."""
        # Test with blanks (4) and duplicates
        encoded = [0, 0, 4, 1, 1, 4, 2, 4, 3, 3, 3]
        decoded = self.dataset.decode_sequence(encoded)
        
        # Should collapse duplicates and remove blanks
        self.assertEqual(decoded, 'ACGT')


if __name__ == '__main__':
    unittest.main()
