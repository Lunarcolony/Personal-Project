# Model Architecture Diagram

```
                    Nanopore Signal to DNA Sequence Model
                    =====================================

Input Signal
(1D electrical current)
     │
     ▼
┌──────────────────────┐
│  Conv1D (5x5)        │
│  64 filters          │
│  + BatchNorm + ReLU  │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│  Conv1D (5x5)        │
│  128 filters         │
│  + BatchNorm + ReLU  │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│  Conv1D (5x5)        │
│  256 filters         │
│  + BatchNorm + ReLU  │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│  Bidirectional LSTM  │
│  Hidden: 256         │
│  Layers: 3           │
│  + Dropout           │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│  Linear Layer        │
│  Output: 5 classes   │
│  (A, C, G, T, blank) │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│  Log Softmax         │
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│  CTC Decoding        │
│  (remove blanks &    │
│   duplicates)        │
└──────────────────────┘
     │
     ▼
DNA Sequence
(ACGT string)


Key Features:
=============

1. Feature Extraction: 3 convolutional layers progressively increase
   the feature dimension from 1 → 64 → 128 → 256

2. Temporal Modeling: Bidirectional LSTM captures dependencies in
   both forward and backward directions

3. CTC Loss: Allows the model to learn alignments between variable-length
   input signals and output sequences without pre-aligned training data

4. Output: Probability distribution over DNA bases at each time step
```

## Model Statistics

- **Total Parameters**: ~1M (default configuration)
- **Input**: Variable-length 1D signal
- **Output**: Variable-length DNA sequence
- **Training**: CTC loss with Adam optimizer
- **Inference**: Greedy decoding with duplicate/blank removal
