from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import remember, forget
from ..models import User
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your-secret-key'  # Change this in production

@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    email = request.json_body.get('email')
    password = request.json_body.get('password')
    
    user = request.dbsession.query(User).filter_by(email=email).first()
    
    if user and user.check_password(password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, SECRET_KEY, algorithm='HS256')
        
        return {
            'token': token,
            'user': user.__json__()
        }
    
    return Response(json={'error': 'Invalid credentials'}, status=401)