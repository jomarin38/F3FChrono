#-udp fonctionnal test
#vim: set et sw=4 sts=4 fileencoding=utf-8:

import socket
import time
import logging
import sys
from PyQt5.QtCore import QObject

UDP_IP_UDPBEEP = "192.168.1.72"
UDP_IP_HOME = "192.168.0.23"
UDP_PORT = 4445
INITMSG = "Init"
EVENTMSG = "Event"

class udpbeep(QObject):
    def __init__(self, udpip, udpport):
        super(QObject, self).__init__()
        self.udpip = udpip
        self.port = udpport
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self):
        self.sock.sendto(bytes('event', 'utf-8'), (self.udpip, self.port))

    def sendData(self, data):
        self.sock.sendto(bytes(data, 'utf-8'), (self.udpip, self.port))

    def terminate(self):
        print('terminated event')
        self.sock.sendto(bytes('terminated', 'utf-8'), (self.udpip, self.port)) 

if __name__ == '__main__':
    print ("UDP Beep Debug")
    #udpbeep = udpBeep ("192.168.0.22", UDP_PORT)
    udpBeep = udpbeep ("255.255.255.255", UDP_PORT)
    end=False
    while not end:
        cmdline=sys.stdin.readline ()
        print (cmdline)
        if (cmdline=="terminate\n"):
            udpBeep.terminate()
            end = True
        else:
            udpBeep.send()



