from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from server.core.model.user import User

from server.utils.security import get_password_hash, verify_password, create_access_token


def create_user(session: Session, id: str, password: str, name: str):
    session.add(
        User(
            id=id,
            password=get_password_hash(password),
            name=name
        )
    )

    return HTTPException(status_code=status.HTTP_201_CREATED, detail="success")


def login(session: Session, id: str, password: str):
    user = session.query(User.id, User.password).filter(User.id == id)

    if not user.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id does not exist")

    user = user.first()
    if not verify_password(plain_password=password, hashed_password=user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")

    return {
        "access_token": create_access_token(user_id=user["id"])
    }


def check_id(session: Session, id: str):
    user = session.query(User.id).filter(User.id == id)

    if user.scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Overlap")

    else:
        return {
            "message": "Available"
        }