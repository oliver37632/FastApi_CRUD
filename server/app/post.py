from server.core.model import session_scope
from server.core.model.user import User
from server.core.schemas.post import Posts

from server.utils.security import get_current_user
from server.utils.post import create_post, get_post_list, see_more_post, delete_post, edit_post
from fastapi import APIRouter, status, Depends

app = APIRouter()


@app.post("", status_code=status.HTTP_201_CREATED)
async def write_post(body: Posts, user: User = Depends(get_current_user)):
    with session_scope() as session:
        req = create_post(title=body.title, content=body.content, id=user.id, session=session)
        return req


@app.get("", status_code=status.HTTP_200_OK)
async def all_get_post():
    with session_scope() as session:
        req = await get_post_list(session=session)
        return req


@app.get("/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int):
    with session_scope() as session:

        req = await see_more_post(post_id=post_id, session=session)
        return req


@app.put("/{post_id}", status_code=status.HTTP_201_CREATED)
async def update_post(post_id: int, body: Posts, user: User = Depends(get_current_user)):
    with session_scope() as session:
        req = await edit_post(post_id=post_id, title=body.title, content=body.content, id=user.id, session=session)
        return req


@app.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def del_post(post_id: int, user: User = Depends(get_current_user)):
    with session_scope() as session:
        req = await delete_post(session=session, post_id=post_id, id=user.id)
        return req