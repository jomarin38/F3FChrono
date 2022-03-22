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
import RPi.GPIO as GPIO
from PyQt5.QtCore import QObject, pyqtSignal
from F3FChrono.chrono import ConfigReader


def statusLED(port, on=True):
    """
    enable the status led
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(port, GPIO.OUT)
    if on:
        GPIO.output(port, GPIO.HIGH)
    else:
        GPIO.output(port, GPIO.LOW)


def addCallback(port, fctn, falling=True):
    """
    add a callback function to a falling or raising edge of a port
    """
    # TODO: add exception handling
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    if falling:
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(port, GPIO.FALLING, callback=fctn, bouncetime=500)
    else:
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(port, GPIO.RISING, callback=fctn, bouncetime=500)


class gpioPort(QTimer):
    def __init__(self, port, duration=200., is_active_low=False, start_blinks=0):
        super().__init__()
        self.terminated = False
        self.duration = duration
        self.port = port
        self.activate = GPIO.HIGH
        self.deactivate = GPIO.LOW
        self.state = False
        self.nbevent = 0
        self.timeout.connect(self.run)
        self.__debug = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port, GPIO.OUT)

        if is_active_low:
            self.activate = GPIO.LOW
            self.deactivate = GPIO.HIGH
        if start_blinks > 0:
            self.slot_blink("blink", start_blinks)

        self.__deactivate()

    def __del__(self):
        self.__deactivate()

    def slot_blink(self, mode, numbers, duration=-1):
        if mode.lower() == "stop":
            self.__deactivate()
        elif mode.lower() == "permanent":
            self.__activate()
        elif mode.lower() == "blink":
            self.nbevent = numbers
            if self.nbevent > 0:
                if duration == -1:
                    self.start(self.duration)
                elif duration > 0:
                    self.start(duration)

    def run(self):
        if (self.port == ConfigReader.config.conf['buzzer'] and ConfigReader.config.conf['buzzer_valid'] or
                self.port == ConfigReader.config.conf['buzzer_next'] and
                ConfigReader.config.conf['buzzer_next_valid']):
            if self.nbevent > 0 or self.nbevent == -1:
                if self.state:
                    self.__deactivate()
                    if self.nbevent > 0:
                        self.nbevent = self.nbevent - 1
                else:
                    self.__activate()
                if self.nbevent == 0:
                    self.stop()

    def __activate(self):
        GPIO.output(self.port, self.activate)
        self.state = True
        if self.__debug:
            print("gpio__activate")
        
    def __deactivate(self):
        GPIO.output(self.port, self.deactivate)
        self.state = False
        if self.__debug:
            print("gpio__deactivate")


def event_detected(port):
    print("callback " + str(port))


def event_detected(port):
    print("callback " + str(port))


class rpi_gpio(QObject):
    signal_buzzer = pyqtSignal(int)
    signal_buzzer_next = pyqtSignal(int)
    signal_btn_next = pyqtSignal()
    btnNext_Timer = QTimer()

    def __init__(self, rpi):
        super().__init__()
        self.signal_buzzer.connect(self.buzzer_fct)
        self.signal_buzzer_next.connect(self.buzzer_next_fct)
        self.buzzer = None
        self.buzzer_next = None
        self.configBtnNext = ConfigReader.config.conf['btn_next']
        self.__debug = True
        if rpi:
            self.buzzer = gpioPort(ConfigReader.config.conf['buzzer'],
                                   duration=ConfigReader.config.conf['buzzer_duration'], start_blinks=2)
            self.buzzer_next = gpioPort(ConfigReader.config.conf['buzzer_next'],
                                        duration=ConfigReader.config.conf['buzzer_next_duration'], start_blinks=2)
            # btn_next callback
            addCallback(self.configBtnNext, self.btn_next_action, True)
            self.btnNext_Timer.timeout.connect(self.btn_next_check)
            self.signal_btn_next.connect(self.btn_next_event)
            


    def buzzer_fct(self, nb):
        if self.__debug:
            print("buzzer base")
        if self.buzzer is not None:
            self.buzzer.slot_blink("blink", nb)

    def buzzer_next_fct(self, nb):
        if self.__debug:
            print("buzzer next : ", nb)
        if self.buzzer_next is not None:
            self.buzzer_next.slot_blink("blink", nb)

    def btn_next_action(self, port):
        if port==self.configBtnNext:
            if self.__debug:
                print("gpio btn_next_action")
            self.signal_btn_next.emit()

    def btn_next_event(self):
        GPIO.remove_event_detect(self.configBtnNext)
        self.btnNext_Timer.start(200)
        if self.__debug:
            print("gpio signal btn_next_event")
        
    def btn_next_check(self):
        if GPIO.input(self.configBtnNext):
            addCallback(self.configBtnNext, self.btn_next_action, True)
            self.btnNext_Timer.stop()
            if self.__debug:
                print("gpio btn_next_check")

if __name__ == '__main__':
    led = gpioPort(19, duration=1000, start_blinks=2)
    addCallback(12, event_detected, False)
    addCallback(5, event_detected, False)
    addCallback(6, event_detected, False)

    sleep(10)

    led.terminated = True
    led.join()

'''    def pressed(value):
        print("pressed %d" % value)

    #addCallback(2,pressed)
    statusLED(23,on=True)

    p1=19
    p2=27

    port1 = gpioPort(p1)
    port2 = gpioPort(p2, duration=3000)
    port1.event.set()
    port2.event.set()
    sleep(2)
    port1.event.set()
    sleep(2)
    port1.terminated = True
    port2.terminated = True
    port1.join()
    port2.join()

    statusLED(23, on=False)
    GPIO.cleanup()
'''
