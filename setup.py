import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README-pypi.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-encrypted-secrets',
    version='0.9.9',
    packages=find_packages(),
    author='Axiomatic LLC',
    author_email='contact@axiomatic.im',
    include_package_data=True,
    license='MIT License',  # example license
    description='A Django app for managing secrets.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/nzaillian/django-encrypted-secrets',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=[
        'PyCryptodome',
        'PyYAML'
    ],
)
