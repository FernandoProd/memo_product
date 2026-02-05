from services.libs.clients.base import BaseClient
from fastapi import HTTPException, status
import httpx

class AuthServiceClient(BaseClient):
    def __init__(self):
        super().__init__(base_url="http://localhost:8001")

    async def get_current_user(self, token) -> httpx.Response:
        response = await self.post(
            "/auth/verify_token",
            json={
                "token": token
            }
        )

        return response