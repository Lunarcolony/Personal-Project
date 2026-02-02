"""
Tests for the nanopore basecaller model.
"""

import unittest
import torch
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nanopore_basecaller.model import NanoporeBasecaller


class TestNanoporeBasecaller(unittest.TestCase):
    """Test the neural network model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = NanoporeBasecaller(
            input_size=1,
            hidden_size=64,
            num_layers=2,
            num_classes=5,
            dropout=0.1
        )
    
    def test_model_initialization(self):
        """Test that model initializes correctly."""
        self.assertIsNotNone(self.model)
        self.assertEqual(self.model.input_size, 1)
        self.assertEqual(self.model.hidden_size, 64)
        self.assertEqual(self.model.num_layers, 2)
        self.assertEqual(self.model.num_classes, 5)
    
    def test_forward_pass(self):
        """Test forward pass with dummy input."""
        batch_size = 2
        time_steps = 100
        features = 1
        
        x = torch.randn(batch_size, time_steps, features)
        output = self.model(x)
        
        # Check output shape
        self.assertEqual(output.shape, (batch_size, time_steps, 5))
    
    def test_predict(self):
        """Test prediction method."""
        batch_size = 2
        time_steps = 100
        features = 1
        
        x = torch.randn(batch_size, time_steps, features)
        predictions = self.model.predict(x)
        
        # Check predictions shape
        self.assertEqual(predictions.shape, (batch_size, time_steps))
        
        # Check predictions are valid indices
        self.assertTrue(torch.all(predictions >= 0))
        self.assertTrue(torch.all(predictions < 5))
    
    def test_model_parameters(self):
        """Test that model has trainable parameters."""
        params = list(self.model.parameters())
        self.assertGreater(len(params), 0)
        
        # Check parameters require gradients
        for param in params:
            self.assertTrue(param.requires_grad)


if __name__ == '__main__':
    unittest.main()
