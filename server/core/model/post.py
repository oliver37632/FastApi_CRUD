from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, DATETIME, text
from sqlalchemy.orm import relationship

from server.core.model.comment import Comment

from server.core.model import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(20), nullable=False)
    content = Column(VARCHAR(255), nullable=False)
    create_at = Column(DATETIME, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    user_id = Column(VARCHAR(10), ForeignKey('user.id'))

    comment = relationship(Comment, cascade="all,delete", backref="post")

