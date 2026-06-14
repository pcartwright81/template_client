"""Tests for the WeatherClient."""

from collections.abc import Callable

import pytest
from aiohttp import ClientSession, ClientResponseError
from aiointercept import AsyncIntercept

from template_client.client import WeatherClient


@pytest.fixture
def mock_intercept() -> Callable:
    """Fixture to manage aiointercept for mocking HTTP requests."""
    def _intercept(intercept):
        return intercept
    return _intercept


@pytest.mark.asyncio
async def test_get_forecast() -> None:
    """Test retrieving a forecast successfully via the two-stage API call."""
    lat = 39.7456
    lon = -97.0892

    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    forecast_url = "https://api.weather.gov/gridpoints/TOP/31,80/forecast"
    mock_data = {"properties": {"periods": [{"name": "Today", "temperature": 70}]}}

    with AsyncIntercept() as intercept:
        intercept.get(
            points_url,
            payload={
                "properties": {
                    "forecast": forecast_url
                }
            },
        )
        intercept.get(forecast_url, payload=mock_data)

        async with ClientSession() as session:
            client = WeatherClient(session)
            result = await client.get_forecast(lat, lon)

        assert result == mock_data


@pytest.mark.asyncio
async def test_get_forecast_points_error() -> None:
    """Test error handling when points endpoint returns an error."""
    lat = 39.7456
    lon = -97.0892

    points_url = f"https://api.weather.gov/points/{lat},{lon}"

    with AsyncIntercept() as intercept:
        intercept.get(points_url, status=400)

        async with ClientSession() as session:
            client = WeatherClient(session)
            with pytest.raises(ClientResponseError):
                await client.get_forecast(lat, lon)


@pytest.mark.asyncio
async def test_get_forecast_forecast_error() -> None:
    """Test error handling when forecast endpoint returns an error."""
    lat = 39.7456
    lon = -97.0892

    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    forecast_url = "https://api.weather.gov/gridpoints/TOP/31,80/forecast"

    with AsyncIntercept() as intercept:
        intercept.get(
            points_url,
            payload={
                "properties": {
                    "forecast": forecast_url
                }
            },
        )
        intercept.get(forecast_url, status=500)

        async with ClientSession() as session:
            client = WeatherClient(session)
            with pytest.raises(ClientResponseError):
                await client.get_forecast(lat, lon)
