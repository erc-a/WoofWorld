# woofworld_backend/woofworld_backend/tweens.py

from pyramid.settings import aslist

def cors_tween_factory(handler, registry):
    """
    Tween factory to handle CORS and Content Security Policy.
    Takes configuration from settings.ini.
    """
    # Get CORS configuration from settings
    allowed_origins_setting = registry.settings.get('cors.allow_origin', 'http://localhost:5173')
    allowed_origins = [origin.strip() for origin in allowed_origins_setting.split(',')]
    
    allowed_methods = [method.strip() for method in registry.settings.get(
        'cors.allow_methods', 
        'GET, POST, PUT, DELETE, OPTIONS'
    ).split(',')]
    
    allowed_headers = [header.strip() for header in registry.settings.get(
        'cors.allow_headers',
        'Content-Type, Authorization, X-Requested-With, Origin, Accept, Cache-Control, X-CSRF-Token'
    ).split(',')]
    
    allow_credentials = True  # Always allow credentials for this app
    max_age = registry.settings.get('cors.max_age', '3600')

    def cors_tween(request):
        # Skip CORS handling for internal routes like debug toolbar
        if request.path.startswith('/_debug_toolbar/'):
            return handler(request)

        # Always set CORS headers, even for errors
        request_origin = request.headers.get('Origin')
        print(f"CORS DEBUG: Processing request {request.method} {request.path}")
        print(f"CORS DEBUG: Request origin: {request_origin}")
        
        # Handle preflight requests first
        if request.method == 'OPTIONS':
            print("CORS DEBUG: Handling OPTIONS preflight request")
            response = request.response
            response.status_int = 200
        else:
            try:
                response = handler(request)
                print(f"CORS DEBUG: Handler completed with status: {response.status_int}")
            except Exception as e:
                print(f"CORS DEBUG: Handler exception: {e}")
                # Create an error response but still apply CORS
                response = request.response
                response.status_int = 500
                response.json_body = {'error': 'Internal server error'}
        
        # Add Content Security Policy headers
        try:
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
        except Exception as e:
            print(f"CORS DEBUG: Error setting CSP: {e}")
        
        # Handle CORS headers - ALWAYS apply them
        response_origin = None

        if request_origin:
            print(f"CORS DEBUG: Request origin: {request_origin}")
            print(f"CORS DEBUG: Allowed origins: {allowed_origins}")
            
            if '*' in allowed_origins:
                response_origin = request_origin  # Return actual origin when using wildcard
                print(f"CORS DEBUG: Using wildcard, setting response origin to: {response_origin}")
            elif request_origin in allowed_origins:
                response_origin = request_origin
                print(f"CORS DEBUG: Origin found in allowed list, setting response origin to: {response_origin}")
            # For local development with different ports and 127.0.0.1
            elif (request_origin.startswith('http://localhost:') or 
                  request_origin.startswith('http://127.0.0.1:')):
                response_origin = request_origin
                print(f"CORS DEBUG: Local development origin, setting response origin to: {response_origin}")
            else:
                print(f"CORS DEBUG: Origin not allowed: {request_origin}")
        else:
            print("CORS DEBUG: No origin header found")
            
        # ALWAYS set CORS headers if we have a valid origin
        if response_origin:
            try:
                response.headers['Access-Control-Allow-Origin'] = response_origin
                response.headers['Access-Control-Allow-Methods'] = ', '.join(allowed_methods)
                response.headers['Access-Control-Allow-Headers'] = ', '.join(allowed_headers)
                if allow_credentials:
                    response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Max-Age'] = max_age
                print(f"CORS DEBUG: Successfully set CORS headers for origin: {response_origin}")
            except Exception as e:
                print(f"CORS DEBUG: Error setting CORS headers: {e}")
        else:
            print("CORS DEBUG: No CORS headers set - no valid origin")

        print(f"CORS DEBUG: Final response headers: {dict(response.headers)}")
        return response

    return cors_tween

def includeme(config):
    """Add the CORS tween to the pyramid configuration.
    
    The tween is added over the exception view tween factory to ensure
    CORS headers are added even to error responses.
    """
    config.add_tween('woofworld_backend.tweens.cors_tween_factory', 
                     over='pyramid.tweens.excview_tween_factory')
