"""
Inference module for making predictions with trained models.
"""

import torch
import numpy as np
from .data_processor import SignalProcessor, NanoporeDataset


def predict_sequence(model, signal, processor=None, device=None):
    """
    Predict DNA sequence from a nanopore signal.
    
    Args:
        model: Trained basecaller model
        signal (np.ndarray): Raw nanopore signal
        processor (SignalProcessor): Signal processor (optional)
        device: Device to run inference on
        
    Returns:
        str: Predicted DNA sequence
    """
    if processor is None:
        processor = SignalProcessor()
    
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model.to(device)
    model.eval()
    
    # Process signal
    processed_signal = processor.process(signal)
    signal_tensor = torch.FloatTensor(processed_signal).unsqueeze(0).unsqueeze(-1)
    signal_tensor = signal_tensor.to(device)
    
    # Make prediction
    with torch.no_grad():
        output = model(signal_tensor)
        predictions = torch.argmax(output, dim=2)
    
    # Decode predictions
    dataset = NanoporeDataset([signal])
    sequence = dataset.decode_sequence(predictions[0])
    
    return sequence


def batch_predict(model, signals, processor=None, device=None, batch_size=32):
    """
    Predict DNA sequences for multiple signals.
    
    Args:
        model: Trained basecaller model
        signals (list): List of raw nanopore signals
        processor (SignalProcessor): Signal processor (optional)
        device: Device to run inference on
        batch_size (int): Batch size for inference
        
    Returns:
        list: List of predicted DNA sequences
    """
    if processor is None:
        processor = SignalProcessor()
    
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model.to(device)
    model.eval()
    
    predictions = []
    dataset = NanoporeDataset(signals, processor=processor)
    
    # Process in batches
    for i in range(0, len(signals), batch_size):
        batch_signals = signals[i:i+batch_size]
        batch_tensors = []
        
        for signal in batch_signals:
            processed = processor.process(signal)
            tensor = torch.FloatTensor(processed).unsqueeze(-1)
            batch_tensors.append(tensor)
        
        # Pad to same length
        max_len = max(t.size(0) for t in batch_tensors)
        padded = torch.zeros(len(batch_tensors), max_len, 1)
        
        for j, tensor in enumerate(batch_tensors):
            padded[j, :tensor.size(0), :] = tensor
        
        padded = padded.to(device)
        
        # Predict
        with torch.no_grad():
            output = model(padded)
            batch_predictions = torch.argmax(output, dim=2)
        
        # Decode
        for pred in batch_predictions:
            sequence = dataset.decode_sequence(pred)
            predictions.append(sequence)
    
    return predictions


def load_model(model_path, model_class, device=None):
    """
    Load a trained model from checkpoint.
    
    Args:
        model_path (str): Path to model checkpoint
        model_class: Model class to instantiate
        device: Device to load model on
        
    Returns:
        model: Loaded model
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    checkpoint = torch.load(model_path, map_location=device)
    
    # Create model instance
    model = model_class()
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    return model
