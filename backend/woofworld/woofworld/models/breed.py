from sqlalchemy import Column, Integer, String, Text
from .meta import Base

class DogBreed(Base):
    __tablename__ = 'breeds'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    breed_group = Column(String(100))
    temperament = Column(Text)
    origin = Column(String(100))
    life_span = Column(String(50))
    weight_metric = Column(String(50))
    height_metric = Column(String(50))
    image_url = Column(String(255))