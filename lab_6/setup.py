from setuptools import setup, find_packages

setup(
    name='library_api',
    version='0.6.0',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0',
        'Flask-RESTful>=0.3.9',
        'marshmallow>=3.0',
        'flasgger>=0.9.5'
    ],
    entry_points={
        'console_scripts': [
            'run-library-api=library_api.app:main'
        ]
    },
)
