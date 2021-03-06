from server.core.schemas.user import SignUp, Login
from server.core.model import session_scope
from server.utils.auth import create_user, check_id, login

from fastapi import APIRouter, status

app = APIRouter()


@app.post("")
async def checking_id(id: str):
    with session_scope() as session:
        return check_id(session=session, id=id)


@app.post("/signup")
async def sign_up(body: SignUp):
    with session_scope() as session:

        return create_user(id=body.id, password=body.password, name=body.name, session=session)


@app.post("/login")
async def logins(body: Login):
    with session_scope() as session:
        return login(session=session, id=body.id, password=body.password)

