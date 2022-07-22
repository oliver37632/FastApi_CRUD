from server.core.model import session_scope
from server.core.model.user import User
from server.core.schemas.comment import Comments

from server.utils.security import get_current_user
from server.utils.comment import create_comment
from fastapi import APIRouter, status, Depends

app = APIRouter()


@app.post("")
async def write_comment(body: Comments, user: User = Depends(get_current_user)):
    with session_scope() as session:
        req = create_comment(content=body.content, post_id=body.post_id, session=session, user_id=user.id)

        return req