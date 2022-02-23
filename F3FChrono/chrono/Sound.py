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
from F3FChrono.chrono.Chrono import chronoStatus

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

class chronoSound(QSoundEffect):
    def __init__(self, source, slot, volume):
        super().__init__()
        self.__debug = False
        try:

            self.setSource(QUrl.fromLocalFile(source))
            if self.__debug:
                print(self.source(), "Status : ", self.status())
            self.handleSlot = self.playingChanged.connect(slot)
            self.setVolume(volume)
            self.InProgress = False


        except TypeError as e:
            print("QSoundError : ", e, " status : ", self.status())

    def playSound(self):
        try:
            self.play()
            self.InProgress = True
        except TypeError as e:
            print("QSoundError : ", e)

    def stopSound(self):
        try:
            self.stop()
            self.InProgress = False
        except TypeError as e:
            print("QSoundError : ", e)

class chronoQSound(QThread):
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_entry = pyqtSignal()
    signal_time = pyqtSignal(float, bool)
    signal_elapsedTime = pyqtSignal(int, bool)
    signal_start = pyqtSignal(int)
    signal_pilotname = pyqtSignal(int)


    def __init__(self, pathname, langage, playsound, volume):
        super().__init__()
        self._translate = QtCore.QCoreApplication.translate
        self.pathname = pathname
        self.langage = langage
        self.finaltime_timer = QtCore.QTimer()
        self.finaltime_timer.timeout.connect(self.__final_time)
        self.play_sound = playsound
        self.sound_list = []
        self.sound_lowPriority = []
        self.signal_elapsedTime.connect(self.sound_elapsedTime)
        self.signal_entry.connect(self.sound_entry)
        self.signal_base.connect(self.sound_base)
        self.signal_time.connect(self.sound_time)
        self.signal_penalty.connect(self.sound_penalty)
        self.signal_pilotname.connect(self.sound_pilot)
        self.marginalConditionFlag = False
        self.training = False
        self.chronoStatus = chronoStatus.InWait

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
        self.windok = 113
        self.windAlert = 114
        self.marginalCondition=115
        self.weatherstationlowvoltage=116
        self.weatherstationsensorslost=117
        self.loadwav(volume)
        self.__debug = True

    def loadwav(self, volume):
        self.time = []
        for i in range(0, 118):
            self.time.append(chronoSound(os.path.join(self.pathname, 'Languages', self.langage, str(i) + '.wav'),\
                                         self.slot_sound_playing_changed, volume))


    def sound_time(self, run_time, training=False):
        self.run_time = run_time
        self.training = training
        if not training:
            self.finaltime_timer.start(2000)
        else:
            self.finaltime_timer.start(300)

    def __final_time(self):
        self.finaltime_timer.stop()
        if self.play_sound:
            if not self.training and self.marginalConditionFlag:
                self.__addSound(self.marginalCondition)
                self.marginalConditionFlag = False
            else:
                # decompose numeric time to find cent, diz, 1/100
                var_time = Decimal("{:0.2f}".format(self.run_time))
                cent, diz = divmod(var_time, 100)
                x = int(var_time % 1 * 100)

                # create sequence sound
                if int(cent) > 0:
                    self.__addSound(int(cent * 100))
                    if int(diz) > 0:
                        self.__addSound(int(diz))
                else:
                    self.__addSound(int(diz))

                if x < 100:
                    self.__addSound(self.index_dot)  # add dot wav
                    if x > 0 and x < 10:
                        self.__addSound(0)
                        self.__addSound(x)
                    else:
                        self.__addSound(x)


    def sound_pilot(self, bib):
        self.__addSound(self.index_pilot)
        self.__addSound(int(bib))

    def slot_lowVoltage(self):
        if self.__debug:
            print("sound low voltage")
        self.__addSound(self.index_lowvoltage, lowpriority=True)

    def slot_windAlarm(self, type):
        if type=="windok":
            self.__addSound(self.windok)
        elif type=="windalert":
            self.__addSound(self.windAlert)
        elif type=="windmarginal":
            self.marginalConditionFlag = True

    def slot_weatherStationLowVoltage(self):
        self.__addSound(self.weatherstationlowvoltage, lowpriority=True)

    def slot_weatherStationSensorsLost(self):
        self.__addSound(self.weatherstationsensorslost)

    def sound_base(self, index):
        if index < 10:
            self.__addSound(index)

    def sound_entry(self):
        self.__addSound(self.index_entry)

    def sound_penalty(self):
        self.__addSound(self.index_penalty)

    def sound_elapsedTime(self, cmd, to_launch):
        if self.__debug:
            print("sound elapsed time : " + str(cmd) + ", to launch" + str(to_launch))
        if 10 <= cmd <= 30:
            if cmd == 30 and to_launch:
                self.__addSound(self.seconds_thirty)
            elif cmd == 25:
                self.__addSound(self.seconds_twentyfive)
            elif cmd == 20:
                self.__addSound(self.seconds_twenty)
            elif cmd == 15:
                self.__addSound(self.seconds_fifteen)
            elif cmd == 10:
                self.__addSound(self.seconds_ten)

    def stop_all(self):
        #print("stop_all")
        if len(self.sound_list) > 0:
            for i in range(len(self.sound_list)-1, -1, -1):
                self.sound_list[i].stop()
            self.sound_list.clear()

    def __addSound(self, num, play=True, lowpriority=False):
        if self.play_sound:
            if lowpriority:
                if self.__debug:
                    print("low priority sound", str(num))
                self.sound_lowPriority.append(num)
                self.checklowPrioritySound()
            else:
                if not self.time[num].isPlaying():
                    self.sound_list.append(self.time[num])
                    if play and len (self.sound_list) == 1 and not lowpriority:
                        self.sound_list[0].playSound()

    def checklowPrioritySound(self):
        if self.chronoStatus == chronoStatus.InWait or self.chronoStatus == chronoStatus.Finished:
            play = len(self.sound_list)==0
            if self.__debug:
                print("Check low priority sound, nb sound in list : ", str(len(self.sound_lowPriority)))
                print("nb sound list : ", str(len(self.sound_list)))
            if len(self.sound_lowPriority)>0:
                for x in self.sound_lowPriority:
                    self.__addSound(x)
                self.sound_lowPriority.clear()

    def slot_status_changed(self, status):
        self.chronoStatus = status
        self.checklowPrioritySound()

    def slot_sound_playing_changed(self):
        if self.__debug:
            print("slot sound")
        if len(self.sound_list) > 0:
            if not self.sound_list[0].isPlaying():
                self.sound_list[0].stop()
                del self.sound_list[0]
                if len(self.sound_list) > 0:
                    self.sound_list[0].playSound()


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)

    Vocal = chronoQSound(os.path.dirname(os.path.dirname(os.getcwd())), "French", 1, 100)
    Vocal.signal_elapsedTime.emit(30, False)
    time.sleep(5)
    Vocal.sound_time(100)
    time.sleep(5)
    try:
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        pass
    finally:
        pass