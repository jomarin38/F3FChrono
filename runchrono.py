import os
import re
import sys
from time import sleep
from argparse import ArgumentParser
from PyQt5 import QtWidgets
from F3FChrono.chrono import ConfigReader
from F3FChrono.gui.MainUiController import MainUiCtrl
from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.dao.EventDAO import EventDAO
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
        m=re.split(r'\s', line.decode('utf-8'))
        if m:
            info['pi'] = m[3]
            info['model'] = m[5]
        return info
    except:
        pass
    return info

def main():

    #logging.basicConfig (filename="runchrono.log", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    pi=get_raspi_revision()
    if(pi['pi']!=''):
        print("warm-up 2 seconds...")
        sleep(2.0)

    print("...start")

    dao = EventDAO()
    chronodata = Chrono()


    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(dao, chronodata, rpi=pi['pi'])

    #launched simulate mode
    if (ConfigReader.config.conf['simulatemode']):
        ui_simulate=SimulateBase()

    try:
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        pass
    finally:
        pass


if __name__ == '__main__':
    parser = ArgumentParser(prog='chrono')
    #parser.add_argument('show=false')
    args = parser.parse_args()

    ConfigReader.init()
    ConfigReader.config = ConfigReader.Configuration ('config.json')

    main()
