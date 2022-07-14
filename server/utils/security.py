from fastapi import HTTPException, Depends, status

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import ACCESS_TIMEOUT, SECRET, ALGORITHM

from server.core.model import session_scope
from server.core.model.user import User
from server.core.model.post import Post
from server.core.model.comment import Comment

from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: str):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TIMEOUT)
    encoded_jwt = jwt.encode({"exp": exp, "sub": user_id}, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    with session_scope() as session:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = session.query(User).filter(User.id == user_id)
        if not user.scalar():
            raise credentials_exception
        return user.first()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def check_post(id: str, post_id: int, session: Session):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this post is not found")

    if post.user_id == id or id == "admin":
        return post

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not valid")


def check_comment(username: str, comment_id: int, session: Session):
    comment = session.query(Comment).filter(Comment.id == comment_id).scalar()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this comment is not found")

    if comment.username == username or username == "admin":
        return comment

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is not valid")
