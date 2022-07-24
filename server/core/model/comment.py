from sqlalchemy import Column, Integer, DATETIME, VARCHAR, ForeignKey, text
from server.core.model import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(VARCHAR(255), nullable=True)
    create_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(VARCHAR(10), ForeignKey('user.id'))