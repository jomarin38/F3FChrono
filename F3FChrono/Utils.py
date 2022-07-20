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

import os
import re

def get_raspi_revision():
    rev_file = '/sys/firmware/devicetree/base/model'
    info = { 'pi': '', 'model': '', 'rev': ''}
    raspi = model = revision = ''
    try:
        fd = os.open(rev_file, os.O_RDONLY)
        line = os.read(fd,256)
        os.close(fd)
        print (line)
        m=re.split(r'\s', line.decode('utf-8'))
        if m:
            info['pi'] = m[3]
            info['model'] = m[5]
        return info
    except:
        pass
    return info


def is_running_on_pi():
    pi = get_raspi_revision()
    return pi['pi'] != ''


def get_ip():
    import itertools
    import os
    import re


    ip = []
    broadcast = []
    f = os.popen('ifconfig')
    for iface in [' '.join(i) for i in
                  iter(lambda: list(itertools.takewhile(lambda l: not l.isspace(), f)), [])]:
        int = re.findall('^(eth?|wlan?|wlx?|enp?|wlps?)[0-9]', iface)
        if int and re.findall('RUNNING', iface):
            ip.append(re.findall(r'(?<=inet\s)[\d.-]+', iface)[0])
            broadcast.append(re.findall(r'(?<=broadcast\s)[\d.-]+', iface)[0])
    if len(broadcast)>0:
        index = 0
        if "192.168.1.251" in ip:
            index = ip.index("192.168.1.251")
        return ip[index], broadcast[index]
    else:
        return None, None