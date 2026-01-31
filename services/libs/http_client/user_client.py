from services.libs.clients.base import BaseClient
from fastapi import HTTPException, status
import httpx

class UserServiceClient(BaseClient):
    def __init__(self):
        super().__init__(base_url="http://localhost:8000/") # Ссылку вывести потом в отдельное место
                                                                # (чтобы все ссылки хранились централизованно, консолидированно)

    async def verify_password(self,
                              user_id: str,
                              password: str
                              ):
        # try:
            response = await self.post(
                "api/api/v1/users/verify",   # тут ошибка должно быть  api/v1/users/verify
                params={
                    "email": email,
                    "password": password
                }
            )
            return response

        # except httpx.HTTPStatusError as e:  # Добавьте эту ветку
        #     if e.response.status_code in [401, 403, 404]:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Invalid credentials"
        #         )
        #     else:
        #         raise HTTPException(
        #             status_code=e.response.status_code,
        #             detail=f"User service error: {e.response.status_code}"
        #         )
        # except HTTPException as e:  # Оставляем для совместимости
        #     if e.status_code == 503:
        #         raise e
        #     else:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Invalid credentials",
        #         )
