from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'psycopg2',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_retry',
    'pyramid_default_cors',
    'alembic',
    'PyJWT',
    'passlib[bcrypt]',
    'pyramid_default_cors'
]

setup(
    name='woofworld',
    version='0.0',
    description='WoofWorld Backend',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = woofworld:main',
        ],
    },
)