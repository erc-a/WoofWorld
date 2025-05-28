from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from .meta import Base
from datetime import datetime

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'videoUrl': self.video_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'isPublic': self.is_public
        }