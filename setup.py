"""A setuptools based setup module."""
from os import path
from setuptools import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='acleebot',
    version='0.0.1',
    description='Chatbot for the Chatango messaging platform.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/toddbirchard/acleebot',
    author='Todd Birchard',
    author_email='toddbirchard@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Chat Chatbot Chatango Ch.py',
    packages=find_packages(),
    install_requires=['Pandas',
                      'Requests',
                      'Flask',
                      'nba-py',
                      'SQLAlchemy',
                      'BS4',
                      'Google-cloud-storage',
                      'Psycopg2-Binary'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
        'env': ['python-dotenv']
    },
    entry_points={
        'console_scripts': [
            'main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/toddbirchard/aclee/issues',
        'Source': 'https://github.com/toddbirchard/acleebot/',
    },
)
