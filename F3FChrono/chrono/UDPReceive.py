import threading
import socket
import time
import logging
import re

from PyQt5.QtCore import QThread, pyqtSignal


INITMSG = "Init"
EVENTMSG = "Event"

'''todo pip3 install iw_parse on picamtracker and send RSSI on udp request.
https://github.com/jsh2134/iw_parse/
'''
class udpreceive(QThread):
    ipbaseclear_sig = pyqtSignal()
    ipinvert_sig = pyqtSignal()
    ipset_sig = pyqtSignal(str, str)

    def __init__(self, udpport, signal_chrono, signal_btnnext, signal_wind, signal_accu, signal_rssi):
        super().__init__()
        self.port = udpport
        self.event_chrono = signal_chrono
        self.event_btn_next = signal_btnnext
        self.event_wind = signal_wind
        self.event_accu = signal_accu
        self.event_rssi = signal_rssi
        self.ipbaseA = ""
        self.ipbaseB = ""
        self.ipbaseclear_sig.connect(self.clear_ipbase)
        self.ipinvert_sig.connect(self.invert_ipbase)
        self.ipset_sig.connect(self.set_ipbase)


        self.msg = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.start()

    def __del__(self):
        self.wait()

    def set_ipbase(self, baseA, baseB):
        self.ipbaseA = baseA
        self.ipbaseB = baseB
        print("baseA : ", baseA, "baseB : ", baseB)

    def clear_ipbase(self):
        self.ipbaseA = ""
        self.ipbaseB = ""

    def invert_ipbase(self):
        tmp = self.ipbaseB
        self.ipbaseB = self.ipbaseA
        self.ipbaseA = tmp

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
                    base = m[2]
                    if base == self.ipbaseA:
                        base = "baseA"
                    elif base == self.ipbaseB:
                        base = "baseB"
                    self.event_chrono.emit("udpreceive", 'event', base)
                elif (m[0]=='simulate' and m[1]=='GPIO'):
                    if m[2].lower()=="btnnext":
                        self.event_btn_next.emit(0)

                elif (m[0]=='simulate' and m[1]=='weather'):
                    self.event_wind.emit(int(m[3]), int(m[2]), bool(m[4]=='True'))
                elif (m[0] == 'simulate' and m[1] == 'info'):
                    self.event_accu.emit(float(m[2]))
                    self.event_rssi.emit(int(m[3]), int(m[4]))
                else:
                    base = address[0]
                    if base == self.ipbaseA:
                        base = "baseA"
                    elif base == self.ipbaseB:
                        base = "baseB"
                    self.event_chrono.emit("udpreceive", data.decode("utf-8").lower(), base)
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
    
    
    



