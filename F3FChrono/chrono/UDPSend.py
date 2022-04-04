#-udp fonctionnal test
#vim: set et sw=4 sts=4 fileencoding=utf-8:

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

import socket
import time
import logging
import sys
from PyQt5.QtCore import QObject


INITMSG = "Init"
EVENTMSG = "Event"
RACEORDERMSG = "Order"

#IPUDPSEND = '255.255.255.255'
UDPPORT = 4445


class udpsend(QObject):
    def __init__(self, udpip, udpport):
        super(QObject, self).__init__()
        print(udpip, udpport)
        self.udpip = udpip
        self.port = udpport
        try:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except Exception as error:
            print("udpsend init error : ", error)

    def __del__(self):
        del self.sock

    def sendEvent(self):
        try:
            self.sock.sendto(bytes('event', 'utf-8'), (self.udpip, self.port))
        except Exception as error:
            print("udpsendEvent error : ", error)


    def sendData(self, data):
        try:
            self.sock.sendto(bytes(data, 'utf-8'), (self.udpip, self.port))
        except Exception as error:
            print("udpsendData error : ", error)

    def sendOrderData(self, data):
        try:
            self.sock.sendto(bytes((RACEORDERMSG+ ' '+ data), 'utf-8'), (self.udpip, self.port))
        except Exception as error:
            print("udpsendOrderData error : ", error)

    def terminate(self):
        print('terminated event')
        try:
            self.sock.sendto(bytes('terminated', 'utf-8'), (self.udpip, self.port))
        except Exception as error:
            print("udpsendTerminate error : ", error)

if __name__ == '__main__':
    print ("UDP Beep Debug")
    #udpbeep = udpBeep ("192.168.0.22", 4445)
    udpBeep = udpbeep ("255.255.255.255", 4445)
    end=False
    while not end:
        cmdline=sys.stdin.readline ()
        print (cmdline)
        if (cmdline=="terminate\n"):
            udpBeep.terminate()
            end = True
        else:
            udpBeep.send()



