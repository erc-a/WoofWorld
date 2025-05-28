def includeme(config):
    # Public Routes
    config.add_route('register', '/api/register')
    config.add_route('login', '/api/login')
    config.add_route('verify_token', '/api/verify-token') # Untuk AuthContext.jsx
    config.add_route('update_profile', '/api/user/profile', request_method='PUT', factory='woofworld_backend.security.AuthenticatedUserFactory')

    config.add_route('list_breeds', '/api/breeds')
    config.add_route('get_breed', '/api/breeds/{id}')
    
    config.add_route('list_facts', '/api/facts') # Sudah ada pagination di view

    # Authenticated Routes (User)
    config.add_route('list_favorites', '/api/favorites', factory='woofworld_backend.security.AuthenticatedUserFactory')
    config.add_route('add_favorite', '/api/favorites', request_method='POST', factory='woofworld_backend.security.AuthenticatedUserFactory')
    config.add_route('remove_favorite', '/api/favorites/{breed_id}', request_method='DELETE', factory='woofworld_backend.security.AuthenticatedUserFactory')


    # Admin Routes
    # Prefix untuk semua rute admin
    admin_prefix = '/api/admin'

    config.add_route('admin_stats', f'{admin_prefix}/stats', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_analytics', f'{admin_prefix}/analytics', factory='woofworld_backend.security.AdminFactory') # Endpoint untuk analytics

    config.add_route('admin_list_users', f'{admin_prefix}/users', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_user', f'{admin_prefix}/users/{{id:\d+}}', request_method='DELETE', factory='woofworld_backend.security.AdminFactory')

    config.add_route('admin_list_breeds', f'{admin_prefix}/breeds', request_method='GET', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_add_breed', f'{admin_prefix}/breeds', request_method='POST', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_get_breed', f'{admin_prefix}/breeds/{{id:\d+}}', request_method='GET', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_update_breed', f'{admin_prefix}/breeds/{{id:\d+}}', request_method='PUT', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_breed', f'{admin_prefix}/breeds/{{id:\d+}}', request_method='DELETE', factory='woofworld_backend.security.AdminFactory')

    config.add_route('admin_list_facts', f'{admin_prefix}/facts', request_method='GET', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_add_fact', f'{admin_prefix}/facts', request_method='POST', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_get_fact', f'{admin_prefix}/facts/{{id:\d+}}', request_method='GET', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_update_fact', f'{admin_prefix}/facts/{{id:\d+}}', request_method='PUT', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_fact', f'{admin_prefix}/facts/{{id:\d+}}', request_method='DELETE', factory='woofworld_backend.security.AdminFactory')
    
    config.add_route('admin_list_videos', f'{admin_prefix}/videos', request_method='GET', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_add_video', f'{admin_prefix}/videos', request_method='POST', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_get_video', f'{admin_prefix}/videos/{{id:\d+}}', request_method='GET', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_update_video', f'{admin_prefix}/videos/{{id:\d+}}', request_method='PUT', factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_video', f'{admin_prefix}/videos/{{id:\d+}}', request_method='DELETE', factory='woofworld_backend.security.AdminFactory')

# Kita tambahkan ACL Factory di security.py