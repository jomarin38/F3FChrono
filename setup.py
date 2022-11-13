#
# This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
# Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import setuptools
from F3FChrono.Utils import is_running_on_pi

with open("README.md", "r") as fh:

    long_description = fh.read()

install_requires = [
       'pandas', 'requests', 'pymysql', 'Django', 'pyserial', 'scipy', 'pyttsx3', 'netifaces',
       'pyqrcode', 'qrcode', 'pypng', 'celery', 'celery-progress', 'python-decouple', 'redis'
    ]

if not is_running_on_pi():
    install_requires.append('fake_rpi')

setuptools.setup(
    name='F3FChrono',
    version='0.1',
    scripts=[] ,
    author="",
    author_email="",
    description="F3F Chronometer and race managment app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jomarin38/F3FChrono",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL v3",
        "Operating System :: OS Independent",
     ],
    install_requires=install_requires
 )
