from .models.user import User

# Fungsi callback untuk pyramid_jwt
def groupfinder(userid, request):
    """
    Dipanggil oleh pyramid_jwt untuk mendapatkan principals (groups) untuk user_id.
    user_id di sini adalah payload dari JWT, yang biasanya berisi 'sub' atau 'user_id'.
    """
    # Asumsi payload JWT memiliki key 'sub' yang berisi user.id
    user = request.dbsession.query(User).filter(User.id == userid).first()
    if user:
        groups = [f'role:{user.role.value}']
        return groups
    return None

# Fungsi helper untuk views
def get_user(request):
    # Payload JWT akan ada di request.jwt_claims jika token valid
    # Kita asumsikan 'sub' di claims adalah user_id
    user_id = request.jwt_claims.get('sub') if hasattr(request, 'jwt_claims') else None
    if user_id:
        return request.dbsession.query(User).filter(User.id == user_id).first()
    return None

def hash_password(password):
    from passlib.hash import bcrypt
    return bcrypt.hash(password)

def check_password(hashed_password, password):
    from passlib.hash import bcrypt
    return bcrypt.verify(password, hashed_password)

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    principals_allowed_by_permission,
)

class RootFactory:
    __acl__ = [
        (Allow, Everyone, 'view_public'),  # Permission for public endpoints like facts, breeds etc
        (Allow, Authenticated, 'view_authenticated'),  # For logged in users
    ]
    def __init__(self, request):
        self.request = request

class AuthenticatedUserFactory(RootFactory):
    """Factory for authenticated user routes"""
    __acl__ = [
        (Allow, Authenticated, [
            'view_authenticated',
            'manage_profile',
            'manage_favorites',
            'access_favorites'
        ])
    ]

class AdminFactory(RootFactory):
    """Factory for admin routes"""
    __acl__ = [
        (Allow, 'role:admin', [
            'admin_access',
            'admin_dashboard',
            'manage_users',
            'manage_breeds',
            'manage_facts',
            'manage_videos',
            'view_analytics',
            'manage_stats',
            'manage_analytics'
        ])
    ]