# Contributing to YouTube Goniometer

Thank you for your interest in contributing to YouTube Goniometer! This document provides guidelines for contributing to the project.

## Getting Started

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/youtube-goniometer.git
   cd youtube-goniometer
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode:**
   ```bash
   pip install -e ".[dev]"
   ```

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Pylint** for linting
- **MyPy** for type checking

Run these before submitting:
```bash
black .
pylint *.py visualizers/
mypy *.py
```

### Testing

Run the test suite:
```bash
# Basic functionality test
python -c "import app; print('✓ Import successful')"

# Run with pytest if available
pytest
```

## Types of Contributions

### Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce
- Provide system information (OS, Python version)
- Include error messages and logs

### Feature Requests
- Describe the feature and its use case
- Explain why it would be valuable
- Consider implementation complexity

### Code Contributions

#### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow existing code style
   - Add type hints
   - Update documentation
   - Add tests if applicable

3. **Test your changes:**
   ```bash
   python app.py  # Test the application
   black .        # Format code
   pylint *.py    # Check for issues
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

#### Code Guidelines

- **Functions**: Include docstrings with type annotations
- **Classes**: Document purpose and key methods
- **Variables**: Use descriptive names
- **Imports**: Group and sort imports logically
- **Error Handling**: Use appropriate exceptions and logging

Example:
```python
def process_audio_data(samples: np.ndarray, sample_rate: int) -> Dict[str, float]:
    """
    Process audio samples to extract stereo characteristics.
    
    Args:
        samples: Audio data array with shape (n_samples, 2)
        sample_rate: Sample rate in Hz
        
    Returns:
        Dictionary containing phase correlation and other metrics
        
    Raises:
        ValueError: If samples array has incorrect shape
    """
    if samples.shape[1] != 2:
        raise ValueError("Expected stereo audio (2 channels)")
    
    # Implementation here...
    return {"phase_correlation": 0.8}
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update configuration documentation
- Include examples where helpful

## Priority Areas for Contribution

### High Priority
- **Platform Testing** - Test on different OS versions
- **Performance Optimization** - Improve real-time processing
- **Error Handling** - Better error messages and recovery
- **Documentation** - Improve user guides and examples

### Medium Priority
- **Feature Enhancements** - Additional visualizations
- **UI Improvements** - Better user experience
- **Configuration Options** - More customization
- **Export Features** - Save/load functionality

### Nice to Have
- **Plugin System** - Extensible architecture
- **Advanced Analytics** - More audio analysis features
- **Themes** - Custom color schemes
- **Automation** - Batch processing capabilities

## Development Guidelines

### Audio Processing
- Maintain real-time performance
- Handle edge cases (silence, clipping)
- Consider different sample rates
- Test with various audio content

### GUI Development
- Keep interface responsive
- Follow Qt/PySide6 best practices
- Ensure thread safety
- Handle window resize properly

### YouTube Integration
- Respect rate limits
- Handle network errors gracefully
- Support various video formats
- Consider privacy implications

## Questions and Support

- **General Questions**: Use GitHub Discussions
- **Bug Reports**: Use GitHub Issues
- **Development Help**: Tag maintainers in issues
- **Real-time Chat**: Consider creating Discord/Slack

## Recognition

Contributors will be:
- Added to AUTHORS file
- Mentioned in release notes
- Credited in documentation

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.