import threading
import socket
import time
import logging
import re

from PyQt5.QtCore import QThread


INITMSG = "Init"
EVENTMSG = "Event"

'''todo pip3 install iw_parse on picamtracker and send RSSI on udp request.
https://github.com/jsh2134/iw_parse/
'''
class udpreceive(QThread):
    def __init__(self, udpport, signal_chrono, signal_wind, signal_accu, signal_rssi):
        super().__init__()
        self.port = udpport
        self.event_chrono = signal_chrono
        self.event_wind = signal_wind
        self.event_accu = signal_accu
        self.event_rssi = signal_rssi

        self.msg = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind (('', self.port))
        self.start()

    def __del__(self):
        self.wait()


    def run(self):
        while(not self.isFinished()):
        # wait until somebody throws an event
            try:
                data, address = self.sock.recvfrom(1024)
                dt=time.time()
                m=re.split(r'\s', data.decode('utf-8'))
                if (m[0]=='terminated'):
                    self.terminate()
                elif (m[0]=='simulate' and m[1]=='base'):
                    self.event_chrono.emit("udpreceive", m[3], m[2])
                elif (m[0]=='simulate' and m[1]=='weather'):
                    self.event_wind.emit(int(m[3]), int(m[2]), bool(m[4]=='True'))
                elif (m[0] == 'simulate' and m[1] == 'info'):
                    self.event_accu.emit(float(m[2]))
                    self.event_rssi.emit(int(m[3]), int(m[4]))
                else:
                    self.event_chrono.emit("udpreceive", data.decode("utf-8") , address[0])
            except socket.error as msg:
                print ('udp receive error {}'.format(msg))
                logging.warning('udp receive error {}'.format(msg))
                continue

                
if __name__ == '__main__':
    print ("Main start")
    udpreceive = udpreceive (UDP_PORT, None, None, None)
    udpreceive.start()
    while (not udpreceive.isFinished()):
        #udpreceive.event.set ()
        time.sleep (1)
    
    
    



