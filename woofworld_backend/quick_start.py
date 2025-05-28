import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Test if we can import the application
try:
    from woofworld_backend import main
    print("✓ Successfully imported main function")
    
    # Test basic configuration
    settings = {
        'jwt.secret': 'development_secret_key_change_in_production',
        'jwt.algorithm': 'HS256', 
        'jwt.expiration': '3600',
        'sqlalchemy.url': 'sqlite:///woofworld.sqlite',
        'cors.allow_origin': '*, http://localhost:5173, http://127.0.0.1:5500, http://localhost:5500',
        'cors.allow_methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'cors.allow_headers': 'Content-Type, Authorization, X-Requested-With, Accept',
        'cors.allow_credentials': 'true',
        'cors.max_age': '3600'
    }
    
    print("✓ Configuration prepared")
    
    # Try to create the app
    app = main({}, **settings)
    print("✓ WSGI application created successfully")
    
    # Try to start with waitress
    from waitress import serve
    print("Starting server on http://localhost:6544 with CORS debugging enabled...")
    print("CORS will allow origins from 127.0.0.1:5500 and localhost:5500")
    serve(app, host='0.0.0.0', port=6544)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
