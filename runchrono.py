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

import os
import re
import sys
import subprocess
import time

from argparse import ArgumentParser
from PyQt5 import QtWidgets, QtCore
from F3FChrono.Utils import is_running_on_pi
import os.path

if not is_running_on_pi():
    # Replace libraries by fake ones
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
    from fake_rpi import toggle_print

    # by default it prints everything to std.error
    toggle_print(False)  # turn on/off printing


def main(webservice_only=False):

    #logging.basicConfig (filename="runchrono.log", level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    if is_running_on_pi():
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

            subprocess.Popen(['celery', '-A', 'administrator',  'worker', '-l', 'info'], cwd=manage_py_path, shell=False)

    print("...start")

    if not webservice_only:

        dao = EventDAO()
        chronodata = Chrono()

        app = QtWidgets.QApplication(sys.argv)
        ui = MainUiCtrl(dao, chronodata, rpi=is_running_on_pi(), webserver_process=webserver_process)

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
    else:
        webserver_process.communicate()


if __name__ == '__main__':
    parser = ArgumentParser(prog='chrono')
    parser.add_argument('--webservice-only', action="store_true")
    parser.add_argument('--external-webserver')
    args = parser.parse_args()

    from F3FChrono.chrono import ConfigReader

    ConfigReader.init()
    ConfigReader.config = ConfigReader.Configuration('config.json')

    from F3FChrono.gui.MainUiController import MainUiCtrl
    from F3FChrono.data.Chrono import Chrono
    from F3FChrono.data.dao.EventDAO import EventDAO
    from F3FChrono.gui.Simulate_base import SimulateBase
    from F3FChrono.data.web.Utils import Utils

    if args.external_webserver is not None:
        Utils.set_external_webserver_IP(args.external_webserver)

    main(args.webservice_only)
