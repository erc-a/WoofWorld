import enum
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    Enum as SAEnum, # Hindari konflik nama dengan enum Python
)
from sqlalchemy.orm import relationship
from .meta import Base
from passlib.hash import bcrypt
from datetime import datetime

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(Text, nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(DateTime, default=datetime.utcnow)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, pw):
        self.password_hash = bcrypt.hash(pw)

    def check_password(self, pw):
        return bcrypt.verify(pw, self.password_hash)

    def to_dict(self, include_email=True):
        data = {
            'id': self.id,
            'name': self.name,
            'role': self.role.value,
            'created_at': self.created_at.isoformat()
        }
        if include_email:
            data['email'] = self.email
        return data