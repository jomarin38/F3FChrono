# vim: set et sw=4 sts=4 fileencoding=utf-8:
import threading
from time import sleep
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
    #GPIO.setwarnings(False)
    if falling:
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(port, GPIO.FALLING, callback=fctn, bouncetime=500)
    else:
        GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(port, GPIO.RISING, callback=fctn, bouncetime=500)



class gpioPort(threading.Thread):
    def __init__(self, port, duration=200., is_active_low=False, start_blinks=0):
        super(gpioPort, self).__init__()
        self.terminated = False
        self.duration   = duration
        self.event      = threading.Event()
        self.port       = port
        self.activate   = GPIO.HIGH
        self.deactivate = GPIO.LOW

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port,GPIO.OUT)

        if is_active_low:
            self.activate   = GPIO.LOW
            self.deactivate = GPIO.HIGH

        if start_blinks > 0:
            self.blink(start_blinks)

        GPIO.output(self.port,self.deactivate)

        self.daemon = True
        self.event.clear()
        self.start()

    def blink(self, numbers):
        if (self.port == ConfigReader.Configuration.conf['buzzer'] and ConfigReader.Configuration.conf[
            'buzzer_valid'] or
                self.port == ConfigReader.Configuration.conf['buzzer_next'] and ConfigReader.Configuration.conf[
                    'buzzer_next_valid']):
            for i in range(0,numbers):
                GPIO.output(self.port,self.activate)
                sleep(self.duration/1000.0)
                GPIO.output(self.port,self.deactivate)
                sleep(self.duration/1000.0)

    def check(self, value):
        self.event.set()

    def run(self):
        while not self.terminated:
            # wait until somebody throws an event
            if self.event.wait(1):
                if (self.port==ConfigReader.Configuration.conf['buzzer'] and ConfigReader.Configuration.conf['buzzer_valid'] or
                    self.port == ConfigReader.Configuration.conf['buzzer_next'] and ConfigReader.Configuration.conf[
                        'buzzer_next_valid']):
                    # create rectangle signal on GPIO port
                    GPIO.output(self.port,self.activate)
                    sleep(self.duration/1000.0)
                    GPIO.output(self.port,self.deactivate)
                    self.event.clear()

        #GPIO.cleanup(self.port)
        GPIO.cleanup()
        
        
def event_detected(port):
    print("callback "+str(port))


'''class gpioPort(threading.Thread):
    def __init__(self, port, duration=200., is_active_low=False, start_blinks=0):
        super(gpioPort, self).__init__()
        self.terminated = False
        self.duration = duration
        self.event = threading.Event()
        self.port = port
        self.activate = GPIO.HIGH
        self.deactivate = GPIO.LOW

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port, GPIO.OUT)

        if is_active_low:
            self.activate = GPIO.LOW
            self.deactivate = GPIO.HIGH

        if start_blinks > 0:
            self.blink(start_blinks)

        GPIO.output(self.port, self.deactivate)

        self.daemon = True
        self.event.clear()
        self.start()

    def blink(self, numbers):
        if (self.port == ConfigReader.config.conf['buzzer'] and ConfigReader.config.conf[
            'buzzer_valid'] or
                self.port == ConfigReader.config.conf['buzzer_next'] and ConfigReader.config.conf[
                    'buzzer_next_valid']):
            for i in range(0, numbers):
                GPIO.output(self.port, self.activate)
                sleep(self.duration / 1000.0)
                GPIO.output(self.port, self.deactivate)
                sleep(self.duration / 1000.0)

    def check(self, value):
        self.event.set()

    def run(self):
        while not self.terminated:
            # wait until somebody throws an event
            if self.event.wait(1):
                if (self.port == ConfigReader.config.conf['buzzer'] and ConfigReader.config.conf['buzzer_valid'] or
                        self.port == ConfigReader.config.conf['buzzer_next'] and ConfigReader.config.conf[
                            'buzzer_next_valid']):
                    # create rectangle signal on GPIO port
                    GPIO.output(self.port, self.activate)
                    sleep(self.duration / 1000.0)
                    GPIO.output(self.port, self.deactivate)
                    self.event.clear()

        # GPIO.cleanup(self.port)
        GPIO.cleanup()

'''
def event_detected(port):
    print("callback " + str(port))


class rpi_gpio(QObject):
    signal_buzzer = pyqtSignal()
    signal_buzzer_end = pyqtSignal()
    signal_buzzer_next = pyqtSignal()

    def __init__(self, rpi, btn_next_action, btn_baseA, btn_baseB):
        super().__init__()
        self.signal_buzzer.connect(self.buzzer_fct)
        self.signal_buzzer_end.connect(self.buzzer_end_fct)
        self.signal_buzzer_next.connect(self.buzzer_next_fct)
        self.buzzer = None
        self.buzzer_next = None
        if rpi != '':
            self.buzzer = gpioPort(ConfigReader.config.conf['buzzer'],
                                   duration=ConfigReader.config.conf['buzzer_duration'], start_blinks=2)
            self.buzzer_next = gpioPort(ConfigReader.config.conf['buzzer_next'],
                                        duration=ConfigReader.config.conf['buzzer_next_duration'], start_blinks=2)
            # btn_next callback
            addCallback(ConfigReader.config.conf['btn_next'], btn_next_action, False)
            # btn_baseA
            addCallback(ConfigReader.config.conf['btn_baseA'], btn_baseA, False)
            # btn_baseB
            addCallback(ConfigReader.config.conf['btn_baseB'], btn_baseB, False)

    def __del__(self):
        if self.buzzer != None:
            self.buzzer.terminated = True
            self.buzzer.join()

    def buzzer_fct(self):
        print("buzzer base")
        if self.buzzer != None:
            self.buzzer.event.set()

    def buzzer_end_fct(self):
        print("buzzer base end*3")
        if self.buzzer != None:
            self.buzzer.blink(3)

    def buzzer_next_fct(self):
        print("buzzer next")
        if self.buzzer_next != None:
            self.buzzer_next.event.set()


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