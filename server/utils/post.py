from server.core.model.post import Post
from server.core.model.comment import Comment
from server.utils.security import check_post

from sqlalchemy.orm import Session


def create_post(title: str, content: str, id: str, session: Session):
    new_post = Post(
        title=title,
        content=content,
        user_id=id
    )

    session.add(new_post)
    session.commit()

    return {
        "message": "success"
    }


async def get_post_list(session: Session):
    posts = session.query(Post).all()

    return {"posts": [{
        "post_id": post.id,
        "title": post.title,
        "content": post.content,
        "user_id": post.user_id,
        "created_at": post.create_at
    } for post in posts]}


async def see_more_post(post_id: int, session: Session):
    post = session.query(Post).filter(Post.id == post_id).first()
    comments = session.query(Comment).filter(Comment.post_id == post_id).all()

    return {
        "post_id": post.id,
        "title": post.title,
        "content": post.content,
        "username": post.user_id,
        "created_at": post.create_at,
        "comment": [{
            "comment_id": comment.id,
            "content": comment.content,
            "username": comment.user_id,
            "created_at": comment.create_at
        }for comment in comments]
    }


async def edit_post(post_id: int, title: str, content: str, id:str, session: Session):
    post = check_post(post_id=post_id, id=id, session=session)

    post.title = title
    post.content = content

    return {
        "message": "success"
    }


async def delete_post(post_id: int, id: str, session: Session):
    post = check_post(post_id=post_id, id=id, session=session)

    session.delete(post)

    return {
        "message": "success"
    }