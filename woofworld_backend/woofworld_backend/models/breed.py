# from sqlalchemy import Column, Integer, String, Text
# from sqlalchemy.orm import relationship
# from .meta import Base

# class DogBreed(Base):
#     __tablename__ = 'dog_breeds' # Nama tabel lebih deskriptif
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False, unique=True)
#     breed_group = Column(String(100))
#     temperament = Column(Text)
#     origin = Column(String(100))
#     life_span = Column(String(50))
#     weight_metric = Column(String(50)) # contoh: "20 - 30"
#     height_metric = Column(String(50)) # contoh: "50 - 60"
#     image_url = Column(String(255)) # URL ke gambar

#     # Relasi jika ada pengguna yang memfavoritkan
#     user_favorites = relationship("Favorite", back_populates="breed")

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'breed_group': self.breed_group,
#             'temperament': self.temperament,
#             'origin': self.origin,
#             'life_span': self.life_span,
#             'weight_metric': self.weight_metric,
#             'height_metric': self.height_metric,
#             'image_url': self.image_url,
#         }