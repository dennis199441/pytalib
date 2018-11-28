from setuptools import setup, find_packages

setup(
	name='pytalib',
	packages=find_packages(),
	description='Python Technical Analysis Library',
	version='0.0.1',
	url='https://github.com/dennis199441/pytalib',
	author='Dennis Cheung',
	author_email='dennis199441@gmail.com',
	install_requires=[
		'networkx',
		'scipy',
    ],
	keywords=['pip','dennis','pytalib']
)