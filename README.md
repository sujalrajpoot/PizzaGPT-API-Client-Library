# PizzaGPT API Client Library

## Overview

The PizzaGPT API Client Library is a professional-grade Python implementation for interacting with the PizzaGPT API. This library provides a robust, type-safe, and maintainable way to integrate PizzaGPT's capabilities into your Python applications.

## Important Disclaimer

This code is provided strictly for educational purposes to demonstrate professional Python programming practices, API client implementation patterns, and modern software architecture concepts. It should not be used in any way that could harm, disrupt, or disrespect PizzaGPT's services or infrastructure. Before using this code or interacting with any API, ensure you have proper authorization and comply with all relevant terms of service and usage policies.

## Features

- Robust error handling with custom exception hierarchy
- Type-safe implementation with comprehensive type hints
- Environment-specific configuration management
- Secure credential handling
- Automatic session management and connection pooling
- Comprehensive logging support
- Clean and maintainable object-oriented design
- Full test coverage and documentation

## Requirements

- Python 3.8 or higher
- Required packages:
  - requests
  - typing
  - dataclasses
  - logging

## Installation

```bash
pip install requests

# For development installation
git clone https://github.com/sujalrajpoot/PizzaGPT-API-Client-Library.git
cd PizzaGPT-API-Client-Library
```

## Quick Start

Basic usage of the library:

```python
from pizzagpt_client import PizzaGPTService, PizzaGPTError

# Create a service instance with default configuration
service = PizzaGPTService()

try:
    # Get a response from PizzaGPT
    response = service.get_response("What's the best pizza topping?")
    print(f"Response: {response}")
except PizzaGPTError as e:
    print(f"Error: {str(e)}")
```

### Error Handling

```python
from pizzagpt_client import (
    PizzaGPTError,
    APIConnectionError,
    APIResponseError
)

try:
    response = service.get_response("Hello")
except APIConnectionError as e:
    print(f"Connection error: {str(e)}")
except APIResponseError as e:
    print(f"API error {e.status_code}: {e.message}")
except PizzaGPTError as e:
    print(f"General error: {str(e)}")
```

## Architecture

The library follows a clean architecture pattern with several key components:

1. **APIClient (Abstract Base Class)**
   - Defines the interface for API interactions
   - Ensures consistent implementation across different client versions

2. **PizzaGPTClient**
   - Concrete implementation of the APIClient interface
   - Handles low-level API communication
   - Manages sessions and authentication

3. **PizzaGPTService**
   - High-level service class
   - Provides a simplified interface for common operations
   - Handles business logic and error management

4. **Support Classes**
   - APICredentials: Immutable credential management
   - APIResponse: Structured response handling
   - Custom exceptions: Granular error handling

## Error Handling

The library implements a comprehensive error handling hierarchy:

```
PizzaGPTError
├── APIConnectionError
└── APIResponseError
```

Each error type provides specific information about the failure mode and appropriate recovery strategies.

## Roadmap

- [ ] Add async support
- [ ] Implement request rate limiting
- [ ] Add response caching
- [ ] Create CLI interface
- [ ] Add middleware support
- [ ] Implement retry mechanisms

## Acknowledgments

- Thanks to the PizzaGPT team for their amazing service
- This project is inspired by professional API client implementations
- Special thanks to all contributors

**Remember** to always respect API terms of service and usage policies when using this library. This code is for educational purposes only. Use responsibly and ethically.

---

Created with ❤️ by **Sujal Rajpoot**

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
