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
        (Allow, Everyone, 'view'), # Permission untuk mengakses endpoint publik seperti facts
        (Allow, Everyone, 'view_public'), # Untuk endpoint publik
        (Allow, Authenticated, 'view_authenticated'), # Untuk user yg login
        (Allow, 'role:admin', 'admin_access'), # Untuk admin
    ]
    def __init__(self, request):
        self.request = request

class AuthenticatedUserFactory(RootFactory):
     # User yang sudah login boleh akses
    __acl__ = [
        (Allow, Authenticated, 'access_favorites'),
        (Allow, 'role:admin', 'admin_access'), # Admin juga boleh
    ]

class AdminFactory(RootFactory):
    # Hanya admin yang boleh akses
    __acl__ = [
        (Allow, 'role:admin', 'admin_dashboard'),
        (Allow, 'role:admin', 'manage_users'),
        (Allow, 'role:admin', 'manage_breeds'),
        (Allow, 'role:admin', 'manage_facts'),
        (Allow, 'role:admin', 'manage_videos'),
        (Allow, 'role:admin', 'view_analytics'),
    ]