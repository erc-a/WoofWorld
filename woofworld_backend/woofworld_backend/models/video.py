from sqlalchemy import Column, Integer, String, Text, DateTime
from .meta import Base
from datetime import datetime

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    video_url = Column(String(255), nullable=False) # URL video, misal dari YouTube/TikTok
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'created_at': self.created_at.isoformat()
        }