# woofworld_backend/woofworld_backend/tweens.py

from pyramid.settings import aslist

def cors_tween_factory(handler, registry):
    """
    Tween factory to handle CORS and Content Security Policy.
    Takes configuration from settings.ini.
    """
    # Get CORS configuration from settings
    allowed_origins_setting = registry.settings.get('cors.allow_origin', '*')
    allowed_origins = [origin.strip() for origin in allowed_origins_setting.split(',')]
    
    allowed_methods = [method.strip() for method in registry.settings.get(
        'cors.allow_methods', 
        'GET, POST, PUT, DELETE, OPTIONS'
    ).split(',')]
    
    allowed_headers = [header.strip() for header in registry.settings.get(
        'cors.allow_headers',
        'Content-Type, Authorization, X-Requested-With, Origin, Accept'
    ).split(',')]
    
    allow_credentials = registry.settings.get('cors.allow_credentials', 'true').lower() == 'true'
    max_age = registry.settings.get('cors.max_age', '3600')

    def cors_tween(request):
        # Skip CORS handling for internal routes like debug toolbar
        if request.path.startswith('/_debug_toolbar/'):
            return handler(request)

        response = handler(request)
        
        # Add Content Security Policy headers
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.tiktok.com",
            "style-src 'self' 'unsafe-inline' https://www.tiktok.com",
            "frame-src 'self' https://www.tiktok.com",
            "frame-ancestors 'self' https://www.tiktok.com tea-va.bytedance.net",
            "img-src 'self' data: https: blob:",
            "media-src 'self' https://www.tiktok.com",
            "connect-src 'self' https://www.tiktok.com"
        ]
        response.headers['Content-Security-Policy'] = "; ".join(csp_directives)

        response_origin = None
        request_origin = request.headers.get('Origin')

        if request_origin:
            if '*' in allowed_origins:
                response_origin = request_origin  # Return actual origin when using wildcard
            elif request_origin in allowed_origins:
                response_origin = request_origin
            # For local development with different ports
            elif any(request_origin.startswith('http://localhost:') for _ in allowed_origins):
                response_origin = request_origin

        # Handle preflight requests
        if request.method == 'OPTIONS':
            response.status_int = 200
            
        if response_origin:
            response.headers['Access-Control-Allow-Origin'] = response_origin
            response.headers['Access-Control-Allow-Methods'] = ', '.join(allowed_methods)
            response.headers['Access-Control-Allow-Headers'] = ', '.join(allowed_headers)
            if allow_credentials:
                response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = max_age

        return response

    return cors_tween

def includeme(config):
    """Add the CORS tween to the pyramid configuration.
    
    The tween is added over the exception view tween factory to ensure
    CORS headers are added even to error responses.
    """
    config.add_tween('woofworld_backend.tweens.cors_tween_factory', 
                     over='pyramid.tweens.excview_tween_factory')