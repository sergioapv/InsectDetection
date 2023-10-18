from setuptools import setup, find_packages

setup(
    name='example',
    version='0.1.0',
    description='Setting up a python package',
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        'ultralytics',  # Include only if this is a genuine requirement
        'fastapi',  # Include only if this is a genuine requirement
        'requests',  # Include only if this is a genuine requirement
        'numpy',  # Include only if this is a genuine requirement
        'django',  # Include only if this is a genuine requirement
        'uvicorn[standard]',
        'datetime',
    ],
)
