#!/usr/bin/env python
# vim: set et sw=4 sts=4 fileencoding=utf-8:
import os
import re
import sys
import logging
from time import sleep
from argparse import ArgumentParser
from PyQt5 import QtWidgets
from F3FChrono import chrono


def get_raspi_revision():
    rev_file = '/sys/firmware/devicetree/base/model'
    info = { 'pi': '', 'model': '', 'rev': ''}
    raspi = model = revision = ''
    try:
        fd = os.open(rev_file, os.O_RDONLY)
        line = os.read(fd,256)
        os.close(fd)
        m = re.match('Raspberry Pi (\d+) Model (\w(?: Plus)?) Rev ([\d\.]+)', line)
        if m:
            info['pi'] = m.group(1)
            info['model'] = m.group(2)
            info['rev'] = m.group(3)
    except:
        pass

    return info

def terminateApp (thread1, thread2, thread3, thread4):
    if not (thread1==None):
        thread1.terminated = True
    if not (thread3==None):
        thread3.terminate()
    if not (thread4==None):
        thread4.terminated = True
    # wait and join threads
    sleep(0.5)
    if not (thread1==None):
        thread1.join()
    if not (thread2==None):
        thread2.join ()
    if not (thread3==None):
        thread3.join()
    if not (thread4==None):
        thread4.join()
    
    print ("terminate")   

def main():
    global config
    
    logging.basicConfig (filename="runchrono.log", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')    
    print(get_raspi_revision())
    
    print("warm-up 2 seconds...")
    sleep(2.0)
    print("...start")
    
    if (config.conf['display']):
        app=QtWidgets.QApplication(sys.argv)
        myapp = F3FChrono.chrono.Chronoui.MyForm ()
        myapp.show()
    
    Chrono = F3FChrono.chrono.Chrono.chrono (F3FChrono.chrono.Chrono.chronoMode.Practice)
    greenLED = F3FChrono.chrono.GPIOPort.gpioPort(config.conf['greenLEDPort'], is_active_low=config.conf['ledActiveLow'], duration=config.conf['signalLength'], start_blinks=3)
    if (config.conf['sound']):
        SoundBeep = F3FChrono.chrono.Sound.chronoSound ()
    else:
        SoundBeep=None
    if (config.conf['vocal']):
        vocal= chrono.chronoVocal()
    else:
        vocal=None
    #redLED = chrono.GPIOPort.gpioPort(config.conf['redLEDPort'],
    #    duration=config.conf['signalLength'],
    #    is_active_low=config.conf['ledActiveLow'])
    if (config.conf['display']):
        eventUI = myapp.GetBaseEventID ()
        eventUI.signalID.connect (myapp.UpdateHMI)
    else:
        eventUI=None
        
    if (config.conf['sound']):
        eventUI.signalID.connect (SoundBeep.Send)
    if (config.conf['vocal']):
        eventUI.signalID.connect (vocal.Sound)
    
    udpReceive = F3FChrono.chrono.UDPReceive.udpreceive(config.conf['IPUDPPORT'], Chrono, greenLED, eventUI)
    udpBeep = F3FChrono.chrono.UDPBeep.udpBeep(config.conf['IPUDPBEEP'], config.conf['IPUDPPORT'])
    
    sleep(1.0)
    print("...start")
    F3FChrono.chrono.GPIOPort.statusLED(config.conf['statusLEDPort'], on=True)
    


    try:
        #writer.setupDecoder()
        loop=0
        testEnd=False
        if (config.conf['display']):
            print("lancement IHM")
            sys.exit(app.exec_())
    
        while not testEnd:
            cmdline=sys.stdin.readline ()
            print (cmdline, testEnd)
            if (cmdline=='reset\n'):
                print ('reset ()')
                Chrono.reset ()
                Chrono.start (F3FChrono.chrono.Chrono.chronoMode.Practice)
            elif (cmdline=='start\n'):
                print ('Start ()')
                Chrono.startRace ()
            elif (cmdline=="value\n"):
                print ('Numero de base ', Chrono.getLapCount ())
                print ('Last Lap : ', Chrono.getLastLapTime ())
                print ('10LastLap : ', Chrono.getLast10BasesTime())
                print ('10LastLapLost : ', Chrono.getLast10BasesLostTime())
            elif (cmdline=="q\n"):
                testEnd = True
                
    except KeyboardInterrupt:
        pass
    finally:
        terminateApp (greenLED, udpReceive, udpBeep, SoundBeep)
        F3FChrono.chrono.GPIOPort.statusLED(config.conf['statusLEDPort'], on=False)
        
if __name__ == '__main__':
    parser = ArgumentParser(prog='chrono')
    #parser.add_argument('show=false')
    args = parser.parse_args()
    global config
    config = chrono.Configuration('config.json')
    #os.system("[ ! -d /run/picamtracker ] && sudo mkdir -p /run/picamtracker && sudo chown pi:www-data /run/picamtracker && sudo chmod 775 /run/picamtracker")
    
    main()
