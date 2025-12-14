"""Client for interacting with the National Weather Service API."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import aiohttp


class WeatherClient:
    """Client for interacting with the National Weather Service API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """
        Initialize the WeatherClient.

        Args:
            session: The aiohttp client session to use for requests.

        """
        self.session = session
        self.base_url = "https://api.weather.gov"

    async def get_forecast(self, lat: float, lon: float) -> dict[str, Any]:
        """
        Fetch forecast data for a specific latitude and longitude.

        Retrieves the grid point data for the coordinates and then fetches
        the corresponding forecast.

        Args:
            lat: The latitude of the location.
            lon: The longitude of the location.

        Returns:
            A dictionary containing the JSON response from the forecast endpoint.

        Raises:
            aiohttp.ClientResponseError: If the API returns a non-200 status.

        """
        url = f"{self.base_url}/points/{lat},{lon}"
        async with self.session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

        forecast_url = data["properties"]["forecast"]

        async with self.session.get(forecast_url) as response:
            response.raise_for_status()
            return await response.json()
