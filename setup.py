from pathlib import Path
from setuptools import setup

setup(
    name='tinyhttp',
    version=(Path(__file__).parent / 'VERSION.text').read_text(),
    license='MIT',
    description='Very fast static file HTTP server using Nim for speed.',
    package_data={'', ['style.css', '*.nim']},
    include_package_data=True,
    install_requires=['nimporter']
)
