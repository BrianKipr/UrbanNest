from setuptools import setup, find_packages

setup(
    name='ecommerce-backend',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-JWT-Extended',
        'Marshmallow'
    ],
)
