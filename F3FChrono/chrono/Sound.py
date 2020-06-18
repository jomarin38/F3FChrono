import time
import os
import sys
import platform
import collections
from F3FChrono.chrono import ConfigReader
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QCoreApplication, QUrl
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QSound, QSoundEffect
from F3FChrono.chrono import ConfigReader
import pyttsx3



class chronoQSound(QThread):
    signal_penalty = pyqtSignal()
    signal_base = pyqtSignal(int)
    signal_entry = pyqtSignal()
    signal_time = pyqtSignal(float)
    signal_elapsedTime = pyqtSignal(str)
    signal_start = pyqtSignal(int)
    signal_pilotname = pyqtSignal(str, str)
    signal_lowVoltage = pyqtSignal()


    def __init__(self, langage, playsound, playvoice, voicerate, buzzer):
        super().__init__()
        self._translate = QtCore.QCoreApplication.translate
        self.soundbase = []
        self.elapsedtime = collections.OrderedDict()
        self.elapsedtime_play = collections.OrderedDict()
        self.settings(playsound, playvoice)
        self.loadwav(langage, buzzer)
        self.signal_elapsedTime.connect(self.sound_elapsedTime)
        self.signal_entry.connect(self.sound_entry)
        self.signal_base.connect(self.sound_base)
        self.signal_time.connect(self.sound_time)
        self.signal_penalty.connect(self.sound_penalty)
        self.signal_pilotname.connect(self.pilot)
        self.signal_lowVoltage.connect(self.lowVoltage)
        self.soundstart_run = False
        self.voice_engine = pyttsx3.init()
        self.voice_engine.setProperty('rate', voicerate)
        self.voice_engine.setProperty('volume', 1)

        self.voice_engine.connect('finished-utterance', self.onVoiceEnd)
        self.voice_engine.setProperty('voice', langage.lower())

        self.nextpilot = self._translate("Next pilot : ", "Next pilot : ")
        self.lowVoltagestr = self._translate("Low Voltage", "Low Voltage")
        #self.voices = self.voice_engine.getProperty('voices')
        #self.voice_engine.setProperty('voice', self.voices[26].id)

    def settings(self, playsound, playvoice):
        self.play_sound = playsound
        self.play_voice = playvoice

    def loadwav(self, langage, buzzer):
        pathname = os.path.dirname(os.path.realpath('Languages/'+langage+'/base0.wav'))
        self.soundbase.clear()
        lap_pathname = pathname+'/laps_only'
        self.soundbase.append(None)
        for index in range(1, 10):
            self.soundbase.append(QSound(lap_pathname + '/base' + str(index) + '.wav'))
        self.soundbase.append(None)
        self.entry = None
        self.entry = QSound(pathname+'/instart.wav')
        self.penalty = QSound(pathname+'/penalty.wav')

        self.elapsedtime['30s'] = QSound(pathname+'/start/30s.wav')
        self.elapsedtime['25s'] = QSound(pathname+'/start/25s.wav')
        self.elapsedtime['20s'] = QSound(pathname+'/start/20s.wav')
        self.elapsedtime['15s'] = QSound(pathname+'/start/15s.wav')
        self.elapsedtime['10s'] = QSound(pathname+'/start/10s.wav')
        #self.elapsedtime['all'] = QSound(pathname+'/start/startall.wav')

    def sound_time(self, run_time):
        if (self.play_voice):
            self.voice_engine.say("{:0>.2f}".format(run_time))
            self.start()

    def pilot(self, first_name, name):
        if self.play_voice:
            self.voice_engine.say(self.nextpilot + first_name + " " + name)
            self.start()

    def lowVoltage(self):
        if self.play_voice:
            self.voice_engine.say(self.lowVoltagestr)
            self.start()

    def run(self):
        self.voice_engine.startLoop()


    def onVoiceEnd(self, name, completed):
        self.voice_engine.endLoop()
        self.stop()

    def sound_base(self, index):
        if self.play_sound and self.soundbase[index] is not None:
            self.soundbase[index].play()

    def sound_entry(self):
        if self.play_sound and self.entry is not None:
            self.entry.play()



    def sound_penalty(self):
        if self.play_sound:
            self.penalty.play()

    def sound_elapsedTime(self, cmd):
        if self.play_sound:
            if cmd != 'end' and self.elapsedtime[cmd].isFinished():
                print('play sound : '+cmd)
                self.elapsedtime[cmd].play()
            if cmd == 'end':
                self.stop_elapsedTime()

    def stop_elapsedTime(self):
        for sound in self.elapsedtime:
            self.elapsedtime[sound].stop()

    def stop_all(self):
        self.stop_elapsedTime ()
        if self.entry is not None:
            self.entry.stop()
        if self.penalty is not None:
            self.penalty.stop()
        for sound in self.soundbase:
            if sound is not None:
                sound.stop()


class noiseGenerator(QThread):

    def __init__(self, playnoise, volume):
        super().__init__()
        pathname = os.path.dirname(os.path.realpath('F3FChrono/chrono/whitenoise.wav'))
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

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    Vocal = chronoQSound("French", 1, 1, 0)
    #Vocal.signal_elapsedTime.emit('30s')
    #time.sleep(5)
    Vocal.sound_time(100)
    time.sleep(5)
    sys.exit(app.exec_())



