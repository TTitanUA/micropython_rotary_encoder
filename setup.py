#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup
import pathlib
import sdist_upip

here = pathlib.Path(__file__).parent.resolve()


# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# load elements of version.py
exec(open(here / 'micropython_rotary_encoder' / 'version.py').read())

setup(
	name="micropython_rotary_encoder",
	version=__version__,
	author="TTitanUA",
	author_email="xttitanx@gmail.com",
	description="This is a micropython raspberry pi pico encoder library.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	license="MIT",
	keywords=["micropython", "raspberry pi pico", "rotary encoder", "EC11", "KY-040"],
	platforms="micropython raspberry pi pico",
	url="https://github.com/TTitanUA/micropython_rotary_encoder",
	packages=[
		"micropython_rotary_encoder",
	],
	classifiers=[
		"Intended Audience :: Developers",
		"Programming Language :: Python :: Implementation :: MicroPython",
		"License :: OSI Approved :: MIT License",
	],
	python_requires='>=3.5',
	cmdclass={'sdist': sdist_upip.sdist},
)