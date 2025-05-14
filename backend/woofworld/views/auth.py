from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import IntegrityError
from ..models import User
import jwt
import os

SECRET_KEY = os.environ.get('JWT_SECRET', 'your-secret-key')

@view_config(route_name='register', renderer='json', request_method='POST')
def register(request):
    try:
        json_data = request.json_body
        name = json_data.get('name')
        email = json_data.get('email')
        password = json_data.get('password')

        if not all([name, email, password]):
            request.response.status = 400
            return {
                'status': 'error',
                'message': 'Semua field harus diisi'
            }

        user = User(
            name=name,
            email=email,
            password_hash=password  # In production, hash this password!
        )

        request.dbsession.add(user)
        
        return {
            'status': 'success',
            'data': user.to_json()
        }
    except IntegrityError:
        request.response.status = 400
        return {
            'status': 'error',
            'message': 'Email sudah terdaftar'
        }

@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    try:
        json_data = request.json_body
        email = json_data.get('email')
        password = json_data.get('password')

        if not all([email, password]):
            request.response.status = 400
            return {
                'status': 'error',
                'message': 'Email dan password harus diisi'
            }

        user = request.dbsession.query(User).filter_by(email=email).first()

        if not user or not user.check_password(password):
            request.response.status = 401
            return {
                'status': 'error',
                'message': 'Email atau password salah'
            }

        token = jwt.encode(
            {'user_id': user.id},
            SECRET_KEY,
            algorithm='HS256'
        )

        return {
            'status': 'success',
            'token': token,
            'user': user.to_json()
        }

    except Exception as e:
        request.response.status = 500
        return {
            'status': 'error',
            'message': str(e)
        }