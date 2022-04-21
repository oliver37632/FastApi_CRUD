from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AccessTokenRequired, RefreshTokenRequired, JWTDecodeError, MissingTokenError

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth = OAuth2PasswordBearer(tokenUrl="token")


def token_check(authorize: AuthJWT, type: str):
    try:
        if type == "access":
            authorize.jwt_required()
        elif type == "refresh":
            authorize.jwt_refresh_token_required()
        else:
            raise ValueError
    except ValueError:
        raise ValueError
    except AccessTokenRequired:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access token required")
    except RefreshTokenRequired:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="refresh token required")
    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")
    except MissingTokenError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token not found")