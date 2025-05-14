from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime
)
from datetime import datetime
from .meta import Base
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = bcrypt.using(rounds=12).hash(password)

    def check_password(self, password):
        if not password:
            return False
        try:
            return bcrypt.verify(password, self.password_hash)
        except ValueError:
            return False

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }