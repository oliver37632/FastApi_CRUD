from sqlalchemy import Column, VARCHAR
from sqlalchemy.orm import relationship

from server.core.model import Base
from server.core.model.post import Post
from server.core.model.comment import Comment


class User(Base):
    __tablename__ = 'user'

    id = Column(VARCHAR(10), primary_key=True)
    name = Column(VARCHAR(5), nullable=True)
    password = Column(VARCHAR(255), nullable=True)

    post = relationship(Post, cascade="all,delete", backref="user")
    comment = relationship(Comment, cascade="all,delete", backref="user")