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

import requests
from netifaces import AF_INET
import netifaces as ni


class Utils:

    _port_number = 8000
    _protocol = 'http://'

    @staticmethod
    def get_ip():

        interfaces = ni.interfaces()

        if 'wlan1' in interfaces:
            return ni.ifaddresses('wlan1')[AF_INET][0]['addr']
        elif 'wlan0' in interfaces:
            return ni.ifaddresses('wlan0')[AF_INET][0]['addr']
        else:
            #Probably not running on raspberry pi ... try to find working interface
            for interface in interfaces:
                if interface != 'lo':
                    if AF_INET in ni.ifaddresses(interface):
                        return ni.ifaddresses(interface)[AF_INET][0]['addr']

        #return the loopback address if we did not find anything better
        return '127.0.0.1'

    @staticmethod
    def set_port_number(port_number):
        Utils._port_number=port_number

    @staticmethod
    def get_port_number():
        return Utils._port_number

    @staticmethod
    def get_base_url():
        return Utils._protocol + Utils.get_ip() + ':' + str(Utils.get_port_number()) + '/f3franking'

    @staticmethod
    def get_logout_url():
        return Utils._protocol + Utils.get_ip() + ':' + str(Utils.get_port_number()) + '/administrator/logout_f3f_admin'

    @staticmethod
    def server_alive():
        try:
            request_url = Utils.get_base_url()+'/is_alive'
            response = requests.post(request_url)
            return True
        except:
            return False
