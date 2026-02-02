"""
Neural network model for nanopore basecalling.
Implements a deep learning architecture to convert electrical signals to DNA sequences.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class NanoporeBasecaller(nn.Module):
    """
    Neural network model for converting nanopore signals to DNA sequences.
    
    Architecture:
    - Convolutional layers for feature extraction from raw signal
    - Bidirectional LSTM layers for temporal modeling
    - CTC (Connectionist Temporal Classification) for sequence prediction
    
    Args:
        input_size (int): Size of input features (default: 1 for raw signal)
        hidden_size (int): Size of hidden layers (default: 256)
        num_layers (int): Number of LSTM layers (default: 3)
        num_classes (int): Number of output classes (DNA bases + blank) (default: 5)
        dropout (float): Dropout rate (default: 0.1)
    """
    
    def __init__(
        self,
        input_size=1,
        hidden_size=256,
        num_layers=3,
        num_classes=5,  # A, C, G, T + blank for CTC
        dropout=0.1
    ):
        super(NanoporeBasecaller, self).__init__()
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        
        # Convolutional layers for feature extraction
        self.conv_layers = nn.Sequential(
            nn.Conv1d(input_size, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Conv1d(64, 128, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(128, 256, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm1d(256),
            nn.ReLU(),
        )
        
        # Bidirectional LSTM layers
        self.lstm = nn.LSTM(
            256,  # Input size from conv layers
            hidden_size,
            num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Output layer for CTC
        self.fc = nn.Linear(hidden_size * 2, num_classes)  # *2 for bidirectional
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        """
        Forward pass through the network.
        
        Args:
            x (torch.Tensor): Input tensor of shape (batch, time_steps, features)
            
        Returns:
            torch.Tensor: Output probabilities of shape (batch, time_steps, num_classes)
        """
        # x shape: (batch, time_steps, features)
        batch_size = x.size(0)
        
        # Transpose for conv1d: (batch, features, time_steps)
        x = x.transpose(1, 2)
        
        # Convolutional feature extraction
        x = self.conv_layers(x)
        
        # Transpose back: (batch, time_steps, features)
        x = x.transpose(1, 2)
        
        # LSTM processing
        x, _ = self.lstm(x)
        
        # Apply dropout
        x = self.dropout(x)
        
        # Output layer
        x = self.fc(x)
        
        # Apply log_softmax for CTC loss
        x = F.log_softmax(x, dim=2)
        
        return x
    
    def predict(self, x):
        """
        Make predictions on input signals.
        
        Args:
            x (torch.Tensor): Input tensor
            
        Returns:
            torch.Tensor: Predicted class indices
        """
        with torch.no_grad():
            output = self.forward(x)
            # Get most likely class at each time step
            predictions = torch.argmax(output, dim=2)
        return predictions


class ResidualBlock(nn.Module):
    """Residual block for deeper architectures."""
    
    def __init__(self, channels, kernel_size=5):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv1d(channels, channels, kernel_size, padding=kernel_size//2)
        self.bn1 = nn.BatchNorm1d(channels)
        self.conv2 = nn.Conv1d(channels, channels, kernel_size, padding=kernel_size//2)
        self.bn2 = nn.BatchNorm1d(channels)
        
    def forward(self, x):
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        out = F.relu(out)
        return out
