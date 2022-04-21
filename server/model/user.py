from sqlalchemy import Column, VARCHAR, text, Integer
from sqlalchemy.orm import relationship

from server.model import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(VARCHAR(10), primary_key=True)
    name = Column(VARCHAR(5), nullable=True)
    password = Column(VARCHAR(255), nullable=True)

    post = relationship("Post", cascade="all,delete", backref="user")
    comment = relationship("Comment", cascade="all,delete", backref="user")

