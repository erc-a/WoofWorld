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
    config = Configurator(settings=settings)
    
    # Include packages
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')
    
    # Security policies
    config.set_authentication_policy(AuthTktAuthenticationPolicy('seekrit'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_root_factory(RootFactory)
    
    # Database
    config.include('.models')
    
    # Routes
    config.include('.routes')
    
    # CORS
    config.add_cors_preflight_handler()
    config.add_route('cors', '/{catch_all:.*}')
    
    config.scan()
    return config.make_wsgi_app()