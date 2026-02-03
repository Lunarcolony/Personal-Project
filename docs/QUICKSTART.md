# Quick Start Guide

This guide will help you get started with the Nanopore Signal to DNA Sequence Basecaller in just a few minutes.

## Installation

### Option 1: Install from source

```bash
git clone https://github.com/Lunarcolony/Personal-Project.git
cd Personal-Project
pip install -r requirements.txt
```

### Option 2: Install as a package

```bash
git clone https://github.com/Lunarcolony/Personal-Project.git
cd Personal-Project
pip install -e .
```

## Run Your First Example

The easiest way to understand how the model works is to run the basic example:

```bash
python examples/basic_usage.py
```

This will:
1. Generate synthetic nanopore signals from DNA sequences
2. Train a small model (5 epochs)
3. Make predictions and show accuracy

Expected output:
```
============================================================
Nanopore Signal to DNA Sequence Basecaller - Example
============================================================

1. Generating synthetic training data...
   Generated 5 training signals
   Example sequence: ACGTACGTACGT
   Signal length: 600 samples

2. Creating datasets...
   Training samples: 4
   Validation samples: 1

3. Creating model...
   Model created with 998,277 parameters

...

6. Making predictions...
   Original sequence:  ACGTACGT
   Predicted sequence: ACGTACGT
   Accuracy: 100.00%
```

## Understanding the Code

### 1. Loading and Processing Signals

```python
from nanopore_basecaller.data_processor import SignalProcessor

# Create a processor
processor = SignalProcessor(normalize=True, filter_signal=True)

# Process a signal
processed_signal = processor.process(raw_signal)
```

### 2. Creating a Model

```python
from nanopore_basecaller.model import NanoporeBasecaller

# Create model with custom parameters
model = NanoporeBasecaller(
    input_size=1,
    hidden_size=256,
    num_layers=3,
    num_classes=5,
    dropout=0.1
)
```

### 3. Training

```python
from nanopore_basecaller import Trainer
from nanopore_basecaller.data_processor import NanoporeDataset

# Create dataset
dataset = NanoporeDataset(signals, sequences, processor)

# Create trainer
trainer = Trainer(
    model=model,
    train_dataset=dataset,
    batch_size=32,
    learning_rate=1e-3
)

# Train
trainer.train(num_epochs=100, save_dir='models')
```

### 4. Making Predictions

```python
from nanopore_basecaller.inference import predict_sequence

# Predict from a signal
sequence = predict_sequence(model, signal, processor)
print(f"Predicted DNA sequence: {sequence}")
```

## Next Steps

### Work with Real Data

To use real nanopore data:

1. Obtain FAST5 files from your sequencing run
2. Extract raw signals (you'll need to implement a loader)
3. Prepare reference sequences for training
4. Train the model with more epochs (50-100+)
5. Evaluate on test data

### Customize the Model

Experiment with different hyperparameters:

```python
model = NanoporeBasecaller(
    hidden_size=512,    # Increase for more capacity
    num_layers=5,       # Deeper network
    dropout=0.2         # More regularization
)
```

### Optimize Training

```python
trainer = Trainer(
    model=model,
    train_dataset=train_data,
    val_dataset=val_data,
    batch_size=64,           # Larger batches (if memory allows)
    learning_rate=5e-4       # Tune learning rate
)
```

## Troubleshooting

### Out of Memory Error

- Reduce `batch_size`
- Reduce `hidden_size` or `num_layers`
- Use a smaller signal window

### Poor Accuracy

- Train for more epochs
- Use more training data
- Check signal quality and preprocessing
- Tune hyperparameters

### Slow Training

- Enable GPU: The code automatically uses CUDA if available
- Increase `batch_size` if memory allows
- Use fewer LSTM layers for faster training

## Resources

- [Architecture Documentation](docs/ARCHITECTURE.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Full API Documentation](README.md)

## Getting Help

If you encounter issues:

1. Check the [README](README.md) for detailed documentation
2. Review the [examples](examples/) directory
3. Open an issue on GitHub

Happy basecalling! 🧬
