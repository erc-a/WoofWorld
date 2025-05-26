def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    # Auth routes
    config.add_route('login', '/api/login')
    config.add_route('register', '/api/register')
    
    # Admin routes
    config.add_route('admin_stats', '/api/admin/stats')
    config.add_route('admin_users', '/api/admin/users')
    config.add_route('admin_user', '/api/admin/users/{id}')
    config.add_route('admin_breeds', '/api/admin/breeds')
    config.add_route('admin_breed', '/api/admin/breeds/{id}')
    config.add_route('admin_facts', '/api/admin/facts')
    config.add_route('admin_fact', '/api/admin/facts/{id}')
    config.add_route('admin_videos', '/api/admin/videos')
    config.add_route('admin_video', '/api/admin/videos/{id}')