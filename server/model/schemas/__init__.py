from pydantic import BaseModel

from fastapi_jwt_auth import AuthJWT

from config import SECRET


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET


@AuthJWT.load_config
def get_config():
    return Settings()
