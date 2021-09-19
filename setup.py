
from distutils.core import setup

README = """
LookUp Table approximator for `Brian2 simulator`_
=================================================

.. _Brian2 simulator: https://briansimulator.org/

What is Brian?
--------------
Brian is a free, open source simulator for spiking neural networks. It is written in the Python programming language and is available on almost all platforms. We believe that a simulator should not only save the time of processors, but also the time of scientists. Brian is therefore designed to be easy to learn and use, highly flexible and easily extensible.

What is Lookup table approximation?
-----------------------------------
The lookup-table approximation is a classical method for computation acceleration in a numerical problem, known for centuries. 
It is extensively used in such software as NEURON and GENESIS, but I kind of miss it in Brian. 
This approximation is based on a straightforward algorithm: 
First, before simulation, one needs to precompute lookup tables for values of $m_\infty(v)$, $h_\infty(v)$, and so on in a full range of voltages. 
Usually, this range goes between the lowest possible to the highest possible voltages.
The range is divided into intervals with constant steps.
For example, this may be a range from −100 to 60 mV with 1 mV step. 
With precomputed tables, one solves differential equations using linear interpolation between table rows instead of computing exponential functions. 
The voltage at a current time moment of a numerical solution is used to find indices of two rows in the lookup table closest to the membrane voltage.
Using these two indices, one can query values for all steady-states and time constants of gating variables and linearly interpolate between
these values - like this:
.. image:: images/SP-Figure1.jpg

How to install?
---------------

pip install lutbrain

An Example
----------


See an example and explanations on the `GitHub`_

.. _GitHub: https://github.com/rat-h/lut4brian



"""
setup(name='lut4brian',
	version='0.1.0',
	packages=['lut4brian'],
	package_dir={'lut4brian': 'lut4brian'},
	description='LookUp Table acceleration for Brian2 stimulator',
	requires=['brian2'],
	long_description=README,
	long_description_content_type="text/x-rst",
	author='Ruben Tikidji-Hamburyan',
	author_email='rth@r-a-r.org',
	url='https://github.com/rat-h/lut4brian',
	licence="GPL2"
)

