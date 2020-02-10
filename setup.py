from pathlib import Path
from setuptools import setup

setup(
    name='tinyhttp',
    author='http://github.com/Pebaz',
    version=(Path(__file__).parent / 'VERSION.txt').read_text(),
    license='MIT',
    description='Very fast static file HTTP server using Nim for speed.',
    py_modules=['mod'],
    package_data={'' : ['*.css', '*.nim']},
    include_package_data=True,
    install_requires=['nimporter'],
    entry_points={
		'console_scripts' : [
			'tinyhttp=mod:main'
		]
	}
)
