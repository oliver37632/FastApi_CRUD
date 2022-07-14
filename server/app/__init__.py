from fastapi import APIRouter

from server.app import auth, post, comment

api_router = APIRouter()

api_router.include_router(auth.app, prefix="/auths", tags=["auth"])
api_router.include_router(post.app, prefix="/posts", tags=["post"])
api_router.include_router(comment.app, prefix="/comments", tags=["comment"])