import time
import os
import sys
import platform
import pygame
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QCoreApplication
from PyQt5.QtMultimedia import QSound



from F3FChrono.chrono.Chrono import chronoStatus

class chronoVocal(QObject): #to use this class, it's needed to install festival and pygame class. Terminal commande line : sudo apt-get install festival, pip3 install pygame
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_time = pyqtSignal(float)
    signal_start = pyqtSignal()

    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.sound=[]
        self.pathname = '/home/sdaviet/PycharmProjects/F3FChrono/Sound/'
        for index in range(11):
            self.sound.append(pygame.mixer.Sound(self.pathname+'base'+str(index)+'.wav'))
        self.penalty=pygame.mixer.Sound(self.pathname+'penalty.wav')
        self.start=pygame.mixer.Sound(self.pathname+'start.wav')

        self.signal_base.connect(self.sound_base)
        self.signal_penalty.connect(self.sound_penalty)
        self.signal_time.connect(self.sound_time)
        self.signal_start.connect(self.sound_start)
        self.soundstart_run=False

    def sound_time(self, time):
        self.waitfinish()
        if (platform.system()=='Linux'):
            msg=None
            msg = 'echo "{:0>.2f} seconds" | festival --tts'.format(time)
            if (msg!=None):
                os.system(msg)

    def sound_base(self, index):
        self.waitfinish()
        self.sound[index].play()
        if self.soundstart_run:
            self.start.stop()

    def sound_penalty(self):
        self.waitfinish()
        self.penalty.play()

    def sound_start(self):
        if self.soundstart_run:
            self.start.stop()
        self.start.play()
        self.soundstart_run=True

    def waitfinish(self):
        while pygame.mixer.music.get_busy() == True:
            continue

class chronoQSound(QObject):
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_time = pyqtSignal(float)
    signal_start = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.sound=[]
        self.pathname = '/home/sdaviet/PycharmProjects/F3FChrono/Sound/'
        for index in range(11):
            self.sound.append(QSound(self.pathname+'base'+str(index)+'.wav'))
        self.penalty=QSound(self.pathname+'penalty.wav')
        self.start=QSound(self.pathname+'start.wav')

        self.signal_base.connect(self.sound_base)
        self.signal_penalty.connect(self.sound_penalty)
        self.signal_time.connect(self.sound_time)
        self.signal_start.connect(self.sound_start)
        self.soundstart_run=False

    def sound_time(self, time):
        if (platform.system()=='Linux'):
            msg=None
            msg = 'echo "{:0>.2f} seconds" | festival --tts'.format(time)
            if (msg!=None):
                os.system(msg)

    def sound_base(self, index):
        if self.soundstart_run:
            self.start.stop()
        self.sound[index].play()

    def sound_penalty(self):
        self.penalty.play()

    def sound_start(self):
        if self.soundstart_run:
            self.start.stop()
        self.start.play()
        self.soundstart_run=True


if __name__ == '__main__':

    '''print ("Main start")
    #Sound = chronoSound ()
    Vocal = chronoVocal ()
    #Sound.event.set ()
    Vocal.Sound ("lap 1")
    time.sleep (2)
    #Sound.terminated=True
    #Sound.join ()

    Vocal=chronoVocal()
    if False:
        for i in range(11):
            Vocal.sound_base(i)
            time.sleep(1)
            Vocal.waitfinish()
        Vocal.sound_time(50.31)
        Vocal.sound_penalty()
        Vocal.waitfinish()
    '''
    app = QCoreApplication(sys.argv)
    Vocal = chronoQSound()
    Vocal.sound_start()
    time.sleep(1)
    sys.exit(app.exec_())


