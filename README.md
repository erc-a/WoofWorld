# 🐕 WoofWorld

WoofWorld adalah aplikasi web yang didedikasikan untuk pecinta anjing, menyediakan informasi lengkap tentang berbagai jenis anjing, fakta menarik tentang anjing, dan platform untuk menyimpan ras anjing favorit Anda.

## 📋 Fitur

- **Penjelajah Ras**: Jelajahi dan cari berbagai ras anjing
- **Informasi Detail**: Dapatkan detail lengkap tentang setiap ras
- **Fakta Anjing**: Pelajari fakta menarik tentang anjing
- **Favorit**: Simpan dan kelola ras anjing favorit Anda
- **Autentikasi Pengguna**: Sistem login dan registrasi yang aman

## 🛠 Teknologi yang Digunakan

### Frontend
- React.js
- Tailwind CSS
- Framer Motion
- React Router

### Backend
- Python (Pyramid Framework)
- PostgreSQL
- SQLAlchemy
- Alembic (Migrasi Database)
- JWT Authentication

## 🚀 Memulai

### Prasyarat
- Node.js (v14 atau lebih tinggi)
- Python 3.8 atau lebih tinggi
- PostgreSQL
- Conda (untuk manajemen environment)

### Instalasi

1. **Clone repository**
```bash
git clone https://github.com/erc-a/WoofWorld.git
cd WoofWorld
```

2. **Setup Frontend**
```bash
cd frontend
npm install
npm run dev
```

3. **Setup Backend**
```bash
cd backend
conda env create -f environment.yml
conda activate woofworld
pip install -e .
alembic upgrade head
pserve development.ini --reload
```

4. **Setup Database**
```bash
# Buat database PostgreSQL
psql -U postgres
CREATE DATABASE woofworld;
```

## 🌐 Endpoint API

- `GET /api/breeds`: Mendapatkan semua ras anjing
- `GET /api/breeds/{id}`: Mendapatkan detail ras spesifik
- `GET /api/facts`: Mendapatkan fakta acak tentang anjing
- `POST /api/register`: Registrasi pengguna baru
- `POST /api/login`: Login pengguna
- `GET /api/favorites`: Mendapatkan ras favorit pengguna
- `POST /api/favorites`: Menambahkan ras ke favorit

## 👥 Kontributor

- **Eric Arwido Damanik** (122140157)
  - Pengembangan Frontend & Backend
  - Desain Database
  - Integrasi API

## 📝 Lisensi

Proyek ini dikumpulkan sebagai bagian dari persyaratan mata kuliah Pemrograman Web (IF3028) di Institut Teknologi Sumatera.

## 📞 Kontak

Untuk pertanyaan tentang proyek ini, silakan hubungi:
- Email: eric.122140157@student.itera.ac.id
- GitHub: erc-a

---
© 2025 WoofWorld. Hak Cipta Dilindungi.
