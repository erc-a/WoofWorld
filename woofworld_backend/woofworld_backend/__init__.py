from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder, RootFactory # <--- IMPORT RootFactory DI SINI

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory)    # Include pyramid_jwt BEFORE setting authentication policy
    config.include('pyramid_jwt')
    
    # Get JWT settings
    jwt_secret = settings['jwt.secret']
    jwt_algorithm = settings.get('jwt.algorithm', 'HS256')
    jwt_expiration = int(settings.get('jwt.expiration', 3600))
    jwt_auth_type = settings.get('jwt.auth_type', 'Bearer')
    
    # Configure JWT authentication with explicit settings
    config.set_jwt_authentication_policy(
        jwt_secret,
        auth_type=jwt_auth_type,
        algorithm=jwt_algorithm,
        callback=groupfinder,
        json_encoder=None,
        expiration=jwt_expiration
    )

    # Set authorization policy
    config.set_authorization_policy(ACLAuthorizationPolicy())

    # Include other components
    config.include('pyramid_tm')
    config.include('.tweens')
    config.include('.models')
    config.include('.routes')
    
    # Scan all views
    config.scan('.views')

    return config.make_wsgi_app()

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)