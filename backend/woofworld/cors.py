from pyramid.security import NO_PERMISSION_REQUIRED

def includeme(config):
    config.add_directive(
        'add_cors_preflight_handler', add_cors_preflight_handler)
    config.add_route_predicate('cors_preflight', CorsPreflightPredicate)
    
    config.add_subscriber(add_cors_to_response, 'pyramid.events.NewResponse')

class CorsPreflightPredicate:
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'cors_preflight = %s' % bool(self.val)

    phash = text

    def __call__(self, context, request):
        if not self.val:
            return False
        return (
            request.method == 'OPTIONS' and
            'Origin' in request.headers and
            'Access-Control-Request-Method' in request.headers
        )

def add_cors_preflight_handler(config):
    config.add_route(
        'cors-options-preflight', '/{catch_all:.*}',
        cors_preflight=True,
    )
    config.add_view(
        handle_cors_preflight,
        route_name='cors-options-preflight',
        permission=NO_PERMISSION_REQUIRED,
    )

def handle_cors_preflight(context, request):
    response = request.response
    if 'Access-Control-Request-Headers' in request.headers:
        response.headers['Access-Control-Allow-Headers'] = (
            request.headers['Access-Control-Request-Headers'])
    
    response.headers.update({
        'Access-Control-Allow-Origin': request.headers.get('Origin', ''),
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Max-Age': '3600',
    })
    return response

def add_cors_to_response(event):
    request = event.request
    response = event.response
    if 'Origin' in request.headers:
        response.headers.update({
            'Access-Control-Allow-Origin': request.headers['Origin'],
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Expose-Headers': 'Content-Type',
        })