from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import Allow, Everyone

class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'admin', 'admin'),
    ]

    def __init__(self, request):
        pass

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Include other packages
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')

    # Security policies
    config.set_authentication_policy(AuthTktAuthenticationPolicy('seekrit'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_root_factory(RootFactory)

    # Include models and database setup
    config.include('.models')

    # Include CORS configuration
    config.include('pyramid_default_cors')
    config.add_cors_preflight_handler()

    # Include routes
    config.include('.routes')

    config.scan()
    return config.make_wsgi_app()