import os
import sys
import transaction
from pyramid.paster import bootstrap, setup_logging
from ..models import User
from ..models.user import UserRole

def main(argv=sys.argv):
    if len(argv) < 3:
        print("Usage: make_admin development.ini user@email.com")
        return 1
        
    config_uri = argv[1]
    email = argv[2]
    
    setup_logging(config_uri)
    env = bootstrap(config_uri)
    
    try:
        with transaction.manager:
            request = env['request']
            dbsession = request.dbsession
            
            user = dbsession.query(User).filter_by(email=email).first()
            if not user:
                print(f"No user found with email {email}")
                return 2
                
            user.role = UserRole.admin
            dbsession.add(user)
            print(f"Successfully made user {user.email} an admin")
            
    except Exception as e:
        print(f"Failed to make user admin: {e}")
        return 1
    finally:
        env['closer']()
    
    return 0

if __name__ == '__main__':
    sys.exit(main() or 0)