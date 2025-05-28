# woofworld_backend/woofworld_backend/__init__.py

from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder, RootFactory # <--- IMPORT RootFactory DI SINI

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory) # <--- SET RootFactory DI SINI

    # Include pyramid_jwt for authentication
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy(
        settings['jwt.secret'],
        auth_type=settings.get('jwt.auth_policy', 'Bearer'),
        expiration=int(settings.get('jwt.expiration', 3600)),
        algorithm=settings.get('jwt.algorithm', 'HS256'),
        callback=groupfinder 
    )

    config.set_authorization_policy(ACLAuthorizationPolicy()) # Pastikan ini sudah tidak dikomentari
    
    config.include('pyramid_tm')
    config.include('.tweens') 
    config.include('.models')
    config.include('.routes')
    
    # Scan all views at once
    config.scan('.views')  
    
    return config.make_wsgi_app()

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)