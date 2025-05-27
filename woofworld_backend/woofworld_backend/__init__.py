# woofworld_backend/woofworld_backend/__init__.py

from pyramid.config import Configurator
# Pastikan security.py dan groupfinder sudah ada dan benar
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder 


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Include pyramid_jwt for authentication
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy(
        settings['jwt.secret'],
        auth_type=settings.get('jwt.auth_policy', 'Bearer'),
        expiration=int(settings.get('jwt.expiration', 3600)),
        algorithm=settings.get('jwt.algorithm', 'HS256'),
        callback=groupfinder 
    )

    config.set_authorization_policy(ACLAuthorizationPolicy())
    
    # Include pyramid_tm
    config.include('pyramid_tm')

    # HAPUS atau KOMENTARI baris ini:
    # config.include('pyramid_defaultcors') 
    # config.add_cors_preflight_handler() # Ini juga tidak diperlukan lagi jika pakai tween manual

    # TAMBAHKAN baris ini untuk mengaktifkan tween CORS manual kita:
    config.include('.tweens') 

    # Models and database setup
    config.include('.models')
    
    # Routes
    config.include('.routes')

    config.scan()
    return config.make_wsgi_app()