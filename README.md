# Nanopore Signal to DNA Sequence Basecaller

An AI model that converts nanopore electrical signals into DNA sequences using deep learning.

## Overview

This project implements a neural network-based basecaller for nanopore sequencing data. It uses a combination of convolutional neural networks (CNNs) for feature extraction and bidirectional LSTMs for temporal modeling, with Connectionist Temporal Classification (CTC) for sequence prediction.

## Features

- **Deep Learning Architecture**: CNN + Bidirectional LSTM with CTC loss
- **Signal Processing**: Automated filtering and normalization of raw signals
- **Training Pipeline**: Complete training framework with validation and checkpointing
- **Inference Engine**: Batch and single-signal prediction capabilities
- **Synthetic Data Generation**: Tools for testing and demonstration
- **Evaluation Metrics**: Accuracy and edit distance calculations

## Architecture

```
Input Signal → CNN Layers → BiLSTM Layers → CTC Output → DNA Sequence
   (1D)         (Feature       (Temporal      (A,C,G,T)
                extraction)     modeling)
```

### Model Components

1. **Convolutional Layers**: Extract features from raw electrical signals
2. **Bidirectional LSTM**: Capture temporal dependencies in both directions
3. **CTC Loss**: Handle variable-length sequence-to-sequence mapping
4. **Output**: Probability distribution over DNA bases (A, C, G, T) + blank

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Lunarcolony/Personal-Project.git
cd Personal-Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Requirements

- Python 3.7+
- PyTorch 2.0+
- NumPy, SciPy, scikit-learn
- h5py (for FAST5 file support)
- matplotlib (for visualization)

## Quick Start

### Run the Basic Example

```bash
python examples/basic_usage.py
```

This will:
- Generate synthetic nanopore signals
- Train a small model
- Make predictions and show accuracy

### Training a Model

```bash
python examples/train.py \
    --data-dir /path/to/data \
    --batch-size 32 \
    --epochs 100 \
    --hidden-size 256 \
    --lr 0.001 \
    --save-dir models
```

### Running Inference

Single signal:
```bash
python examples/inference.py \
    --model models/best_model.pth \
    --signal signal.npy \
    --output prediction.fasta
```

Batch inference:
```bash
python examples/inference.py \
    --model models/best_model.pth \
    --signal-dir signals/ \
    --output predictions.fasta
```

## Usage

### As a Python Library

```python
import numpy as np
from nanopore_basecaller import NanoporeBasecaller, SignalProcessor, predict_sequence

# Load or generate signal
signal = np.load('signal.npy')

# Create model and processor
model = NanoporeBasecaller()
processor = SignalProcessor()

# Load trained weights
import torch
checkpoint = torch.load('models/best_model.pth')
model.load_state_dict(checkpoint['model_state_dict'])

# Predict sequence
sequence = predict_sequence(model, signal, processor)
print(f"Predicted DNA sequence: {sequence}")
```

### Training with Custom Data

```python
from nanopore_basecaller import NanoporeBasecaller, Trainer
from nanopore_basecaller.data_processor import SignalProcessor, NanoporeDataset

# Prepare your data
signals = [...]  # List of signal arrays
sequences = [...]  # List of DNA sequences

# Create dataset
processor = SignalProcessor(normalize=True, filter_signal=True)
dataset = NanoporeDataset(signals, sequences, processor)

# Create and train model
model = NanoporeBasecaller(hidden_size=256, num_layers=3)
trainer = Trainer(model, dataset, batch_size=32, learning_rate=1e-3)
trainer.train(num_epochs=100, save_dir='models')
```

## Project Structure

```
Personal-Project/
├── src/
│   ├── nanopore_basecaller/
│   │   ├── __init__.py
│   │   ├── model.py              # Neural network architecture
│   │   ├── data_processor.py     # Signal processing & dataset
│   │   ├── trainer.py            # Training pipeline
│   │   └── inference.py          # Prediction functions
│   └── utils/
│       └── helpers.py            # Utility functions
├── examples/
│   ├── basic_usage.py            # Quick demo
│   ├── train.py                  # Training script
│   └── inference.py              # Inference script
├── tests/
│   ├── test_model.py             # Model tests
│   ├── test_data_processor.py    # Data processing tests
│   └── test_utils.py             # Utility tests
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual test files:

```bash
python tests/test_model.py
python tests/test_data_processor.py
python tests/test_utils.py
```

## Model Details

### Hyperparameters

- **Input Size**: 1 (raw signal)
- **Hidden Size**: 256 (default, configurable)
- **Number of Layers**: 3 (default, configurable)
- **Output Classes**: 5 (A, C, G, T, blank)
- **Dropout**: 0.1
- **Learning Rate**: 0.001
- **Optimizer**: Adam

### Loss Function

The model uses **CTC (Connectionist Temporal Classification)** loss, which allows the network to learn alignments between input signals and output sequences without requiring pre-aligned training data.

## Data Format

### Input Signals

- Format: 1D numpy arrays
- Type: Float32
- Represents: Electrical current measurements over time

### Output Sequences

- Format: Strings
- Characters: A, C, G, T (DNA bases)

## Performance Considerations

- **GPU Acceleration**: Automatically uses CUDA if available
- **Batch Processing**: Supports efficient batch inference
- **Memory Management**: Handles variable-length sequences efficiently

## Future Improvements

- [ ] Support for modified bases (e.g., methylation)
- [ ] Integration with FAST5 file format
- [ ] Transformer-based architecture option
- [ ] Real-time inference optimization
- [ ] Pre-trained model weights
- [ ] Benchmarking on real nanopore data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## References

- Oxford Nanopore Technologies
- Connectionist Temporal Classification (CTC)
- Deep Learning for Genomics

## Author

Lunarcolony

## Acknowledgments

This project implements concepts from nanopore basecalling research and deep learning for sequence analysis.
