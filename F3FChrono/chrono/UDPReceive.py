#-udp fonctionnal test
#vim: set et sw=4 sts=4 fileencoding=utf-8:

import threading
import socket
import time
import logging
import re

from PyQt5.QtCore import pyqtSignal, QObject


UDP_PORT = 4445
INITMSG = "Init"
EVENTMSG = "Event"

#todo Qthread à la place de Thread & Qobject.
class udpreceive(threading.Thread, QObject):
    def __init__(self, udpport, eventUI, eventwindUI):
        super().__init__()
        super(QObject, self).__init__()
        self.port = udpport
        self.eventUI = eventUI
        self.event_windUI = eventwindUI

        self.terminated = False
        self.msg = ""
        self.event = threading.Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind (('', self.port))
        self.daemon = True
        self.event.clear()
        self.start()

    def check(self, value):
        self.event.set()

    def run(self):
        while not self.terminated:
            # wait until somebody throws an event
            try:
                data, address = self.sock.recvfrom(1024)
                dt=time.time()
                m=re.split(r'\s', data.decode('utf-8'))
                if (m[0]=='terminated'):
                    self.terminated=True
                elif (m[0]=='simulate' and m[1]=='base'):
                    self.eventUI.emit("udpreceive", m[3], m[2])
                elif (m[0]=='simulate' and m[1]=='weather'):
                    self.event_windUI.emit(int(m[3]), int(m[2]), bool(m[4]=='True'))
                else:
                    self.eventUI.emit("udpreceive", data.decode("utf-8") , address[0])
            except socket.error as msg:
                print ('udp receive error {}'.format(msg))
                logging.warning('udp receive error {}'.format(msg))
                self.event.clear()
                continue

                
if __name__ == '__main__':
    print ("Main start")
    udpreceive = udpreceive (UDP_PORT, None, None, None)
    #udpreceive.event.set ()
    while (not udpreceive.terminated):
        #udpreceive.event.set ()
        time.sleep (1)
        
    udpreceive.join ()
    
    
    



