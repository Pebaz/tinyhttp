from pathlib import Path
from setuptools import setup

setup(
    name='tinyhttp',
    author='http://github.com/Pebaz',
    version=(Path(__file__).parent / 'tinyhttp/VERSION.txt').read_text(),
    license='MIT',
    description='Very fast static file HTTP server using Nim for speed.',
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
