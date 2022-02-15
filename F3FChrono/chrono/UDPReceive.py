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
    ipwBtn_set_sig = pyqtSignal(list, list, list, list, list)
    simulate_base_sig = pyqtSignal(str)
    simulate_wbtn_sig = pyqtSignal(str)
    switchMode_sig = pyqtSignal()
    penalty_sig = pyqtSignal()

    def __init__(self, udpport, signal_chrono, signal_btnnext, signal_windspeed, signal_winddir, signal_rain, \
                 signal_picam, weatherList_sig, weatherStatus_sig):
        super().__init__()
        self.__debug = False
        self.port = udpport
        self.event_chrono = signal_chrono
        self.event_btn_next = signal_btnnext
        self.event_wind_speed = signal_windspeed
        self.event_wind_dir = signal_winddir
        self.event_rain = signal_rain
        self.event_picam = signal_picam
        self.event_weatherlist_sig = weatherList_sig
        self.event_weatherStatus_sig = weatherStatus_sig
        self.clear_ipbase()
        self.clear_ipwBtn()

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
        if self.__debug:
            print("baseA : ", baseA, "\nbaseB : ", baseB)

    def clear_ipbase(self):
        self.ipbaseA = []
        self.ipbaseB = []

    def invert_ipbase(self):
        tmp = self.ipbaseB
        self.ipbaseB = self.ipbaseA
        self.ipbaseA = tmp

    def set_ipwBtn(self, baseA, baseB, btnNext, switchMode, penalty):
        self.ipwBtn_baseA = baseA
        self.ipwBtn_baseB = baseB
        self.ipwBtn_btnNext = btnNext
        self.ipwBtn_SwitchMode = switchMode
        self.ipwBtn_penalty = penalty
        if self.__debug:
            print("baseA : ", baseA, "\nbaseB : ", baseB, "\nBtn Next : ", btnNext, "\nSwitchMode : ", switchMode,
                  "\nPenalty : ", penalty)

    def clear_ipwBtn(self):
        self.ipwBtn_baseA = [[], [], []]
        self.ipwBtn_baseB = [[], [], []]
        self.ipwBtn_btnNext = [[], [], []]
        self.ipwBtn_SwitchMode = [[], [], []]
        self.ipwBtn_penalty = [[], [], []]

    def run(self):
        while (not self.isFinished()):
            # wait until somebody throws an event
            try:
                data, address_temp = self.sock.recvfrom(1024)
                address = list(address_temp)
                if self.__debug:
                    print(data, address)
                dt = time.time()
                m = re.split(r'\s', data.decode('utf-8'))
                if (m[0] == 'terminated'):
                    self.terminate()
                    break
                elif m[0] == 'simulate':
                    if m[1] == 'GPIO':
                        if m[2].lower() == "btnnext":
                            self.event_btn_next.emit(0)
                        break
                    if m[1] == 'base':
                        address[0] = m[2]
                        for i in range(0, 3):
                            del(m[0])
                    elif m[1] == 'wBtn':
                        address[0] = m[2]
                        del(m[2])
                        del(m[0])
                    else:
                        del(m[0])

                if m[0] == 'wind_speed':
                    self.event_wind_speed.emit(float(m[1]), str(m[2]))
                elif m[0] == 'wind_dir':
                    self.event_wind_dir.emit(float(m[1]), float(m[2]))
                elif m[0] == 'rain':
                    self.event_rain.emit(bool(m[1] == 'True'))
                elif m[0] == 'info':
                    self.event_picam.emit(float(m[1]), float(m[2]))
                elif m[0] == 'wBtn':
                    self._wbtn_function(address[0], int(m[1]))
                elif m[0] == "anemometerList":
                    temp = list()
                    for i in range(0, int(m[1])):
                        temp.append(m[2+i])
                    self.event_weatherlist_sig.emit(temp)
                elif m[0] == "anemometerStatus":
                    self.event_weatherStatus_sig.emit(m[1])
                else:
                    self._base_function(m[0].lower(), address[0])
            except socket.error as msg:
                print('udp receive error {}'.format(msg))
                logging.warning('udp receive error {}'.format(msg))
                continue

    def _base_function(self, event, ip):
        find, base = self._find_ip_function(ip)
        if not find:
            self.simulate_base_sig.emit(ip)
            base = ip
        else:
            self.event_chrono.emit("udpreceive", event, base)
        return find, base

    def _wbtn_function(self, ip, shortpush):
        find, base = self._find_ip_function(ip, shortpush)
        if find and (base == "baseA" or base == "baseB"):
            self.event_chrono.emit("udpreceive", "event", base)
        elif find and base == "btn_next":
            self.event_btn_next.emit()
        elif find and base == "switch_mode":
            self.switchMode_sig.emit()
        elif find and base == "penalty":
            self.penalty_sig.emit()
        else:
            self.simulate_wbtn_sig.emit(ip)

    def _find_ip_function(self, ip, shortpush=0):  # return True if find in lists, "function"; False not find, "ip"
        if shortpush <= len(self.ipwBtn_baseA) and shortpush <= len(self.ipwBtn_baseB) \
                and shortpush <= len(self.ipwBtn_btnNext) and shortpush <= len(self.ipwBtn_SwitchMode) and\
                shortpush <= len(self.ipwBtn_penalty):
            if ip in self.ipbaseA or ip in self.ipwBtn_baseA[shortpush]:
                if self.__debug:
                    print("baseA")
                return True, "baseA"
            elif ip in self.ipbaseB or ip in self.ipwBtn_baseB[shortpush]:
                if self.__debug:
                    print("baseB")
                return True, "baseB"
            elif ip in self.ipwBtn_btnNext[shortpush]:
                if self.__debug:
                    print("btn_next")
                return True, "btn_next"
            elif ip in self.ipwBtn_SwitchMode[shortpush]:
                if self.__debug:
                    print("switch mode")
                return True, "switch_mode"
            elif ip in self.ipwBtn_penalty[shortpush]:
                if self.__debug:
                    print("Penalty")
                return True, "penalty"
            else:
                return False, ip
        else:
            return False, ip

if __name__ == '__main__':
    UDP_PORT = 4445
    print("Main start")
    udpreceive = udpreceive(UDP_PORT, None, None, None)
    udpreceive.start()
    while (not udpreceive.isFinished()):
        # udpreceive.event.set ()
        time.sleep(1)
