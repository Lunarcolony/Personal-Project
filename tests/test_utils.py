"""
Tests for utility functions.
"""

import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.helpers import (
    generate_synthetic_signal,
    calculate_accuracy,
    edit_distance
)


class TestHelpers(unittest.TestCase):
    """Test helper functions."""
    
    def test_generate_synthetic_signal(self):
        """Test synthetic signal generation."""
        sequence = "ACGT"
        signal = generate_synthetic_signal(sequence, signal_length_per_base=50)
        
        # Should generate signal with correct length
        expected_length = len(sequence) * 50
        self.assertEqual(len(signal), expected_length)
        
        # Should be numpy array
        self.assertIsInstance(signal, np.ndarray)
    
    def test_calculate_accuracy(self):
        """Test accuracy calculation."""
        # Perfect match
        acc = calculate_accuracy("ACGT", "ACGT")
        self.assertEqual(acc, 1.0)
        
        # Partial match
        acc = calculate_accuracy("ACGT", "ACGG")
        self.assertGreater(acc, 0.5)
        self.assertLess(acc, 1.0)
        
        # No match
        acc = calculate_accuracy("AAAA", "TTTT")
        self.assertEqual(acc, 0.0)
        
        # Different lengths
        acc = calculate_accuracy("ACGT", "AC")
        self.assertGreater(acc, 0.0)
        self.assertLess(acc, 1.0)
    
    def test_edit_distance(self):
        """Test edit distance calculation."""
        # Identical strings
        self.assertEqual(edit_distance("ACGT", "ACGT"), 0)
        
        # Single substitution
        self.assertEqual(edit_distance("ACGT", "ACGG"), 1)
        
        # Single insertion
        self.assertEqual(edit_distance("ACGT", "ACGGT"), 1)
        
        # Single deletion
        self.assertEqual(edit_distance("ACGT", "ACT"), 1)
        
        # Multiple operations
        self.assertEqual(edit_distance("ACGT", "TGCA"), 4)


if __name__ == '__main__':
    unittest.main()
