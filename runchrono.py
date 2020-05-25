import os
import re
import sys
import subprocess
import time

from argparse import ArgumentParser
from PyQt5 import QtWidgets, QtCore
import os.path

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

pi=get_raspi_revision()
if pi['pi'] == '':
    # Replace libraries by fake ones
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
    from fake_rpi import toggle_print

    # by default it prints everything to std.error
    toggle_print(False)  # turn on/off printing

from F3FChrono.chrono import ConfigReader
from F3FChrono.gui.MainUiController import MainUiCtrl
from F3FChrono.data.Chrono import Chrono
from F3FChrono.data.dao.EventDAO import EventDAO
from F3FChrono.gui.Simulate_base import SimulateBase
from F3FChrono.data.web.Utils import Utils



def main():

    #logging.basicConfig (filename="runchrono.log", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    pi=get_raspi_revision()
    if(pi['pi']!=''):
        print("warm-up 2 seconds...")
        time.sleep(2.0)

    webserver_process = None

    if ConfigReader.config.conf['run_webserver']:
        Utils.set_port_number(ConfigReader.config.conf['webserver_port'])
        if Utils.server_alive():
            print('Webserver already running.')
        else:
            print("Starting webserver ...")
            manage_py_path = os.path.realpath('F3FChrono/web')
            webserver_process = \
                subprocess.Popen(['python3', os.path.join(manage_py_path, 'manage.py'), 'runserver', '0.0.0.0:'
                                  +str(ConfigReader.config.conf['webserver_port'])],
                                 shell=False)

    print("...start")

    dao = EventDAO()
    chronodata = Chrono()


    app = QtWidgets.QApplication(sys.argv)
    ui = MainUiCtrl(dao, chronodata, rpi=pi['pi'], webserver_process=webserver_process)

    if not os.path.isfile('voltage_log.txt'):
        MainUiCtrl.startup_time = time.time()
    else:
        with open("voltage_log.txt", "r") as file:
            first_line = file.readline()
            MainUiCtrl.startup_time = float(first_line.split(',')[0])


    #launched simulate mode
    if (ConfigReader.config.conf['simulatemode']):
        ui_simulate=SimulateBase()
        ui_simulate.close_signal.connect(ui.MainWindow.close)
        ui.close_signal.connect(ui_simulate.MainWindow.close)

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
    ConfigReader.config = ConfigReader.Configuration('config.json')

    main()
