from setuptools import setup, find_packages

setup(
    name='library_api',
    version='0.5.0',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.85.0',
        'uvicorn[standard]>=0.18.0',
        'motor>=3.1.1',
        'pydantic-mongo>=0.1.0'
        'python-jose[cryptography]>=3.3.0',
        'passlib[bcrypt]>=1.7.4',
    ],
    entry_points={
        'console_scripts': [
            'run-library-api=library_api.main:main'
        ]
    },
)
