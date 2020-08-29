import time
import os
import sys
from decimal import Decimal
import platform
import collections
from F3FChrono.chrono import ConfigReader
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QCoreApplication, QUrl
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QSound, QSoundEffect
from F3FChrono.chrono import ConfigReader


class noiseGenerator(QThread):

    def __init__(self, playnoise, volume):
        super().__init__()
        pathname = os.path.dirname(os.path.realpath('whitenoise.wav'))
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(pathname + '/whitenoise.wav'))

        self.sound.setLoopCount(QSoundEffect.Infinite)
        self.settings(playnoise, volume)

    def settings(self, playnoise, volume):
        self.playnoise = playnoise
        self.sound.setVolume(volume)

    def run(self):
        if self.playnoise:
            self.sound.play()

    def stop(self):
        self.sound.stop()

class chronoQSound(QThread):
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_entry = pyqtSignal()
    signal_time = pyqtSignal(float)
    signal_elapsedTime = pyqtSignal(int, bool)
    signal_start = pyqtSignal(int)
    signal_pilotname = pyqtSignal(int)
    signal_lowVoltage = pyqtSignal()


    def __init__(self, pathname, langage, playsound, volume):
        super().__init__()
        self._translate = QtCore.QCoreApplication.translate
        self.pathname = pathname
        self.langage = langage
        self.play_sound = playsound
        self.loadwav(volume)
        self.signal_elapsedTime.connect(self.sound_elapsedTime)
        self.signal_entry.connect(self.sound_entry)
        self.signal_base.connect(self.sound_base)
        self.signal_time.connect(self.sound_time)
        self.signal_penalty.connect(self.sound_penalty)
        self.signal_pilotname.connect(self.sound_pilot)
        self.signal_lowVoltage.connect(self.lowVoltage)
        self.sound_list = []

        #define constant index
        self.index_dot = 101
        self.index_pilot = 102
        self.index_entry = 103
        self.index_penalty = 104
        self.index_lowvoltage = 105
        self.index_seconds = 106
        self.seconds_thirty = 107
        self.seconds_twentyfive = 108
        self.seconds_twenty = 109
        self.seconds_fifteen = 110
        self.seconds_ten = 111
        self.to_launch = 112


    def loadwav(self, volume):
        try:
            self.time = []
            for i in range(0, 113):
                self.time.append(QSoundEffect())
                self.time[i].setSource(QUrl.fromLocalFile(
                    os.path.join(self.pathname, 'Languages', self.langage, str(i) + '.wav')))
                self.time[i].playingChanged.connect(self.slot_sound_playing_changed)
                self.time[i].setVolume(volume)
        except TypeError as e:
            print("QSoundError : ", e)

    def sound_time(self, run_time):
        self.stop_all()
        if self.play_sound:
            # decompose numeric time to find cent, diz, 1/100
            cent, diz = divmod(int(run_time), 100)
            x = int(Decimal("{:>6.2f}".format(run_time)) % 1 * 100)

            # create sequence sound
            if int(cent) > 0:
                self.sound_list.append(int(cent * 100))
                if int(diz) > 0:
                    self.sound_list.append(int(diz))
            else:
                self.sound_list.append(int(diz))

            if x < 100:
                self.sound_list.append(self.index_dot)  # add dot wav
                if x > 0 and x < 10:
                    self.sound_list.append(0)
                    self.sound_list.append(x)
                else:
                    self.sound_list.append(x)
            self.__start_play()

    def sound_pilot(self, bib):
        self.stop_all()
        if self.play_sound:
            self.sound_list.clear()
            self.sound_list.append(self.index_pilot)
            self.sound_list.append(int(bib))
            self.__start_play()

    def lowVoltage(self):
        self.stop_all()
        if self.play_sound:
            self.sound_list.append(self.index_lowvoltage)
            self.__start_play()

    def sound_base(self, index):
        self.stop_all()
        if self.play_sound and index < 10:
            self.sound_list.append(index)
            self.__start_play()

    def sound_entry(self):
        self.stop_all()
        if self.play_sound:
            self.sound_list.append(self.index_entry)
            self.__start_play()

    def sound_penalty(self):
        self.stop_all()
        if self.play_sound:
            self.sound_list.append(self.index_penalty)
            self.__start_play()

    def sound_elapsedTime(self, cmd, to_launch):
        if self.play_sound:
            if 10 <= cmd <= 30:
                self.stop_all()
                if cmd == 30:
                    self.sound_list.append(self.seconds_thirty)
                    if to_launch:
                        self.sound_list.append(self.to_launch)
                elif cmd == 25:
                    self.sound_list.append(self.seconds_twentyfive)
                elif cmd == 20:
                    self.sound_list.append(self.seconds_twenty)
                elif cmd == 15:
                    self.sound_list.append(self.seconds_fifteen)
                elif cmd == 10:
                    self.sound_list.append(self.seconds_ten)
                if len(self.sound_list) > 0:
                    self.__start_play()
        print(self.sound_list)

    def stop_all(self):
        if len(self.sound_list) > 0:
            for i in range(0, len(self.sound_list)-1, -1):
                self.time[self.sound_list[i]].stop()
            self.sound_list.clear()

    def __start_play(self):
        self.time[self.sound_list[0]].play()
        '''#debug sound list to play
        print(self.sound_list)
        print(str(self.time[self.sound_list[0]].status()) + ', ' + str(QSoundEffect.Ready))
        print(self.time[self.sound_list[0]].isPlaying())
        '''
        if not self.time[self.sound_list[0]].isPlaying():
            print("not playing")
            self.time[self.sound_list[0]].stop()
            self.time[self.sound_list[0]].play()

    def slot_sound_playing_changed(self):
        if len(self.sound_list) > 0:
            if not self.time[self.sound_list[0]].isPlaying():
                self.time[self.sound_list[0]].stop()
                del self.sound_list[0]
                if len(self.sound_list) > 0:
                    self.time[self.sound_list[0]].play()


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    Vocal = chronoQSound("French", 1, 1, 0)
    #Vocal.signal_elapsedTime.emit('30s')
    #time.sleep(5)
    Vocal.sound_time(100)
    time.sleep(5)
    sys.exit(app.exec_())



