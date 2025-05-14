from setuptools import setup, find_packages

requires = [
    'pyramid',
    'waitress',
    'sqlalchemy',
    'alembic',
    'psycopg2',
    'pyramid_tm',
    'zope.sqlalchemy',
    'transaction',
    'pyramid_retry',
    'PyJWT',
    'passlib[bcrypt]',  # Add this line
]

setup(
    name='woofworld',
    version='0.0',
    description='WoofWorld Backend',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = woofworld:main',
        ],
    },
)