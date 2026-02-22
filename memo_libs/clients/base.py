import httpx
import logging


logger = logging.getLogger(__name__)


class BaseClient:
    """A basic async HTTP-client for interaction of microservices"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> httpx.Response:
        """Internal method for HTTP requests"""

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.request(method, endpoint, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error on {method} {endpoint}: {e}")
                raise
            except Exception as e:
                logger.exception(f"Unexpected error on {method} {endpoint}")
                raise

    async def post(self, endpoint: str, **kwargs) -> httpx.Response:
        """Send a POST request"""
        return await self._request("POST", endpoint, **kwargs)

    async def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """Send a GET request"""
        return await self._request("GET", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        """Send a DELETE request"""
        return await self._request("DELETE", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> httpx.Response:
        """Send a PUT request"""
        return await self._request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs) -> httpx.Response:
        """Send a PATCH request"""
        return await self._request("PATCH", endpoint, **kwargs)