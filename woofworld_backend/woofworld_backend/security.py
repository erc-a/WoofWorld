import logging
log = logging.getLogger(__name__) # Atau logger spesifik modul

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    principals_allowed_by_permission,
)

from .models.user import User # Pastikan User diimpor

def groupfinder(userid, request):
    log.info(f"groupfinder: Received userid = '{userid}' (type: {type(userid)})")
    
    if userid is None:
        log.warning("groupfinder: Received None userid")
        return None

    try:
        # Ensure userid is string since that's what we're storing in JWT
        userid_str = str(userid)
        user = request.dbsession.query(User).filter(User.id == int(userid_str)).first()
        
        if user:
            groups = [f'role:{user.role.value}', Authenticated]  # Add Authenticated group
            log.info(f"groupfinder: User '{user.email}' (ID: {userid_str}) found. Groups: {groups}")
            return groups
        else:
            log.warning(f"groupfinder: No user found with id '{userid_str}'")
            return None
            
    except (ValueError, TypeError) as e:
        log.error(f"groupfinder: Failed to process userid '{userid}': {e}")
        return None
    except Exception as e:
        log.error(f"groupfinder: Unexpected error: {e}", exc_info=True)
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

class RootFactory:
    __acl__ = [
        (Allow, Everyone, 'view_public'),  # For public endpoints like facts, breeds etc
        (Allow, Authenticated, ['view_authenticated', 'view_profile']),  # Basic authenticated user permissions
    ]

    def __init__(self, request):
        self.request = request

class AuthenticatedUserFactory(RootFactory):
    """Factory for authenticated user routes"""
    __acl__ = [
        (Allow, Everyone, 'view_public'),  # Inherit public permissions
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