from sqlalchemy import Column, Integer, DATETIME, VARCHAR, ForeignKey, text
from server.model import Base


class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(VARCHAR(255), nullable=True)
    create_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(VARCHAR(10), ForeignKey('user.id'))
