#sound.py
#vim: set et sw=4 sts=4 fileencoding=utf-8:

import threading
import time
import os
import platform


class chronoSound(threading.Thread):
    def __init__(self):
        super(chronoSound, self).__init__()
        self.terminated = False
        self.event = threading.Event()
        self.daemon = True
        self.event.clear()
        self.start()
        


    def check(self, value):
        self.event.set()

    def run(self):
        while not self.terminated:
            # wait until somebody throws an event
            if self.event.wait(0.5):
                if (platform.platform() == "linux"):
                    os.system("play -n -C1 synth 0.2 sine 500")
                self.event.clear()
            #else:
            #    os.system("flite -voice slt -t " + vocal)
            
    def Send (self, msg):
        if (platform.platform() == "linux"):
            os.system("play -n -C1 synth 0.2 sine 500")
            
class chronoVocal():
    def Sound (self, string):
        if (platform.platform()=="linux"):
            msg='flite -voice slt -t "' + string +'"'
            print(msg)
            os.system(str(msg))

        print ("todo : Ajouter un message contenant Lap X, In Start, Time : XX.XXX")

        

        
        
if __name__ == '__main__':
    print ("Main start")
    if (True):
        Sound = chronoSound ()
        Vocal = chronoVocal ()
        Sound.event.set ()
        Vocal.Sound ("last lap : 5.01")
        time.sleep (2)
        Sound.terminated=True
        Sound.join ()  
    else :
        Sound = ToneGenerator()
        Sound.play (500, 0.5, 1)
        
        wait (2)
    
    



