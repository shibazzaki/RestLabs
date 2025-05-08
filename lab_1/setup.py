from setuptools import setup, find_packages

setup(
    name='library_api',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0',
        'marshmallow>=3.0'
    ],
    entry_points={
        'console_scripts': [
            'run-library-api=library_api.app:main'
        ]
    },
)
