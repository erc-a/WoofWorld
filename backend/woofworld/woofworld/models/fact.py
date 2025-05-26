from sqlalchemy import Column, Integer, Text, DateTime
from .meta import Base
from datetime import datetime

class Fact(Base):
    __tablename__ = 'facts'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }