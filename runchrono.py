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
from F3FChrono.chrono.UDPReceive import udpreceive
from F3FChrono.chrono.UDPBeep import udpbeep
from F3FChrono.gui.Simulate_base import SimulateBase

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

def main():
    global config
    
    #logging.basicConfig (filename="runchrono.log", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    pi=get_raspi_revision()
    if(pi['pi']!=''):
        print("warm-up 2 seconds...")
        sleep(2.0)

    print("...start")

    dao = EventDAO()
    chronodata = Chrono()
    chronohard = ChronoHard()

    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(dao, chronodata, chronohard, config.conf['sound'])
    udpReceive=udpreceive(config.conf['UDPPORT'], ui.refresh_chronoui)
    udpBeep=udpbeep(config.conf['IPUDPBEEP'], config.conf['UDPPORT'])

    #launched simulate mode
    if (config.conf['simulate']):
        ui_simulate=SimulateBase()

    try:
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        pass
    finally:
        udpBeep.terminate()
        #udpReceive.event.join()
        pass

if __name__ == '__main__':
    parser = ArgumentParser(prog='chrono')
    #parser.add_argument('show=false')
    args = parser.parse_args()
    global config
    config = Configuration ('config.json')

    main()
