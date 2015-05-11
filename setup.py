try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A hangman game',
    'author': 'Raul Ascencio',
    'url': 'http://destruction.io/hangman',
    'download_url': 'http://destruction.io/hangman/hangman.zip.',
    'author_email': 'r@destruction.io.',
    'version': '0.1',
    'install_requires': ['pytest', 'ncurses', 'urwid'],
    'packages': ['hangman'],
    'scripts': [],
    'name': 'hangman'

}

setup(**config)
