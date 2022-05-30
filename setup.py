#!/usr/local/bin/python3.4

"""
## Copyright (c) 2022 INSPIRE5G-Plus [, ANY ADDITIONAL AFFILIATION]
## ALL RIGHTS RESERVED.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Neither the name of the INSPIRE5G-Plus [, ANY ADDITIONAL AFFILIATION]
## nor the names of its contributors may be used to endorse or promote
## products derived from this software without specific prior written
## permission.
##
## This work has been performed in the framework of the INSPIRE5G-Plus project,
## funded by the European Commission under Grant number 871808 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.inspire-5gplus.eu/).
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='e2e_slice_mngr',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='v0.1',

    description='INSPIRE5G-Plus E2E Network Slice manager',
    long_description='INSPIRE5G-Plus E2E Network Slice manager',

    # The project's main homepage.
    url='https://github.com/INSPIRE-5Gplus/i5p-wp3-netslice4ssla',

    # Author details
    author='Pol Alemany',
    author_email='palemany@cttc.es',

    # Choose your license
    license='Apache 2.0',

    # What does your project relate to?
    keywords='Network Slicing NFV orchestrator',

    packages=find_packages(),
    install_requires=['Flask>=2.0.2', 'flask-restful', 'python-dateutil', 'requests', 'xmlrunner', 'pika', 'coloredlogs'],
)