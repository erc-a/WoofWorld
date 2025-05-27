# woofworld_backend/setup.py

from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'alembic',
    'psycopg2-binary',
    'pyramid_jwt',
    'passlib[bcrypt]',
    'requests'
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'pytest-cov',
]

setup(
    name='woofworld_backend',
    version='0.1',
    description='WoofWorld Backend API',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = woofworld_backend:main',
        ],
        'console_scripts': [
            'initialize_woofworld_db = woofworld_backend.scripts.initializedb:main',
        ],
    },
)