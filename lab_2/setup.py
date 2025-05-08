from setuptools import setup, find_packages

setup(
    name='library_api_fast',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.85.0',
        'uvicorn[standard]>=0.18.0'
    ],
    entry_points={
        'console_scripts': [
            # після інсталяції: run-library-api
            'run-library-api=library_api.main:main'
        ]
    },
)
