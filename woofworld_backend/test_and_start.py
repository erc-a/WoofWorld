import os
print("Current working directory:", os.getcwd())
print("Python executable:", os.sys.executable)

# Check if we're in the right directory
backend_path = r"C:\Project\Pemograman Web\WoofWorld\woofworld_backend"
if os.path.exists(backend_path):
    os.chdir(backend_path)
    print("Changed to backend directory:", os.getcwd())
    
    # Check if development.ini exists
    if os.path.exists("development.ini"):
        print("✓ development.ini found")
    else:
        print("✗ development.ini not found")
        
    # Check if woofworld_backend directory exists
    if os.path.exists("woofworld_backend"):
        print("✓ woofworld_backend package found")
    else:
        print("✗ woofworld_backend package not found")
        
    # Try to import the module
    try:
        import sys
        sys.path.insert(0, '.')
        from woofworld_backend import main
        print("✓ Successfully imported woofworld_backend.main")
        
        # Read development.ini to get settings
        from pyramid.paster import get_app
        try:
            app = get_app('development.ini', 'main')
            print("✓ Successfully created WSGI app from development.ini")
            
            # Start with waitress
            from waitress import serve
            print("🚀 Starting server on localhost:6544...")
            print("📡 CORS enabled for 127.0.0.1:5500 and localhost:5500")
            print("🔧 Debug mode enabled - check console for CORS logs")
            serve(app, host='0.0.0.0', port=6544)
            
        except Exception as e:
            print(f"✗ Error creating app from development.ini: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"✗ Error importing woofworld_backend: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"✗ Backend path not found: {backend_path}")
