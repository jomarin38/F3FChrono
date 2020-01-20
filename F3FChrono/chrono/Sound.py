#sound.py
#vim: set et sw=4 sts=4 fileencoding=utf-8:

import threading
import time
import os
import platform
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


        

        
        
if __name__ == '__main__':
    print ("Main start")
    #Sound = chronoSound ()
    Vocal = chronoVocal ()
    #Sound.event.set ()
    Vocal.Sound ("lap 1")
    time.sleep (2)
    #Sound.terminated=True
    #Sound.join ()

    



