from memo_libs.clients.base import BaseClient
import httpx
import logging


logger = logging.getLogger(__name__)


class UserServiceClient(BaseClient):
    """Client for interacting with the user service"""

    def __init__(
            self,
            api_key: str | None = None,
            base_url: str | None = None,
    ):
        super().__init__(
            base_url=base_url
        )
        self.api_key = api_key

    async def verify_password(
            self,
            email: str,
            password: str
    ) -> httpx.Response:
        """
        Verify user credentials with the user service.

        Args:
            - email: User's email.
            - password: User's password.

        Returns:
            - Response containing user data if credentials are valid.
        """

        response = await self.post(
            "/api/v1/users/verify",
            json={
                "email": email,
                "password": password
            }
        )
        return response

    async def get_user_by_id(
            self,
            user_id: str,
    ) -> httpx.Response:
        """
        Retrieve user details by ID.

        Args:
            user_id: UUID of the user.

        Returns:
            Response containing user data.
        """

        headers = {}
        if self.api_key:
            headers["X-Internal-Api-Key"] = self.api_key

        logger.debug(f"Fetching user by ID: {user_id}")
        response = await self.get(
            f'/api/v1/users/{user_id}',
            headers=headers
        )
        return response
