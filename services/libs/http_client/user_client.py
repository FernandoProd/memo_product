from services.libs.clients.base import BaseClient
from fastapi import HTTPException, status

class UserServiceClient(BaseClient):
    def __init__(self):
        super().__init__(base_url="http://localhost:8000/") # Ссылку вывести потом в отдельное место
                                                                # (чтобы все ссылки хранились централизованно, консолидированно)

    async def verify_password(self,
                              email: str,
                              password: str
                              ):
        try:
            response = await self.post(
                "api/api/v1/users/verify",   # тут ошибка должно быть  api/v1/users/verify
                json={
                    "email": email,
                    "password": password
                }
            )
            return response
        except HTTPException as e:
            if e.status_code == 503:
                raise e
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
