#!/usr/bin/env python
import os
import sys
import transaction
from pyramid.paster import bootstrap, setup_logging
from woofworld_backend.models import User
from woofworld_backend.models.user import UserRole

def create_admin():
    print("Starting admin creation script...")
    config_uri = 'development.ini'
    print(f"Using config: {config_uri}")
    
    setup_logging(config_uri)
    print("Logging setup complete")
    
    env = bootstrap(config_uri)
    print("Bootstrap complete")
    
    try:
        print("Starting transaction...")
        with transaction.manager:
            request = env['request']
            dbsession = request.dbsession
            print("Database session obtained")
            
            # Check if admin@test.com exists
            print("Querying for existing user...")
            user = dbsession.query(User).filter_by(email='admin@test.com').first()
            if user:
                print(f"User {user.email} found. Current role: {user.role}")
                print(f"UserRole.admin enum value: {UserRole.admin}")
                print(f"UserRole.admin enum name: {UserRole.admin.name}")
                user.role = UserRole.admin
                dbsession.add(user)
                dbsession.flush()  # Flush to persist changes
                # Verify the change
                updated_user = dbsession.query(User).filter_by(email='admin@test.com').first()
                print(f"After update - User role: {updated_user.role}")
                print(f"Successfully updated user {user.email} to admin role")
            else:
                print("User not found, creating new admin user")
                new_admin = User(name='Admin User', email='admin@test.com')
                new_admin.set_password('admin123')
                new_admin.role = UserRole.admin
                dbsession.add(new_admin)
                dbsession.flush()
                print(f"Successfully created admin user with ID: {new_admin.id}")
                
    except Exception as e:
        print(f"Failed to create/update admin: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        env['closer']()
    
    return 0

if __name__ == '__main__':
    sys.exit(create_admin())
