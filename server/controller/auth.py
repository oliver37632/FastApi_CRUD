from server.model import session_scope
from server.model.user import User
from server.model.schemas.user import SignUp, Login

from datetime import timedelta

import bcrypt

from fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, status, Depends

from config import ACCESS_TIMEOUT, REFRESH_TIMEOUT

app = APIRouter(
    prefix="/auths",
    tags=["auth"],
    responses={404: {"message": "Not Found"}}
)


@app.post("", status_code=status.HTTP_200_OK)
async def auth(userId: str):
    with session_scope() as session:

        auth = session.query(User).filter(User.id == userId)

        if not auth.scalar():
            return {
                "message": "usable"
            }, 200

        return {
                "message": "overlap"
            }, 409


@app.post("/signups", status_code=status.HTTP_201_CREATED)
async def signup(body: SignUp):
    with session_scope() as session:
        try:
            new_signup = User(
                id=body.id,
                name=body.name,
                password=bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt())
            )

            session.add(new_signup)
            session.commit()
        except ValueError:
            return {
                "message": "id is overlap"
            }, 409


@app.post("/logins", status_code=status.HTTP_200_OK)
async def login(body: Login, authorize: AuthJWT=Depends()):

    access_expires_delta = timedelta(minutes=ACCESS_TIMEOUT)
    refresh_expires_delta = timedelta(minutes=REFRESH_TIMEOUT)

    access_token = authorize.create_access_token(
        subject=body.id,
        expires_time=access_expires_delta
    )
    refresh_token = authorize.create_refresh_token(
        subject=body.id,
        expires_time=refresh_expires_delta
    )


    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }, 200








