from pyramid.view import view_config
from pyramid.response import Response
import json

def includeme(config):
    # Public Routes
    config.add_route('home', '/')
    config.add_route('register', '/api/register')
    config.add_route('login', '/api/login')
    config.add_route('verify_token', '/api/verify-token', factory='woofworld_backend.security.AuthenticatedUserFactory')
    config.add_route('update_profile', '/api/user/profile', request_method='PUT', 
                     factory='woofworld_backend.security.AuthenticatedUserFactory')

    # Breed Routes
    config.add_route('list_breeds', '/api/breeds')
    config.add_route('get_breed', '/api/breeds/{id}')
    
    # Facts Routes
    config.add_route('list_facts', '/api/facts')

    # Public Videos and Popular Breeds
    config.add_route('list_public_videos', '/api/videos', request_method='GET')
    config.add_route('list_popular_breeds', '/api/popular-breeds', request_method='GET')

    # Authenticated Routes (User)
    config.add_route('list_favorites', '/api/favorites', 
                     factory='woofworld_backend.security.AuthenticatedUserFactory')
    config.add_route('add_favorite', '/api/favorites', request_method='POST', 
                     factory='woofworld_backend.security.AuthenticatedUserFactory')
    config.add_route('remove_favorite', '/api/favorites/{breed_id}', request_method='DELETE', 
                     factory='woofworld_backend.security.AuthenticatedUserFactory')

    # Admin Routes
    admin_prefix = '/api/admin'
    
    # Admin Stats & Analytics
    config.add_route('admin_stats', f'{admin_prefix}/stats', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_analytics', f'{admin_prefix}/analytics', 
                     factory='woofworld_backend.security.AdminFactory')

    # Admin User Management
    config.add_route('admin_list_users', f'{admin_prefix}/users', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_user', f'{admin_prefix}/users/{{id:\\d+}}', 
                     request_method='DELETE', factory='woofworld_backend.security.AdminFactory')
    config.add_route('make_admin', f'{admin_prefix}/users/make-admin', request_method='POST', 
                     factory='woofworld_backend.security.AdminFactory')

    # Admin Breed Management
    config.add_route('admin_list_breeds', f'{admin_prefix}/breeds', request_method='GET', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_add_breed', f'{admin_prefix}/breeds', request_method='POST', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_get_breed', f'{admin_prefix}/breeds/{{id:\\d+}}', request_method='GET', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_update_breed', f'{admin_prefix}/breeds/{{id:\\d+}}', request_method='PUT', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_breed', f'{admin_prefix}/breeds/{{id:\\d+}}', request_method='DELETE', 
                     factory='woofworld_backend.security.AdminFactory')

    # Admin Fact Management
    config.add_route('admin_list_facts', f'{admin_prefix}/facts', request_method='GET', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_add_fact', f'{admin_prefix}/facts', request_method='POST', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_get_fact', f'{admin_prefix}/facts/{{id:\\d+}}', request_method='GET', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_update_fact', f'{admin_prefix}/facts/{{id:\\d+}}', request_method='PUT', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_fact', f'{admin_prefix}/facts/{{id:\\d+}}', request_method='DELETE', 
                     factory='woofworld_backend.security.AdminFactory')
    
    # Admin Video Management
    config.add_route('admin_list_videos', f'{admin_prefix}/videos', request_method='GET', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_add_video', f'{admin_prefix}/videos', request_method='POST', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_get_video', f'{admin_prefix}/videos/{{id:\\d+}}', request_method='GET', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_update_video', f'{admin_prefix}/videos/{{id:\\d+}}', request_method='PUT', 
                     factory='woofworld_backend.security.AdminFactory')
    config.add_route('admin_delete_video', f'{admin_prefix}/videos/{{id:\\d+}}', request_method='DELETE', 
                     factory='woofworld_backend.security.AdminFactory')