"""A setuptools based setup module."""
from os import path
from io import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='broiestbot',
    version='1.0.0',
    description='Chatbot for the Chatango messaging platform.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/toddbirchard/broiestbot',
    author='Todd Birchard',
    author_email='toddbirchard@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='Chatbot Chatango Chat Bot Ch.py',
    packages=find_packages(),
    install_requires=['Pandas',
                      'Requests',
                      'SQLAlchemy',
                      'BS4',
                      'Google-cloud-storage',
                      'PyMySQL',
                      'Loguru',
                      'Plotly',
                      'psutil'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
        'env': ['python-dotenv']
    },
    entry_points={
        'console_scripts': [
            'run=main:init_bot',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/toddbirchard/broiestbot/issues',
        'Source': 'https://github.com/toddbirchard/broiestbot/',
    },
)
