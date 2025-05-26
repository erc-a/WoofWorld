from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from .meta import Base
import enum
from datetime import datetime
from passlib.hash import bcrypt

class UserRole(enum.Enum):
    user = 'user'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'created_at': self.created_at.isoformat()
        }