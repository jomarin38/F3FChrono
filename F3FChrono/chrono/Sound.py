#sound.py
#vim: set et sw=4 sts=4 fileencoding=utf-8:

import threading
import time
import os
import platform
import pygame
from F3FChrono.chrono.Chrono import chronoStatus

#https://pythonbasics.org/python-play-sound/
class chronoSound(threading.Thread):
    def __init__(self, sound):
        super(chronoSound, self).__init__()
        self.terminated = False
        self.event = threading.Event()
        self.daemon = True
        self.event.clear()
        self.start()
        self.status=0
        self.lap=0
        self.sound=sound
        


    def check(self, status, lap):
        self.status=status
        self.lap=lap
        if self.sound:
            self.event.set()

    def run(self):
        while not self.terminated:
            # wait until somebody throws an event
            if self.event.wait(0.5):
                if (platform.system() == "Linux"):
                    msg = None
                    # msg='flite -t "' + string +'"'
                    if (self.status == chronoStatus.Launched):
                        msg = 'echo "Launched" | festival --tts'
                    elif (self.status == chronoStatus.InStart):
                        msg = 'echo "In start" | festival --tts'
                    elif (self.status == chronoStatus.InProgress and self.lap == 0):
                        msg = 'echo "Started" | festival --tts'
                    elif (self.status == chronoStatus.InProgress and self.lap > 0):
                        msg = 'echo "{}" | festival --tts'.format(self.lap)
                    elif (self.status == chronoStatus.Finished):
                        msg = 'echo "{:0>6.2f}" | festival --tts'.format(self.lap)

                    if (msg != None):
                        os.system(msg)
                self.event.clear()

            
    def Send (self, msg):
        if (platform.platform() == "Linux"):
            os.system("play -n -C1 synth 0.2 sine 500")
            
class chronoVocal(): #to use this class, it's needed to install festival application. Terminal commande line : sudo apt-get install festival

    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.sound=[]
        pathname = '/home/sdaviet/PycharmProjects/F3FChrono/Sound/'
        for index in range(11):
            self.sound.append(pathname+'base'+str(index)+'.wav')
        self.penalty=pathname+'penalty.wav'
        self.start=pathname+'start.wav'
    def Sound (self, status, chronoLap):
        if (platform.system()=='Linux'):
            msg=None
            #msg='flite -t "' + string +'"'
            if (status==chronoStatus.Launched):
                msg='echo "Launched" | festival --tts'
            elif(status==chronoStatus.InStart):
                msg = 'echo "In start" | festival --tts'
            elif(status==chronoStatus.InProgress and chronoLap==0):
                msg = 'echo "Started" | festival --tts'
            elif(status==chronoStatus.InProgress and chronoLap>0):
                msg = 'echo "Lap {}" | festival --tts'.format(chronoLap)

            if (msg!=None):
                os.system(msg)

    def sound_time (self, time):
        self.waitfinish()
        if (platform.system()=='Linux'):
            msg=None
            msg = 'echo "{:0>.2f} seconds" | festival --tts'.format(time)
            if (msg!=None):
                os.system(msg)

    def sound_base(self, index):
        self.waitfinish()
        pygame.mixer.music.load(self.sound[index])
        pygame.mixer.music.play()

    def sound_penalty(self):
        self.waitfinish()
        pygame.mixer.music.load(self.penalty)
        pygame.mixer.music.play()

    def waitfinish(self):
        while pygame.mixer.music.get_busy() == True:
            continue


        
        
if __name__ == '__main__':

    '''print ("Main start")
    #Sound = chronoSound ()
    Vocal = chronoVocal ()
    #Sound.event.set ()
    Vocal.Sound ("lap 1")
    time.sleep (2)
    #Sound.terminated=True
    #Sound.join ()

    '''
    Vocal=chronoVocal()
    for i in range(11):
        Vocal.sound_base(i)
        time.sleep(1)
        Vocal.waitfinish()
    Vocal.sound_time(50.31)
    Vocal.sound_penalty()
    Vocal.waitfinish()



