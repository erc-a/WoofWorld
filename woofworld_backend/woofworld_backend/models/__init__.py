# woofworld_backend/models/__init__.py

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy # Impor zope.sqlalchemy tetap dibutuhkan untuk register

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .user import User, UserRole # Impor User dan UserRole langsung dari models.user
# from ..security import get_user, hash_password, check_password 

# from .breed import DogBreed # noqa # Pastikan ini sudah dikomentari/dihapus jika breed dari API
from .fact import Fact # noqa
from .favorite import Favorite # noqa
from .video import Video # noqa
from .meta import Base # Impor Base untuk digunakan di bawah (jika perlu, tapi biasanya tidak di sini)


# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager, **kwargs):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - Wires up a session count scheme
    - Hooks the session to the transaction manager
    - Injects the session into the request as request.dbsession
    """
    dbsession = session_factory(**kwargs)
    zope.sqlalchemy.register( # Ini adalah penggunaan utama zope.sqlalchemy
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('woofworld_backend.models')``.

    """
    settings = config.get_settings()
    # Pastikan tm.manager_hook diset jika menggunakan pyramid_tm secara eksplisit
    # Biasanya ini sudah dihandle oleh pyramid_tm jika di-include di __init__.py utama
    if 'tm.manager_hook' not in settings:
        settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    # Ini seharusnya sudah di-include di __init__.py utama aplikasi.
    # Jika belum, bisa ditambahkan di sini atau (lebih baik) di __init__.py utama.
    # config.include('pyramid_tm')

    # HAPUS BARIS INI:
    # config.include('zope.sqlalchemy')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )