from server.core.model.post import Post
from server.core.model.comment import Comment
from server.utils.security import check_comment

from sqlalchemy.orm import Session


def create_comment(content: str, user_id: str, post_id: int, session: Session):
    new_comment = Comment(
        content=content,
        user_id=user_id,
        post_id=post_id
    )

    session.add(new_comment)
    session.commit()

    return {
        "message": "success"
    }

