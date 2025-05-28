from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder, RootFactory
import logging # Tambahkan ini
log = logging.getLogger(__name__) # Tambahkan ini

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Log nilai JWT settings yang penting
    log.info("============================================================")
    log.info(f"INISIASI APLIKASI: Nilai jwt.secret dari settings: '{settings.get('jwt.secret')}'")
    log.info(f"INISIASI APLIKASI: Nilai jwt.algorithm dari settings: '{settings.get('jwt.algorithm', 'HS256')}'") # Default HS256 jika tidak ada
    log.info(f"INISIASI APLIKASI: Nilai jwt.expiration dari settings: '{settings.get('jwt.expiration')}'")
    log.info("============================================================")

    config = Configurator(settings=settings, root_factory=RootFactory)

    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy(
                settings['jwt.secret'], # Pastikan ini menggunakan nilai yang benar-benar dari settings
        auth_type=settings.get('jwt.auth_policy', 'Bearer'),
        expiration=int(settings.get('jwt.expiration', 3600)), # Pastikan konversi int berhasil
        algorithm=settings.get('jwt.algorithm', 'HS256'),
        callback=groupfinder
    )

    config.set_authorization_policy(ACLAuthorizationPolicy())

    config.include('pyramid_tm')
    config.include('.tweens')
    config.include('.models')
    config.include('.routes')

    config.scan('.views')

    return config.make_wsgi_app()

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)