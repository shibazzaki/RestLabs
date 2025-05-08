from setuptools import setup, find_packages

setup(
    name='library_api',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0',
        'Flask-SQLAlchemy>=3.0',
        'marshmallow>=3.0',
        'marshmallow-sqlalchemy>=0.28',
        'psycopg2-binary>=2.9'
    ],
    entry_points={
        'console_scripts': [
            'run-library-api=library_api.app:main'
        ]
    },
)
