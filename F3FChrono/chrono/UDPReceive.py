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
    ipbase_clear_sig = pyqtSignal()
    ipbase_invert_sig = pyqtSignal(list)
    ipbase_set_sig = pyqtSignal(list, list)
    ipwBtn_clear_sig = pyqtSignal()
    ipwBtn_set_sig = pyqtSignal(str, str, str)
    simulate_base_sig = pyqtSignal(str)
    simulate_wbtn_sig = pyqtSignal(str)

    def __init__(self, udpport, signal_chrono, signal_btnnext, signal_wind, signal_rain, signal_accu, signal_rssi):
        super().__init__()
        self.port = udpport
        self.event_chrono = signal_chrono
        self.event_btn_next = signal_btnnext
        self.event_wind = signal_wind
        self.event_rain = signal_rain
        self.event_accu = signal_accu
        self.event_rssi = signal_rssi
        self.ipbaseA = ""
        self.ipbaseB = ""
        self.ipwBtn_baseA = ""
        self.ipwBtn_baseB = ""
        self.ipwBtn_btnNext = ""
        self.ipbase_clear_sig.connect(self.clear_ipbase)
        self.ipbase_invert_sig.connect(self.invert_ipbase)
        self.ipbase_set_sig.connect(self.set_ipbase)
        self.ipwBtn_clear_sig.connect(self.clear_ipwBtn)
        self.ipwBtn_set_sig.connect(self.set_ipwBtn)


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

    def set_ipwBtn(self, baseA, baseB, btnNext):
        self.ipwBtn_baseA = baseA
        self.ipwBtn_baseB = baseB
        self.ipwBtn_btnNext = btnNext
        print("baseA : ", baseA, "baseB : ", baseB)

    def clear_ipwBtn(self):
        self.ipwBtn_baseA = ""
        self.ipwBtn_baseB = ""
        self.ipwBtn_btnNext = ""

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
                    base = self._find_base_name(m[2])
                    if base is not None:
                        self.event_chrono.emit("udpreceive", 'event', base)
                    else:
                        self.simulate_base_sig.emit(m[2])
                elif (m[0]=='simulate' and m[1]=='GPIO'):
                    if m[2].lower()=="btnnext":
                        self.event_btn_next.emit(0)
                elif (m[0]=='simulate' and m[1]=='wBtn'):
                    if m[2].lower()==self.ipwBtn_btnNext:
                        self.event_btn_next.emit(0)
                    elif m[2].lower()==self.ipwBtn_baseA:
                        self.event_chrono.emit("udpreceive", 'event', 'baseA')
                    elif m[2].lower() == self.ipwBtn_baseB:
                        self.event_chrono.emit("udpreceive", 'event', 'baseB')
                    else:
                        self.simulate_wbtn_sig.emit(m[2])
                elif m[0]=='wind':
                    self.event_wind.emit(int(m[2]), int(m[1]))
                elif m[0]=='rain':
                    self.event_rain.emit(bool(m[1] == 'True'))

                elif m[0] == 'info':
                    self.event_accu.emit(float(m[1]))
                    self.event_rssi.emit(int(m[2]), int(m[3]))
                else:
                    base = address[0]
                    self.event_chrono.emit("udpreceive", data.decode("utf-8").lower(),
                                           self._find_base_name(base))
            except socket.error as msg:
                print('udp receive error {}'.format(msg))
                logging.warning('udp receive error {}'.format(msg))
                continue

    def _find_base_name(self, ip):
        if ip in self.ipbaseA:
            print("baseA")
            return "baseA"
        elif ip in self.ipbaseB:
            print("baseB")
            return "baseB"
        else:
            return None

if __name__ == '__main__':
    print ("Main start")
    udpreceive = udpreceive(UDP_PORT, None, None, None)
    udpreceive.start()
    while (not udpreceive.isFinished()):
        #udpreceive.event.set ()
        time.sleep (1)
    
    
    



