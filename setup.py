"""
Usage:
	pip install tinyhttp

Upload to PyPi:
	python3 setup.py sdist
	twine upload dist/<tinyhttp artifact>

Please note: In order to use Nimporter, you must have both Nim installed as well
as the [Nimpy](https://github.com/yglukhov/Nimpy) library.
Make sure to star it on GitHub as well while you're up there. ;)
"""

from pathlib import Path
from setuptools import setup

setup(
    name='tinyhttp',
    author='http://github.com/Pebaz',
    url='http://github.com/Pebaz/tinyhttp',
    version=(Path(__file__).parent / 'tinyhttp/VERSION.txt').read_text(),
    license='MIT',
    description='Very fast static file HTTP server using Nim for speed.',
    long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
    packages=['tinyhttp'],
    package_data={
        'tinyhttp' : ['*.txt', '*.css', '*.nim'],
    },
    include_package_data=True,
    install_requires=['nimporter'],
    entry_points={
		'console_scripts' : [
			'tinyhttp=tinyhttp.mod:main'
		]
	}
)
