from setuptools import setup

APP=['helloworld.py']
OPTIONS = {
	'argv_emulation': True,
}

def for_mac(build_number,name):
	setup(
		name=name,
		version=build_number,
		app=APP,
		options={'py2app': OPTIONS},
		setup_requires=['py2app']
	)
