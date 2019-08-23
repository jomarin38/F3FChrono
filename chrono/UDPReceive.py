#-udp fonctionnal test
#vim: set et sw=4 sts=4 fileencoding=utf-8:

import threading
import socket
import time
import logging



UDP_PORT = 4445
INITMSG = "Init"
EVENTMSG = "Event"

class udpreceive(threading.Thread):
    def __init__(self, udpport, chronoID, ledID, eventUI):
        super(udpreceive, self).__init__()
        self.port = udpport
        self.chronoID=chronoID
        self.ledID=ledID
        self.eventUI=eventUI
        self.terminated = False
        self.msg = ""
        self.event      = threading.Event()
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind (('',self.port))
        self.daemon = True
        self.event.clear()
        self.start()
        


    def check(self, value):
        self.event.set()

    def run(self):
        while not self.terminated:
            # wait until somebody throws an event
            #if self.event.wait(0.5):
                try:
                    data, address = self.sock.recvfrom(1024)
                    dt=time.time()
                    print ('received {} bytes from {}, time : {}'.format(len (data), address, dt))
                    print (data)
                    if (data.decode ('utf-8')=='terminated'):
                        self.terminated=True
                    elif not (self.chronoID==None):
                        #if (self.chronoID.isInStart ()):
                        self.chronoID.declareBase(address)
                        
                    if not (self.ledID==None):
                        self.ledID.event.set()
                    if not (self.eventUI==None):
                        if not (self.chronoID==None):
                            self.Msg = str(self.chronoID.getLapCount ())+" : "+'{:.2f}'.format (self.chronoID.getLastLapTime ())
                            if (self.chronoID.getLapCount ()>=10):
                                self.Msg=self.Msg + ", 10B : "+'{:.2f}'.format (self.chronoID.getLast10BasesTime ()) + ", 10BLost : " + '{:.2f}'.format (self.chronoID.getLast10BasesTime ())
                        self.eventUI.signalID.emit (self.Msg)
                    
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
    
    
    



