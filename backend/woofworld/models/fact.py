from sqlalchemy import (
    Column,
    Integer,
    Text
)
from .meta import Base

class Fact(Base):
    __tablename__ = 'dog_facts'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content
        }