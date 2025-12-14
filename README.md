# Template Client

A modern Python template for building API clients with async/await patterns.

## Features

- 🚀 Async/await support with aiohttp
- 🧪 Comprehensive test coverage (100% required)
- 📝 Full type hints and documentation
- 🔍 Strict linting with Ruff
- 📦 Ready-to-publish Python package
- 🐳 Dev container configuration
- 🤖 Automated dependency updates with Renovate

## Requirements

- Python 3.14+
- aiohttp
- colorlog

## Installation

### From Source

```bash
git clone https://github.com/pcartwright81/template_client.git
cd template_client
pip install -e .
```

### For Development

```bash
pip install -e ".[dev,test]"
```

## Usage

```python
import aiohttp
from template_client.client import WeatherClient

async def get_weather():
    async with aiohttp.ClientSession() as session:
        client = WeatherClient(session)
        # Your implementation here
        pass
```

## Testing

Run the test suite with 100% coverage requirement:

```bash
pytest
```

This will fail if coverage drops below 100%.

## Development

### Linting

```bash
ruff check .
ruff format .
```

### Using Dev Container

This project includes a dev container configuration. Open in VS Code:

1. Install the "Dev Containers" extension
2. Click the green icon in the bottom-left corner
3. Select "Reopen in Container"

## Contributing

Contributions are welcome! Please ensure:

- All tests pass with 100% coverage
- Code is properly formatted with Ruff
- All type hints are present
- Documentation is updated

## License

MIT License - see LICENSE file for details

## API Reference

### WeatherClient

Async client for the National Weather Service API.

#### Methods

**`async get_forecast(lat: float, lon: float) -> dict[str, Any]`**

Fetch forecast data for a specific latitude and longitude.

**Parameters:**
- `lat` (float): The latitude of the location
- `lon` (float): The longitude of the location

**Returns:**
- `dict[str, Any]`: Forecast data from the API

**Raises:**
- `aiohttp.ClientResponseError`: If the API returns a non-200 status

**Example:**
```python
async with aiohttp.ClientSession() as session:
    client = WeatherClient(session)
    forecast = await client.get_forecast(39.7456, -97.0892)
    print(forecast)
```
