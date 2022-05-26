# vim: set et sw=4 sts=4 fileencoding=utf-8:

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
from time import sleep
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from gpiozero import Button, LED
from PyQt5.QtCore import QObject, pyqtSignal
from F3FChrono.chrono import ConfigReader




class rpi_gpio(QObject):
    signal_buzzer = pyqtSignal(int)
    signal_buzzer_next = pyqtSignal(int)
    signal_btn_next = pyqtSignal()

    def __init__(self, rpi):
        super().__init__()
        self.signal_buzzer.connect(self.buzzer_fct)
        self.signal_buzzer_next.connect(self.buzzer_next_fct)
        self.buzzer_next = None
        self.__debug = True
        self.nb_event = 0
        self.btnnext_enableEvent = True
        if rpi:
            self.btnNext = Button(ConfigReader.config.conf['btn_next'], pull_up = None, active_state=False, bounce_time=0.1)
            self.buzzer_next = LED(ConfigReader.config.conf['buzzer_next'])
            self.buzzer_next_fct (2)
            self.btnNext.when_pressed = self.btnNext_pressed
            self.btnNext.when_released = self.btnNext_released

    def buzzer_fct(self, nb):
        if self.__debug:
            print("buzzer base")
        if self.buzzer is not None:
            self.buzzer.slot_blink("blink", nb)
            
    def buzzer_next_fct(self, nb):
        if self.__debug:
            print("buzzer next : ", nb)
        if self.buzzer_next is not None:
            self.buzzer_next.blink(0.5, 0.5, nb)
            
    def buzzer_next_slot_blink(self, mode, number, duration=-1):#duration in seconds
        if mode.lower() == "stop":
            self.buzzer_next.off()
        elif mode.lower() == "permanent":
            self.buzzer_next.on()
        elif mode.lower() == "blink":
            beeptime = 0.5
            if duration != -1:
                beeptime = duration/1000
            self.buzzer_next.blink(beeptime, beeptime, number)
            if (self.__debug):
                print("buzzer next blink duration:", beeptime)

    def btnNext_pressed(self):
        if self.__debug:
            print("gpio btnNext_pressed")
        if self.btnnext_enableEvent:
            self.signal_btn_next.emit()
            self.btnnext_enableEvent = False

    def btnNext_released(self):
        self.btnnext_enableEvent = True
        #self.btnNext_Timer.start(200)
        if self.__debug:
            print("gpio signal btn_next_released")



if __name__ == '__main__':
    import sys
    from F3FChrono.Utils import is_running_on_pi
    from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QThread, QCoreApplication
    
    ConfigReader.init()
    ConfigReader.config = ConfigReader.Configuration('../../config.json')
    rpi = rpi_gpio(rpi = is_running_on_pi())

    rpi.signal_btn_next.connect(rpi.event_signal)
    app = QCoreApplication(sys.argv)
    
    sys.exit(app.exec())

    del (rpi)
