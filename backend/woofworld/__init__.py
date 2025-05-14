from pyramid.config import Configurator
from pyramid.response import Response

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:5173',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Expose-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        })
    event.request.add_response_callback(cors_headers)

def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # CORS configuration
    config.add_subscriber(add_cors_headers_response_callback, 'pyramid.events.NewRequest')
    
    # Handle OPTIONS requests
    def options_view(request):
        response = Response()
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:5173',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Max-Age': '3600'
        })
        return response

    config.add_route('cors', '{catch_all:.*}', request_method='OPTIONS')
    config.add_view(options_view, route_name='cors')
    
    # Include packages
    config.include('.models')
    config.include('.routes')
    
    config.scan('.views')
    return config.make_wsgi_app()