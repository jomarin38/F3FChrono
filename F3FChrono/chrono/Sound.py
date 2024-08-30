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

class specialSound():
    def __init__(self, num, already_play = False):
        self.num = num
        self.alreadyPlay = already_play

class noiseGenerator(QThread):

    def __init__(self, playnoise, volume):
        super().__init__()
        self.__debug = False
        pathname = os.path.dirname(os.path.realpath('whitenoise.wav'))
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(pathname + '/whitenoise.wav'))
        if self.__debug:
            print("source : ", self.sound.source(), "Status : ", self.sound.status())
        self.sound.setLoopCount(QSoundEffect.Infinite)
        self.settings(playnoise, volume)

    def settings(self, playnoise, volume):
        self.playnoise = playnoise
        self.sound.setVolume(volume/100)

    def run(self):
        if self.playnoise:
            self.sound.play()

    def stop(self):
        self.sound.stop()

class chronoSound(QSoundEffect):
    def __init__(self, num, source, slot, volume):
        super().__init__()
        self.__debug = False
        try:
            self.number = num
            self.setSource(QUrl.fromLocalFile(source))
            if self.__debug:
                print("Num : ", num, ", source : ", self.source(), "Status : ", self.status())
            self.handleSlot = self.playingChanged.connect(slot)
            self.setVolume(volume)
        except TypeError as e:
            print("QSoundError : ", e, " status : ", self.status(), " number : ", str(num))

    def playSound(self):
        try:
            self.play()
        except TypeError as e:
            print("QSoundError : ", e)

    def stopSound(self):
        try:
            self.stop()
        except TypeError as e:
            print("QSoundError : ", e)

class chronoQSound(QThread):
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_time = pyqtSignal(float, bool, bool)
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
        self.signal_base.connect(self.sound_base)
        self.signal_time.connect(self.sound_time)
        self.signal_penalty.connect(self.sound_penalty)
        self.signal_pilotname.connect(self.sound_pilot)
        self.marginalConditionFlag = False
        self.training = False
        self.chronoStatus = chronoStatus.InWait

        #define constant index
        self.specialsound = collections.OrderedDict()
        self.specialsound['index_dot'] = specialSound(101)
        self.specialsound['index_pilot'] = specialSound(102)
        self.specialsound['index_entry'] = specialSound(103)
        self.specialsound['index_penalty'] = specialSound(104)
        self.specialsound['index_lowvoltage'] = specialSound(105)
        self.specialsound['index_seconds'] = specialSound(106)
        self.specialsound['seconds_thirty'] = specialSound(107)
        self.specialsound['seconds_twentyfive'] = specialSound(108)
        self.specialsound['seconds_twenty'] = specialSound(109)
        self.specialsound['seconds_fifteen'] = specialSound(110)
        self.specialsound['seconds_ten'] = specialSound(111)
        self.specialsound['to_launch'] = specialSound(112)
        self.specialsound['windok'] = specialSound(113)
        self.specialsound['windAlert'] = specialSound(114)
        self.specialsound['marginalCondition'] = specialSound(115)
        self.specialsound['weatherstationlowvoltage'] = specialSound(116)
        self.specialsound['weatherstationsensorslost'] = specialSound(117)
        self.specialsound['tolate'] = specialSound(118)
        self.specialsound['tolate_Entry'] = specialSound(118)
        self.loadwav(volume)
        self.volume = volume
        self.entry_sound = False
        self.entry_soundToLate = False
        self.toLateSound = False
        self.__debug = False

    def loadwav(self, volume):
        self.time = []
        for i in range(0, 119):
            if i==self.specialsound['index_entry'].num:
                self.time.append(chronoSound(i, os.path.join(self.pathname, 'Languages', self.langage, str(i) + '.wav'), \
                                             self.slot_sound_entry, volume))
            else:
                self.time.append(chronoSound(i, os.path.join(self.pathname, 'Languages', self.langage, str(i) + '.wav'),\
                                         self.slot_sound_playing_changed, volume))

    def sound_time(self, run_time, training=False, MCFlag=False):
        self.run_time = run_time
        self.training = training
        self.MCFlag = MCFlag
        if not training:
            self.finaltime_timer.start(2000)
        else:
            self.finaltime_timer.start(300)

    def __final_time(self):
        self.finaltime_timer.stop()
        if self.play_sound:
            if not self.training and self.MCFlag:
                self.__addSound(self.specialsound['marginalCondition'].num)
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
                    self.__addSound(self.specialsound['index_dot'].num)  # add dot wav
                    if x > 0 and x < 10:
                        self.__addSound(0)
                        self.__addSound(x)
                    else:
                        self.__addSound(x)
                        print("sound .XX : " + str(x))


    def sound_pilot(self, bib):
        self.__addSound(self.specialsound['index_pilot'].num)
        self.__addSound(int(bib))

    def slot_lowVoltage(self):
        if self.__debug:
            print("sound low voltage")
        self.__addSound(self.specialsound['index_lowvoltage'].num, lowpriority=True)

    def slot_windAlarm(self, type):
        if type=="windok":
            self.__addSound(self.specialsound['windok'].num)
        elif type=="windalert":
            self.__addSound(self.specialsound['windAlert'].num)
        elif type=="windmarginal":
            if self.__debug:
                print("sot_windalarm Marginal Condition, chronostatus : ", self.chronoStatus)
            if self.chronoStatus == chronoStatus.InWait or self.chronoStatus == chronoStatus.Finished:
                self.__addSound(self.specialsound['marginalCondition'].num)

    def slot_weatherStationLowVoltage(self):
        self.__addSound(self.specialsound['weatherstationlowvoltage'].num, lowpriority=True)

    def slot_weatherStationSensorsLost(self):
        self.__addSound(self.specialsound['weatherstationsensorslost'].num)

    def sound_base(self, index):
        if index < 10:
            self.__addSound(index)

    def sound_entry(self):
        if self.time[self.specialsound['seconds_ten'].num].isPlaying():
            if self.__debug:
                print("sound seconds_ten play and set volume to 0")
            self.time[self.specialsound['seconds_ten'].num].setVolume(0)
        self.specialsound['index_entry'].alreadyPlay = True
        self.time[self.specialsound['index_entry'].num].playSound()

    def sound_penalty(self):
        self.__addSound(self.specialsound['index_penalty'].num)

    def sound_elapsedTime(self, cmd, to_launch):
        if self.__debug:
            print("sound elapsed time : " + str(cmd) + ", to launch" + str(to_launch))
        if 10 <= cmd <= 30:
            if cmd == 30 and to_launch and not self.specialsound['seconds_thirty'].alreadyPlay:
                self.specialsound['seconds_thirty'].alreadyPlay = True
                self.__addSound(self.specialsound['seconds_thirty'].num)
            elif cmd == 30 and not to_launch:
                if self.time[self.specialsound['seconds_ten'].num].isPlaying():
                    if self.__debug:
                        print("sound seconds_ten play and stop it")
                    self.time[self.specialsound['seconds_ten'].num].stopSound()
                    self.specialsound['seconds_ten'].alreadyPlay = False
            elif cmd == 25 and not self.specialsound['seconds_twentyfive'].alreadyPlay:
                self.__addSound(self.specialsound['seconds_twentyfive'].num)
                self.specialsound['seconds_twentyfive'].alreadyPlay = True
            elif cmd == 20 and not self.specialsound['seconds_twenty'].alreadyPlay:
                self.__addSound(self.specialsound['seconds_twenty'].num)
                self.specialsound['seconds_twenty'].alreadyPlay = True
            elif cmd == 15 and not self.specialsound['seconds_fifteen'].alreadyPlay:
                self.__addSound(self.specialsound['seconds_fifteen'].num)
                self.specialsound['seconds_fifteen'].alreadyPlay = True
            elif cmd == 10 and not self.specialsound['seconds_ten'].alreadyPlay:
                self.__addSound(self.specialsound['seconds_ten'].num)
                self.specialsound['seconds_ten'].alreadyPlay = True

    def sound_toLate(self):
        self.__addSound(self.specialsound['tolate'].num)
        self.specialsound['tolate'].alreadyPlay = True

    def sound_toLateEntry(self):
        self.__addSound(self.specialsound['tolate_Entry'].num)
        self.specialsound['tolate_Entry'].alreadyPlay = True

    def stop_Timing(self):
        if self.time[self.specialsound['seconds_ten'].num].isPlaying():
            self.time[self.specialsound['seconds_ten'].num].stopSound()
            self.specialsound['seconds_ten'].alreadyPlay = False

    def stop_all(self):
        if self.__debug:
            print("stop_all")
        if len(self.sound_list) > 0:
            for i in range(len(self.sound_list)-1, -1, -1):
                self.sound_list[i].stopSound()
            self.sound_list.clear()
        for key in self.specialsound.keys():
            self.specialsound[key].alreadyPlay = False

    def __addSound(self, num, play=True, lowpriority=False):
        if self.play_sound:
            if lowpriority:
                if self.__debug:
                    print("add low priority sound", str(num))
                self.sound_lowPriority.append(num)
                self.checklowPrioritySound()
            else:
                #if not self.time[num].isPlaying(): #fix issue for time like 45.45
                if self.__debug:
                    print("add sound", str(num))

                self.sound_list.append(self.time[num])
                if play and len (self.sound_list) == 1:
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
        if self.__debug:
            print("sound slot status changed : ", str(status))
        if (status == chronoStatus.InStartLate) and not self.specialsound['tolate'].alreadyPlay \
                and not self.specialsound['tolate_Entry'].alreadyPlay:
            if self.__debug:
                print("sound self.to_late")
            self.sound_toLate()
        elif (status == chronoStatus.Late) and not self.specialsound['tolate_Entry'].alreadyPlay:
            if self.__debug:
                print("sound self.to_lateEntry")
            self.sound_toLateEntry()
        elif (status == chronoStatus.InStart or status == chronoStatus.InStartLate):
            self.sound_entry()
        elif status == chronoStatus.Launched:
            self.specialsound['seconds_thirty'].alreadyPlay = False
            self.specialsound['seconds_twentyfive'].alreadyPlay = False
            self.specialsound['seconds_twenty'].alreadyPlay = False
            self.specialsound['seconds_fifteen'].alreadyPlay = False
            self.specialsound['seconds_ten'].alreadyPlay = False
        elif status == chronoStatus.InWait or status == chronoStatus.Finished:
            for key in self.specialsound.keys():
                self.specialsound[key].alreadyPlay = False

    def slot_sound_playing_changed(self):
        soundPlaying = [p.number for p in self.time if p.isPlaying()]
        if len(soundPlaying)>0:
            if self.__debug:
                print("slot sound play", soundPlaying)
        if len(self.sound_list) > 0:
            if not self.sound_list[0].isPlaying():
                self.sound_list[0].stopSound()
                del self.sound_list[0]
                if len(self.sound_list) > 0:
                    self.sound_list[0].playSound()

    def slot_sound_entry(self):
        if self.specialsound['index_entry'].alreadyPlay:
            if self.__debug:
                print("slot sound entry and check ten seconds is playing to setVolume")
            if not self.time[self.specialsound['index_entry'].num].isPlaying():
                self.specialsound['index_entry'].alreadyPlay = False
                if self.time[self.specialsound['seconds_ten'].num].isPlaying():
                    self.time[self.specialsound['seconds_ten'].num].setVolume(self.volume)


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)

    Vocal = chronoQSound(os.path.dirname(os.path.dirname(os.getcwd())), "French", 1, 100)
    Vocal.sound_toLate()
    Vocal.sound_elapsedTime(30, False)
    time.sleep(5)
    #Vocal.sound_time(45.45)
    Vocal.signal_time.emit(45.45, False)
    time.sleep(5)
    try:
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        pass
    finally:
        pass