from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .meta import Base

class Favorite(Base):
    __tablename__ = 'favorites'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    breed_api_id = Column(String(100), primary_key=True) 
    breed_name = Column(String(255), nullable=False)
    breed_image_url = Column(Text)
    breed_temperament = Column(Text)

    user = relationship("User", back_populates="favorites")
    # TIDAK ADA relasi ke DogBreed lokal di sini

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'id': self.breed_api_id, # Frontend mungkin mengharapkan 'id' untuk breed
            'breed_api_id': self.breed_api_id,
            'name': self.breed_name, # Diganti dari self.breed.name
            'image': {'url': self.breed_image_url} if self.breed_image_url else None, # Sesuaikan dengan struktur yg diharapkan frontend
            'temperament': self.breed_temperament
        }