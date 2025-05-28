from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized, HTTPOk
from ..models import User 
from ..models.user import UserRole
from ..security import get_user, hash_password, check_password # Ambil dari security.py
import logging
import shutil
import os
import uuid

log = logging.getLogger(__name__)

@view_config(route_name='register', request_method='POST', renderer='json')
def register_view(request):
    try:
        json_body = request.json_body
        name = json_body.get('name')
        email = json_body.get('email')
        password = json_body.get('password')

        if not all([name, email, password]):
            raise HTTPBadRequest(json_body={'message': 'Nama, email, dan password dibutuhkan.'})

        if request.dbsession.query(User).filter_by(email=email).first():
            raise HTTPBadRequest(json_body={'message': 'Email sudah terdaftar.'})

        new_user = User(name=name, email=email)
        new_user.set_password(password) # Gunakan method dari model User
        # Default role adalah 'user' seperti di model
        request.dbsession.add(new_user)
        request.dbsession.flush() # Untuk mendapatkan ID user

        # Generate token setelah registrasi (opsional, tapi umum)
        token = request.create_jwt_token(new_user.id) # 'sub' (subject) diisi user.id
        
        return {
            'message': 'Registrasi berhasil.',
            'user': new_user.to_dict(),
            'token': token
        }
    except HTTPBadRequest as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Register error: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Terjadi kesalahan internal saat registrasi.'}

@view_config(route_name='login', request_method='POST', renderer='json')
def login_view(request):
    try:
        email = request.json_body.get('email')
        password = request.json_body.get('password')

        if not email or not password:
            raise HTTPBadRequest(json_body={'message': 'Email dan password dibutuhkan.'})

        user = request.dbsession.query(User).filter_by(email=email).first()

        if user and user.check_password(password): # Gunakan method dari model User
            token = request.create_jwt_token(user.id) # 'sub' (subject) diisi user.id
            return {
                'message': 'Login berhasil.',
                'token': token,
                'user': user.to_dict()
            }
        else:
            raise HTTPUnauthorized(json_body={'message': 'Email atau password salah.'})
    except (HTTPBadRequest, HTTPUnauthorized) as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Login error: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Terjadi kesalahan internal saat login.'}


@view_config(route_name='verify_token', request_method='GET', renderer='json', permission='view_authenticated')
def verify_token_view(request):
    """
    Endpoint untuk frontend memverifikasi token.
    Jika decorator permission 'view_authenticated' terpenuhi, berarti token valid.
    """
    try:
        current_user = get_user(request) # Mengambil user berdasarkan token JWT
        if current_user:
            return current_user.to_dict()
        raise HTTPUnauthorized(json_body={'message': 'Token tidak valid atau sesi berakhir.'})
    except Exception as e:
        log.error(f"Token verification failed: {e}", exc_info=True)
        raise HTTPUnauthorized(json_body={'message': 'Token tidak valid atau sesi berakhir.'})

@view_config(route_name='update_profile', request_method='PUT', renderer='json', permission='view_authenticated')
def update_profile_view(request):
    """
    Endpoint untuk mengupdate profil pengguna.
    """
    try:
        current_user = get_user(request)
        if not current_user:
            raise HTTPUnauthorized(json_body={'message': 'User tidak ditemukan.'})

        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Update user data
        if name:
            current_user.name = name
        if email:
            # Check if email is already taken by another user
            existing_user = request.dbsession.query(User).filter(
                User.email == email,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPBadRequest(json_body={'message': 'Email sudah digunakan.'})
            current_user.email = email

        # Handle profile picture upload
        profile_picture = request.POST.get('profile_picture')
        if profile_picture and hasattr(profile_picture, 'file'):
            # Get file extension
            filename = profile_picture.filename
            extension = filename.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                raise HTTPBadRequest(json_body={'message': 'Format gambar tidak didukung. Gunakan JPG atau PNG.'})

            # Generate unique filename
            new_filename = f"{uuid.uuid4()}.{extension}"
            file_path = f"uploads/profiles/{new_filename}"

            # Save file
            upload_dir = os.path.join(request.registry.settings['upload_dir'], 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            full_path = os.path.join(upload_dir, new_filename)
            
            profile_picture.file.seek(0)
            with open(full_path, 'wb') as output_file:
                shutil.copyfileobj(profile_picture.file, output_file)

            current_user.profile_picture = file_path

        request.dbsession.add(current_user)
        
        return {
            'message': 'Profil berhasil diperbarui.',
            'user': current_user.to_dict()
        }
    except HTTPBadRequest as e:
        request.response.status = e.status_int
        return e.json_body
    except Exception as e:
        log.error(f"Update profile error: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Terjadi kesalahan internal saat memperbarui profil.'}