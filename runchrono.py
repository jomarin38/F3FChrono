#!/usr/bin/env python
# vim: set et sw=4 sts=4 fileencoding=utf-8:
import os
import re
import sys
import logging
from time import sleep
from argparse import ArgumentParser
from PyQt5 import QtWidgets
from F3FChrono.chrono.ConfigReader import Configuration
from F3FChrono.chrono.Chrono import ChronoHard
from F3FChrono.gui.MainUiController import MainUiCtrl
from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.dao.EventDAO import EventDAO

def get_raspi_revision():
    rev_file = '/sys/firmware/devicetree/base/model'
    info = { 'pi': '', 'model': '', 'rev': ''}
    raspi = model = revision = ''
    try:
        fd = os.open(rev_file, os.O_RDONLY)
        line = os.read(fd,256)
        os.close(fd)
        print (line)
        m = re.match('Raspberry Pi (\d+) Model (\w(?: Plus)?) Rev ([\d\.]+)', line)
        if m:
            info['pi'] = m.group(1)
            info['model'] = m.group(2)
            info['rev'] = m.group(3)
    except:
        pass

    return info

'''def terminateApp (thread1, thread2, thread3, thread4):
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
'''

def main():
    global config
    
    logging.basicConfig (filename="runchrono.log", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')    
    pi=get_raspi_revision())
    if(pi[0]!=''):
        print("warm-up 2 seconds...")
        sleep(2.0)

    print("...start")

    dao = EventDAO()
    chronodata = Chrono()
    chronohard = ChronoHard()
    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(dao, chronodata, chronohard)


    try:
        # writer.setupDecoder()
        print("lancement IHM")
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        pass
    finally:
        pass

if __name__ == '__main__':
    parser = ArgumentParser(prog='chrono')
    #parser.add_argument('show=false')
    args = parser.parse_args()
    global config
    config = Configuration ('config.json')
    #os.system("[ ! -d /run/picamtracker ] && sudo mkdir -p /run/picamtracker && sudo chown pi:www-data /run/picamtracker && sudo chmod 775 /run/picamtracker")
    
    main()
