from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class SocialMediaPosts(Base):
    __tablename__ = "social_media_posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("Users") # the class name Users
    
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Votes(Base):
    __tablename__ = "votes"
    social_media_post_id = Column(Integer, ForeignKey("social_media_posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
