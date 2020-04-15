import time
import os
import sys
import platform
import collections
from F3FChrono.chrono import ConfigReader
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QCoreApplication
from PyQt5.QtMultimedia import QSound
from F3FChrono.chrono import ConfigReader


class chronoQSound(QObject):
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_entry = pyqtSignal()
    signal_time = pyqtSignal(float)
    signal_elapsedTime = pyqtSignal(str)
    signal_start = pyqtSignal(int)


    def __init__(self, playsound, playvoice, buzzer):
        super().__init__()
        self.soundbase = []

        self.elapsedtime = collections.OrderedDict()
        self.loadwav(playsound, playvoice, buzzer)
        self.signal_elapsedTime.connect(self.sound_elapsedTime)
        self.signal_entry.connect(self.sound_entry)
        self.signal_base.connect(self.sound_base)
        self.signal_time.connect(self.sound_time)
        self.signal_penalty.connect(self.sound_penalty)
        self.soundstart_run = False


    def loadwav(self, playsound, playvoice,  buzzer):
        self.play_sound = playsound
        self.play_voice = playvoice
        pathname = os.path.dirname(os.path.realpath('Sound/base0.wav'))
        lap_pathname = pathname + '/laps_beep'
        self.soundbase.clear()
        if buzzer:
            lap_pathname = pathname+'/laps_only'
            self.soundbase.append(None)
            for index in range(1, 10):
                self.soundbase.append(QSound(lap_pathname + '/base' + str(index) + '.wav'))
            self.soundbase.append(None)
        else:
            for index in range(11):
                self.soundbase.append(QSound(lap_pathname+'/base'+str(index)+'.wav'))
        self.entry = None
        if not buzzer:
            self.entry = QSound(pathname+'/entry.wav')

        self.penalty = QSound(pathname+'/penalty.wav')

        self.elapsedtime['30s'] = QSound(pathname+'/start/30s.wav')
        self.elapsedtime['25s'] = QSound(pathname+'/start/25s.wav')
        self.elapsedtime['20s'] = QSound(pathname+'/start/20s.wav')
        self.elapsedtime['15s'] = QSound(pathname+'/start/15s.wav')
        self.elapsedtime['10s'] = QSound(pathname+'/start/10s.wav')
        self.elapsedtime['all'] = QSound(pathname+'/start/startall.wav')

    def sound_time(self, time):
        if (self.play_voice):
            if (platform.system()=='Linux'):
                msg = 'echo "{:0>.2f} seconds" | festival --tts'.format(time)
                os.system(msg)

    def sound_base(self, index):
        if self.play_sound and self.soundbase[index] is not None:
            self.soundbase[index].play()
            for sound in self.elapsedtime:
                if not self.elapsedtime[sound].isFinished():
                    self.elapsedtime[sound].stop()

    def sound_entry(self):
        if self.play_sound and self.entry is not None:
            self.entry.play()

    def sound_penalty(self):
        if self.play_sound:
            self.penalty.play()

    def sound_elapsedTime(self, cmd):
        if self.play_sound:
            if cmd != 'end':
                print('play sound : '+cmd)
                self.elapsedtime[cmd].play()
            else:
                for sound in self.elapsedtime:
                    self.elapsedtime[sound].stop()


    def stop_all(self):
        for sound in self.elapsedtime:
            self.elapsedtime[sound].stop()
        if self.entry is not None:
            self.entry.stop()
        if self.penalty is not None:
            self.penalty.stop()
        for sound in self.soundbase:
            if sound is not None:
                sound.stop()


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    Vocal = chronoQSound(1, 0, 0)
    Vocal.signal_elapsedTime.emit('30s')
    time.sleep(5)
    #Vocal.sound_time(100)
    sys.exit(app.exec_())


