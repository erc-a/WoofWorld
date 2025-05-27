import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.user import User, UserRole


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.drop_all(engine) # Hapus tabel lama jika ada (hati-hati di production)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        # Buat admin user awal
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@woofworld.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        admin_user = User(name='Admin User', email=admin_email, role=UserRole.admin)
        admin_user.set_password(admin_password) # Gunakan method dari model
        dbsession.add(admin_user)
        
        print(f"Admin user created: {admin_email} / {admin_password}")

        # Tambahkan data dummy jika perlu untuk development
        # Contoh:
        # fact1 = Fact(content="Anjing Dalmation lahir tanpa bintik.")
        # dbsession.add(fact1)