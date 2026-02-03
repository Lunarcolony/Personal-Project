# Contributing to Nanopore Basecaller

Thank you for your interest in contributing to this project! This document provides guidelines for contributions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Personal-Project.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`

## Development Setup

### Running Tests

```bash
python -m pytest tests/
```

Or run individual test files:
```bash
python tests/test_model.py
python tests/test_data_processor.py
python tests/test_utils.py
```

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

## How to Contribute

### Reporting Bugs

- Use the GitHub issue tracker
- Describe the bug clearly
- Include steps to reproduce
- Provide system information (OS, Python version, PyTorch version)

### Suggesting Features

- Open an issue with the "feature request" label
- Describe the feature and its use case
- Explain how it would benefit the project

### Submitting Code

1. Make your changes in a feature branch
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation as needed
5. Commit with clear, descriptive messages
6. Push to your fork
7. Create a pull request

### Pull Request Guidelines

- One feature/fix per PR
- Include tests for new code
- Update README if needed
- Follow existing code style
- Provide a clear description of changes

## Code Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Areas for Contribution

### High Priority

- [ ] Support for FAST5 file format
- [ ] Pre-trained model weights
- [ ] Transformer-based architecture option
- [ ] Performance benchmarking tools
- [ ] Real nanopore data examples

### Medium Priority

- [ ] Modified base detection (methylation)
- [ ] Data augmentation techniques
- [ ] Hyperparameter optimization tools
- [ ] Integration with basecalling pipelines
- [ ] Visualization tools

### Documentation

- [ ] Tutorial notebooks
- [ ] API documentation
- [ ] Use case examples
- [ ] Performance optimization guide

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
