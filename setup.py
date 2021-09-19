from distutils.core import setup
setup(name='lut4brian',
	version='0.1',
	packages=['lut4brian'],
	package_dir={'lut4brian': 'lut4brian'},
	description='LookUp Table acceleration for Brian2 stimulator',
	requires=['brian2'],
	author='Ruben Tikidji-Hamburyan',
	author_email='rth@r-a-r.org',
	url='https://github.com/rat-h/lut4brian',
	licence="licence.txt"
)

