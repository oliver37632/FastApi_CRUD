from server.model import session_scope
from server.model.comment import Comment
from server.model.user import User
from server.model.post import Post

from server.model.schemas.comment import Comments

from server.utils.auth import token_check

from datetime import datetime

from fastapi import APIRouter, status, Depends

from fastapi_jwt_auth import AuthJWT

app = APIRouter(
    prefix="/comments",
    tags=["comment"],
    responses={404: {"message": "Not Found"}}
)


@app.post("", status_code=status.HTTP_201_CREATED)
async def comment_psot(post_id: int, body: Comments, authorize: AuthJWT = Depends()):
    with session_scope() as session:
        token_check(authorize=authorize, type="access")

        user_id = authorize.get_jwt_subject()

        new_comment = Comment(
            post_id=post_id,
            user_id=user_id,
            content=body.content,
            create_at=datetime.now()
        )

        session.add(new_comment)
        session.commit()

        return {
            "message", "success"
        }, 201


@app.get("", status_code=status.HTTP_200_OK)
async def comment_get(post_id: int, authorize: AuthJWT = Depends()):
    with session_scope() as session:
        token_check(authorize=authorize, type="access")
        try:
            join = session.query(
                User.id,
                Comment.content,
                Comment.create_at
            ).join(User, User.id == Comment.user_id)\
                .filter(Comment.post_id == post_id)

            return {
                "comment": [{
                    "user_id": id,
                    "content": content,
                    "create_at": str(create_at)
                } for id, content, create_at in join]
            }, 200

        except:
            return {
                "message": "Not Match"
            }, 400