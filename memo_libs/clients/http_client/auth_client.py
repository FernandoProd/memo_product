from memo_libs.clients.base import BaseClient
import httpx
import logging


logger = logging.getLogger(__name__)


class AuthServiceClient(BaseClient):
    """Client for interacting with the auth service"""

    def __init__(self, base_url: str | None = None):
        super().__init__(base_url=base_url)

    async def get_current_user(self, token) -> httpx.Response:
        """Verify token and return current user data"""

        logger.debug("Verifying token with auth service")
        response = await self.post(
            "/auth/verify_token",
            json={
                "token": token
            }
        )
        return response