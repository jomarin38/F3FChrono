import time
import os
import sys
import platform
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QCoreApplication
from PyQt5.QtMultimedia import QSound
from F3FChrono.chrono import ConfigReader


'''class chronoVocal(QObject): #to use this class, it's needed to install festival and pygame class. Terminal commande line : sudo apt-get install festival, pip3 install pygame
    import pygame
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
'''


class chronoQSound(QObject):
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_entry = pyqtSignal()
    signal_time = pyqtSignal(float)
    signal_waitlaunch = pyqtSignal()
    signal_waitlaunch_stop = pyqtSignal()
    signal_waitstart = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.soundbase=[]
        self.pathname=os.path.dirname(os.path.realpath('Sound/base0.wav'))

        for index in range(11):
            self.soundbase.append(QSound(self.pathname+'/base'+str(index)+'.wav'))
        self.entry=QSound(self.pathname+'/entry.wav')
        self.penalty=QSound(self.pathname+'/penalty.wav')
        self.waitlaunch=QSound(self.pathname+'/start.wav')
        self.waitstart=QSound(self.pathname+'/start.wav')

        self.signal_waitlaunch.connect(self.sound_waitlaunch)
        self.signal_waitlaunch_stop.connect(self.sound_waitlaunch_stop)
        self.signal_waitstart.connect(self.sound_waitstart)
        self.signal_entry.connect(self.sound_entry)
        self.signal_base.connect(self.sound_base)
        self.signal_time.connect(self.sound_time)
        self.signal_penalty.connect(self.sound_penalty)
        self.soundstart_run=False


    def sound_time(self, time):
        if (ConfigReader.config.conf['voice']):
            if (platform.system()=='Linux'):
                msg = 'echo "{:0>.2f} seconds" | festival --tts'.format(time)
                os.system(msg)

    def sound_base(self, index):
        if ConfigReader.config.conf['sound']:
            self.soundbase[index].play()
            if self.soundstart_run:
                self.waitstart.stop()

    def sound_entry(self):
        if ConfigReader.config.conf['sound']:
            self.entry.play()

    def sound_penalty(self):
        if ConfigReader.config.conf['sound']:
            self.penalty.play()

    def sound_waitlaunch(self):
        if ConfigReader.config.conf['sound']:
            self.waitlaunch.play()
            self.soundstart_run=True

    def sound_waitlaunch_stop(self):
        self.waitlaunch.stop()
        
    def sound_waitstart(self):
        if ConfigReader.config.conf['sound']:
            self.waitstart.play()
            if self.soundstart_run:
                self.waitlaunch.stop()
            self.soundstart_run=True

    def stop_all(self):
        self.waitlaunch.stop()
        self.waitstart.stop()
        self.entry.stop()
        self.penalty.stop()
        for sound in self.soundbase:
            sound.stop()


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
    Vocal.sound_waitstart()
    time.sleep(1)
    #Vocal.sound_time(100)
    sys.exit(app.exec_())


