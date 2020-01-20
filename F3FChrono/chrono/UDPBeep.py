#-udp fonctionnal test
#vim: set et sw=4 sts=4 fileencoding=utf-8:

import socket
import time
import logging
import sys
from PyQt5.QtCore import QObject


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

    def __del__(self):
        del self.sock

    def send(self):
        self.sock.sendto(bytes('event', 'utf-8'), (self.udpip, self.port))

    def sendData(self, data):
        self.sock.sendto(bytes(data, 'utf-8'), (self.udpip, self.port))

    def terminate(self):
        print('terminated event')
        self.sock.sendto(bytes('terminated', 'utf-8'), (self.udpip, self.port)) 

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



