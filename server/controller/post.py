from server.model import session_scope
from server.model.post import Post

from server.model.schemas.post import Posts
from server.utils.auth import token_check


from fastapi import APIRouter, status, Depends, Response

from fastapi_jwt_auth import AuthJWT

app = APIRouter(
    prefix="/posts",
    tags=["post"],
    responses={404: {"message": "Not Found"}}
)


@app.post("", status_code=status.HTTP_201_CREATED)
async def post(body: Posts, authorize: AuthJWT = Depends()):
    with session_scope() as session:
        token_check(authorize=authorize, type="access")
        user_id = authorize.get_jwt_subject()
        new_posts = Post(
            user_id="test",
            title=body.title,
            content=body.content
        )

        session.add(new_posts)
        session.commit()

    return {
        "message": "success"
    }, 201


@app.get("", status_code=status.HTTP_200_OK)
async def get_post(authorize: AuthJWT=Depends()):
    with session_scope() as session:
        token_check(authorize=authorize, type="access")

        posts = session.query(Post).all()

        if posts:
            return {
                "posts": [{
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "user_id": post.user_id
                } for post in posts]
            }, 200
        return {
            "message": "NotFound"
        }, 404


@app.delete("")
async def post_delete(id: int, authorize: AuthJWT=Depends()):
    with session_scope() as session:
        token_check(authorize=authorize, type="access")
        user_id = authorize.get_jwt_subject()

        post_del = session.query(Post).filter(Post.id == id, Post.user_id == user_id).first()

        if post_del:
            session.delete(post_del)
            session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
