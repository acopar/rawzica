# coding: utf-8

import os
import sys
from shutil import copy

from setuptools import setup, find_packages
from rawzica import __version__


setup(
    name='rawzica',
    py_modules=['rawzica'],
    version=__version__,
    install_requires=(
    ),
    entry_points={
    },
    data_files=(
        ('/etc/cron.daily/', ['rawzica']),
        ('/etc/', ['rawzica.conf']),
    ),
)
ETC_FILE = 'rawzica.conf'
if not os.path.exists('/etc/' + ETC_FILE):
    copy(os.path.join(__file__, ETC_FILE), '/etc/')

setup_path = os.path.dirname(__file__)
copy(os.path.join(setup_path, 'rawzica.py'), '/usr/local/bin/rawzica')
