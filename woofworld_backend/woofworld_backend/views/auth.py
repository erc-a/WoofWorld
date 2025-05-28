# woofworld_backend/woofworld_backend/views/auth.py
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized, HTTPOk
from ..models import User
from ..models.user import UserRole
from ..security import get_user, hash_password, check_password
import logging
import jwt
# Hapus import shutil, os, uuid jika tidak digunakan lagi untuk upload file
# import shutil
# import os
# import uuid

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
        new_user.set_password(password)
        request.dbsession.add(new_user)
        request.dbsession.flush()

        token = request.create_jwt_token(str(new_user.id))

        return {
            'message': 'Registrasi berhasil.',
            'user': new_user.to_dict(), # Pastikan to_dict() tidak mengirim profile_picture jika sudah dihapus dari model
            'token': token
        }
    except HTTPBadRequest as e:
        request.response.status_code = e.status_int # type: ignore
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

        if user and user.check_password(password):            # Create JWT token with explicit settings
            settings = request.registry.settings
            jwt_secret = settings['jwt.secret']
            jwt_algorithm = settings.get('jwt.algorithm', 'HS256')
            jwt_expiration = int(settings.get('jwt.expiration', 3600))

            log.info(f"LOGIN_VIEW: Creating token for user ID: {user.id}")
            log.info(f"LOGIN_VIEW: Using algorithm: {jwt_algorithm}")

            # Create token with explicit claims
            token = request.create_jwt_token(
                str(user.id),
                expiration=jwt_expiration,
                algorithm=jwt_algorithm
            )
            
            log.info(f"LOGIN_VIEW: Token created successfully")

            # --- Tes Decode Manual Langsung Setelah Pembuatan ---
            try:
                decoded_payload_manual = jwt.decode(
                    token,
                    actual_secret_for_creation,
                    algorithms=[actual_algorithm_for_creation]
                )
                log.info(f"LOGIN_VIEW: Decode manual token BARU SUKSES. Payload: {decoded_payload_manual}")
                if str(decoded_payload_manual.get('sub')) != str(user.id):
                    log.error(f"LOGIN_VIEW: PERINGATAN! 'sub' di token ({decoded_payload_manual.get('sub')}) tidak cocok dengan user.id ({user.id}) setelah decode manual.")

            except jwt.ExpiredSignatureError:
                log.error("LOGIN_VIEW: Decode manual token BARU GAGAL - Token expired (Seharusnya tidak terjadi untuk token baru)")
            except jwt.InvalidSignatureError:
                log.error("LOGIN_VIEW: Decode manual token BARU GAGAL - INVALID SIGNATURE! (Ini masalah besar jika terjadi di sini!)")
            except Exception as e:
                log.error(f"LOGIN_VIEW: Decode manual token BARU GAGAL - Error lain: {e}", exc_info=True)
            # --- Akhir Tes Decode Manual ---

            return {
                'message': 'Login berhasil.',
                'token': token,
                'user': user.to_dict()
            }
        else:
            raise HTTPUnauthorized(json_body={'message': 'Email atau password salah.'})
    except (HTTPBadRequest, HTTPUnauthorized) as e:
        request.response.status_code = e.status_int # type: ignore
        return e.json_body
    except Exception as e:
        log.error(f"Login error: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Terjadi kesalahan internal saat login.'}



@view_config(route_name='verify_token', request_method='GET', renderer='json', permission='view_authenticated')
def verify_token_view(request):
    try:
        # Log the incoming token
        auth_header = request.headers.get('Authorization', '')
        log.info(f"VERIFY_TOKEN: Received Authorization header: {auth_header}")
        
        # Log JWT claims if they exist
        if hasattr(request, 'jwt_claims'):
            log.info(f"VERIFY_TOKEN: JWT claims present: {request.jwt_claims}")
        else:
            log.warning("VERIFY_TOKEN: No JWT claims found in request")
            
        current_user = get_user(request)
        if current_user:
            log.info(f"VERIFY_TOKEN: User found - ID: {current_user.id}, Email: {current_user.email}")
            return current_user.to_dict()
            
        log.warning("VERIFY_TOKEN: No user found for token")
        raise HTTPUnauthorized(json_body={'message': 'Token tidak valid atau sesi berakhir.'})
    except Exception as e:
        log.error(f"VERIFY_TOKEN: Verification failed: {e}", exc_info=True)
        raise HTTPUnauthorized(json_body={'message': 'Token tidak valid atau sesi berakhir.'})

@view_config(route_name='update_profile', request_method='PUT', renderer='json', permission='manage_profile')
def update_profile_view(request):
    try:
        current_user = get_user(request)
        if not current_user:
            # Ini seharusnya tidak terjadi jika permission 'manage_profile' bekerja dengan benar
            # dan get_user mengembalikan None jika token tidak valid/user tidak ada.
            raise HTTPUnauthorized(json_body={'message': 'Autentikasi dibutuhkan.'})

        json_data = request.json_body
        name = json_data.get('name')
        email = json_data.get('email')

        if name:
            current_user.name = name
        if email:
            existing_user = request.dbsession.query(User).filter(
                User.email == email,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPBadRequest(json_body={'message': 'Email sudah digunakan oleh pengguna lain.'})
            current_user.email = email

        # Tidak ada lagi pemrosesan untuk profile_picture
        # current_user.profile_picture bisa dibiarkan apa adanya di DB atau di-set null jika mau.
        # Untuk saat ini, kita tidak mengubahnya jika tidak ada input baru.

        request.dbsession.add(current_user) # Atau flush() saja jika hanya update
        request.dbsession.flush()

        return {
            'message': 'Profil berhasil diperbarui.',
            'user': current_user.to_dict() # Pastikan to_dict() tidak mengirim profile_picture
        }
    except (HTTPBadRequest, HTTPUnauthorized) as e: # type: ignore
        request.response.status_code = e.status_int # type: ignore
        return e.json_body
    except Exception as e:
        log.error(f"Update profile error: {e}", exc_info=True)
        request.response.status_code = 500
        return {'message': 'Terjadi kesalahan internal saat memperbarui profil.'}