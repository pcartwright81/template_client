"""Tests for the WeatherClient."""

from collections.abc import Generator

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from template_client.client import WeatherClient


@pytest.fixture
def mock_aioresponses() -> Generator[aioresponses, None, None]:
    """Fixture to manage aioresponses for mocking HTTP requests."""
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_get_forecast(mock_aioresponses: aioresponses) -> None:
    """Test retrieving a forecast successfully via the two-stage API call."""
    lat = 39.7456
    lon = -97.0892

    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    mock_aioresponses.get(
        points_url,
        payload={
            "properties": {
                "forecast": "https://api.weather.gov/gridpoints/TOP/31,80/forecast"
            }
        },
    )

    forecast_url = "https://api.weather.gov/gridpoints/TOP/31,80/forecast"
    mock_data = {"properties": {"periods": [{"name": "Today", "temperature": 70}]}}
    mock_aioresponses.get(forecast_url, payload=mock_data)

    async with ClientSession() as session:
        client = WeatherClient(session)
        result = await client.get_forecast(lat, lon)

    assert result == mock_data

    mock_aioresponses.assert_called_with(points_url, method="GET")
    mock_aioresponses.assert_called_with(forecast_url, method="GET")
