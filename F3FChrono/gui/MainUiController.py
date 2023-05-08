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

from F3FChrono.chrono import ConfigReader
from F3FChrono.data.Round import Round
from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.gui.Simulate_base import SimulateBase
from F3FChrono.chrono.Chrono import *
from F3FChrono.data.dao.EventDAO import EventDAO, RoundDAO
from F3FChrono.data.Chrono import Chrono
from F3FChrono.chrono.Sound import *
from F3FChrono.chrono.GPIOPort import rpi_gpio
from F3FChrono.chrono.UDPSend import *
from F3FChrono.data.web.Utils import Utils
from F3FChrono.Utils import get_ip
from F3FChrono.chrono.TCPServer import tcpServer
import os


class MainUiCtrl(QtWidgets.QMainWindow):
    close_signal = pyqtSignal()
    startup_time = None

    def __init__(self, eventdao, chronodata, rpi, webserver_process):
        super().__init__()
        self.__debug=True
        self.webserver_process = webserver_process
        self.daoEvent = eventdao
        self.daoRound = RoundDAO()
        self.event = None
        self.rpigpio = rpi_gpio(rpi)
        self.chronodata = chronodata
        self.chronoHard = ChronoArduino(self.rpigpio.signal_btn_next)
        self.base_test = -10

        if ConfigReader.config.conf['language'] != "English":
            _translator = QtCore.QTranslator()
            _path = os.path.join(os.getcwd(), 'Languages', ConfigReader.config.conf['language'] + '.qm')
            _translator.load(_path)
            QtWidgets.QApplication.instance().installTranslator(_translator)

        self.vocal = chronoQSound(os.getcwd(), ConfigReader.config.conf['language'],
                                  ConfigReader.config.conf['sound'], ConfigReader.config.conf['soundvolume'])
        self.noise = noiseGenerator(ConfigReader.config.conf['noisesound'], ConfigReader.config.conf['noisevolume'])

        self.initUI()

        self.rpigpio.signal_btn_next.connect(self.next_action)

        self.chronoHard.accu_signal.connect(self.slot_accu)
        self.chronoHard.buzzer_validated.connect(self.slot_buzzer)
        self.chronoHard.event_voltage()
        self.chronoHard.udpReceive.switchMode_sig.connect(self.slot_switch_mode)
        self.chronoHard.status_changed.connect(self.vocal.slot_status_changed)
        self.signal_race = None
        self.signal_training = None
        self.low_voltage_ask = False
        ip, broadcast = get_ip()
        self.udpsend = udpsend(broadcast, ConfigReader.config.conf['udpport'])
        self.enableConnectedDisplay = ConfigReader.config.conf['enableDisplay']
        self.launch_time = ConfigReader.config.conf['Launch_time']
        self.configSound = ConfigReader.config.conf["sound"]
        self.chronoHard.weather.set_rules_limit(self.event.min_allowed_wind_speed, self.event.max_allowed_wind_speed,
                                                self.event.max_wind_dir_dev)
        self.tcp = tcpServer()
        self.tcp.contestRunning.connect(self.slot_contestRunning)
        self.tcp.pilotRequestSig.connect(self.slotPilotListRequest)
        if ConfigReader.config.conf['inStartBlackOut'] and ConfigReader.config.conf['competition_mode']:
            ConfigReader.config.conf['inStartBlackOut'] = False
    def initUI(self, ):
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.closeEvent = self.closeEvent
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.MainWindow)
        if ConfigReader.config.conf['fullscreen']:
            self.MainWindow.showFullScreen()
        else:
            self.MainWindow.setFixedSize(480, 320)

        self.controllers = collections.OrderedDict()

        self.controllers['config'] = WConfigCtrl("panel Config", self.ui.centralwidget)
        self.controllers['round'] = WRoundCtrl("panel Chrono", self.ui.centralwidget, self.vocal.signal_elapsedTime)
        self.controllers['training'] = WTrainingCtrl("panel Training", self.ui.centralwidget,
                                                     ConfigReader.config.conf['training_speech_interval'])
        self.controllers['settings'] = WSettings("panel Settings", self.ui.centralwidget)
        self.controllers['settingswDevices'] = WSettingsWirelessDevices("panel SettingswDevices", self.ui.centralwidget)
        self.controllers['settingsadvanced'] = WSettingsAdvanced("panel SettingsAdvanced", self.ui.centralwidget)
        self.controllers['settingsbase'] = WSettingsBase("panel SettingsBase", self.ui.centralwidget)
        self.controllers['settingswBtn'] = WSettingswBtn("panel Settings_wBtn", self.ui.centralwidget)
        self.controllers['settingssound'] = WSettingsSound("panel SettingsSound", self.ui.centralwidget)
        self.controllers['settingQrCode'] = WSettingsQrCode("panel QrCode", self.ui.centralwidget)
        self.controllers['wind'] = WWindCtrl("panel Wind", self.ui.centralwidget)

        for key, ctrl in self.controllers.items():
            for x in ctrl.get_widget():
                self.ui.verticalLayout.addWidget(x)

        round_widgets_list = self.controllers['round'].get_widget()
        self.ui.verticalLayout.setStretchFactor(round_widgets_list[0], 1)
        self.ui.verticalLayout.setStretchFactor(round_widgets_list[1], 12)
        self.ui.verticalLayout.setStretchFactor(round_widgets_list[2], 3)

        # connect signal event to method
        self.controllers['config'].btn_settings_sig.connect(self.set_show_settings)
        self.controllers['config'].btn_next_sig.connect(self.start)
        self.controllers['config'].contest_sig.connect(self.contest_changed)
        self.controllers['config'].contest_valuechanged_sig.connect(self.context_valuechanged)
        self.controllers['config'].btn_random_sig.connect(self.random_bib_start)
        self.controllers['config'].btn_day_1_sig.connect(self.bib_day_1)
        self.controllers['config'].btn_quitapp_sig.connect(self.shutdown_app)
        self.controllers['config'].btn_shutdown_sig.connect(self.shutdown_rpi)
        self.controllers['round'].btn_next_sig.connect(self.next_action)
        self.controllers['round'].btn_home_sig.connect(self.home_action)
        self.controllers['round'].btn_home_sig.connect(self.slot_contestRunning)
        self.controllers['round'].cancel_round_sig.connect(self.cancel_round)
        self.controllers['round'].wChronoCtrl.btn_penalty_100_sig.connect(self.penalty_100)
        self.controllers['round'].wChronoCtrl.btn_penalty_1000_sig.connect(self.penalty_1000)
        self.controllers['round'].wChronoCtrl.btn_clear_penalty_sig.connect(self.clear_penalty)
        self.controllers['round'].wChronoCtrl.btn_null_flight_sig.connect(self.null_flight)
        self.controllers['round'].wChronoCtrl.time_elapsed_sig.connect(self.handle_time_elapsed)
        self.controllers['round'].wChronoCtrl.btn_refly_sig.connect(self.refly)
        self.controllers['round'].wPilotCtrl.btn_cancel_flight_sig.connect(self.display_cancel_round)
        self.controllers['round'].btn_gscoring_sig.connect(self.enable_group_scoring)
        self.controllers['settings'].btn_cancel_sig.connect(self.settings_cancel)
        self.controllers['settings'].btn_valid_sig.connect(self.settings_valid)
        self.controllers['settings'].btn_settingsadvanced_sig.connect(self.show_settingsadvanced)
        self.controllers['settings'].btn_settingssound_sig.connect(self.show_settingssound)
        self.controllers['settings'].qrcode_sig.connect(self.show_settingsQrCode)
        self.controllers['settings'].btn_settingswDevices_sig.connect(self.show_settingswDevices)

        self.controllers['settingswDevices'].btn_settingsbase_sig.connect(self.show_settingsbase)
        self.controllers['settingswDevices'].btn_settingswBtn_sig.connect(self.show_settingswBtn)
        self.controllers['settingswDevices'].btn_settingsback_sig.connect(self.show_settings)
        self.controllers['settingswDevices'].btn_cancel_sig.connect(self.settings_cancel)
        self.controllers['settingswDevices'].btn_valid_sig.connect(self.settings_valid)
        self.controllers['settingswDevices'].btn_settingsbase_sig.connect(self.show_settingsbase)
        self.controllers['settingswDevices'].btn_settingswBtn_sig.connect(self.show_settingswBtn)
        self.controllers['settingswDevices'].btn_AnemometerGetList_sig.connect(self.chronoHard.weather.anemometer.GetList)
        self.controllers['settingswDevices'].btn_AnemometerConnect_sig.connect(self.chronoHard.weather.anemometer.Connect)
        self.controllers['settingswDevices'].wirelessDevicesSelected_sig.connect(self.chronoHard.weather.setConfig)
        
        self.chronoHard.weather.anemometer.list_sig.connect(self.controllers['settingswDevices'].anemometerSetData)
        self.chronoHard.weather.anemometer.status_sig.connect(self.controllers['settingswDevices'].view.AnemometerStatus.setText)
        self.chronoHard.weather.gui_wind_speed_dir_signal.connect(self.controllers['settingswDevices'].weatherStation_display)
        self.chronoHard.weather.set_minVoltageWindDir(ConfigReader.config.conf['voltage_min_windDir'])
        self.chronoHard.weather.weather_sound_signal.connect(self.vocal.slot_windAlarm)
        self.chronoHard.weather.weather_lowVoltage_signal.connect(self.vocal.slot_weatherStationLowVoltage)
        self.chronoHard.weather.weather_sensor_lost.connect(self.vocal.slot_weatherStationSensorsLost)
        self.controllers['settingsbase'].set_udp_sig(self.chronoHard.udpReceive.simulate_base_sig,
                                                     self.chronoHard.udpReceive.ipbase_set_sig,
                                                     self.chronoHard.udpReceive.ipbase_clear_sig,
                                                     self.chronoHard.udpReceive.ipbase_invert_sig)
        self.controllers['settingswBtn'].set_udp_sig(self.chronoHard.udpReceive.simulate_wbtn_sig,
                                                     self.chronoHard.udpReceive.ipwBtn_set_sig,
                                                     self.chronoHard.udpReceive.ipwBtn_clear_sig)
        self.controllers['settingsadvanced'].btn_settings_sig.connect(self.show_settings)
        self.controllers['settingsadvanced'].btn_cancel_sig.connect(self.settings_cancel)
        self.controllers['settingsadvanced'].btn_valid_sig.connect(self.settings_valid)
        self.controllers['settingsbase'].btn_settings_sig.connect(self.show_settingswDevices)
        self.controllers['settingsbase'].btn_cancel_sig.connect(self.settings_cancel)
        self.controllers['settingsbase'].btn_valid_sig.connect(self.settings_valid)
        self.controllers['settingswBtn'].btn_settings_sig.connect(self.show_settingswDevices)
        self.controllers['settingswBtn'].btn_cancel_sig.connect(self.settings_cancel)
        self.controllers['settingswBtn'].btn_valid_sig.connect(self.settings_valid)
        self.controllers['settingssound'].btn_settings_sig.connect(self.show_settings)
        self.controllers['settingssound'].btn_cancel_sig.connect(self.settings_cancel)
        self.controllers['settingssound'].btn_valid_sig.connect(self.settings_valid)
        self.controllers['settingQrCode'].btn_back_sig.connect(self.show_settings)
        self.controllers['training'].btn_reset_sig.connect(self.chronoHard.arduino.reset_training)
        self.controllers['training'].btn_home_sig.connect(self.home_training)
        self.controllers['training'].btn_next_sig.connect(self.next_action)

        self.show_config()
        self.MainWindow.show()
        self.controllers['config'].set_contest(self.daoEvent.get_list())
        self.controllers['wind'].display_wind_info(-1.0, "m/s", -1.0, False, False)
        self.chronoHard.weather.gui_weather_signal.connect(self.controllers['wind'].display_wind_info)
        self.chronoHard.weather.gui_weather_signal.connect(self.controllers['round'].wChronoCtrl.display_wind_info)
        self.controllers['wind'].lowVoltage_sig.connect(self.vocal.slot_lowVoltage)

    def show_config(self):
        self.controllers['round'].hide()
        self.controllers['training'].hide()
        self.controllers['settings'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['config'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_chrono(self):
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['round'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_settings(self):
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['settings'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_settingswDevices(self):
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settings'].hide()
        self.controllers['settingswDevices'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_settingsadvanced(self):
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['settingsadvanced'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_settingsbase(self):
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['settingsbase'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_settingswBtn(self):
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['settingswBtn'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_settingssound(self):
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['settingssound'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_training(self):
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingQrCode'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['training'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def show_settingsQrCode(self, url):
        self.controllers['settingQrCode'].displayF3FRankingQrCode()
        self.controllers['training'].hide()
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['round'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['settingswBtn'].hide()
        self.controllers['settingsbase'].hide()
        self.controllers['settingssound'].hide()
        self.controllers['settingswDevices'].hide()
        self.controllers['settingQrCode'].show()
        self.controllers['wind'].show()
        if self.__debug:
            print(self.MainWindow.size())

    def set_show_settings(self):
        self.controllers['settings'].set_data()
        self.controllers['settingssound'].set_data()
        self.controllers['settingsadvanced'].set_data()
        self.controllers['settingsbase'].set_data()
        self.controllers['settingswBtn'].set_data()
        self.controllers['settingswDevices'].set_data()
        self.show_settings()

    def set_signal_mode(self, training=False):
        if self.signal_training is not None:
            self.chronoHard.run_training.disconnect(self.controllers['training'].wChronoCtrl.set_time)
            self.chronoHard.status_changed.disconnect(self.controllers['training'].wChronoCtrl.set_status)
            self.controllers['training'].wChronoCtrl.training_voice_sig.disconnect(self.vocal.sound_time)
            self.signal_training = None
        if self.signal_race is not None:
            self.chronoHard.status_changed.disconnect(self.slot_status_changed)
            self.chronoHard.run_started.disconnect(self.slot_run_started)
            self.chronoHard.lap_finished.disconnect(self.slot_lap_finished)
            self.chronoHard.run_finished.disconnect(self.slot_run_finished)
            self.chronoHard.run_validated.disconnect(self.slot_run_validated)
            self.chronoHard.altitude_finished.disconnect(self.slot_altitude_finished)
            self.chronoHard.udpReceive.penalty_sig.disconnect(self.penalty_100)
            self.controllers['round'].get_alarm_sig().disconnect(self.slot_weather_alarm)
            if self.rpigpio.buzzer_next is not None:
                self.chronoHard.weather.beep_signal.emit("stop", 0, 1000)
                self.chronoHard.weather.beep_signal.disconnect(self.rpigpio.buzzer_next_slot_blink)
            self.signal_race = None
        if training == True:
            self.chronoHard.run_training.connect(self.controllers['training'].wChronoCtrl.set_time)
            self.chronoHard.status_changed.connect(self.controllers['training'].wChronoCtrl.set_status)
            self.controllers['training'].wChronoCtrl.training_voice_sig.connect(self.vocal.sound_time)
            self.signal_training = True
        elif training == False:
            self.chronoHard.status_changed.connect(self.slot_status_changed)
            self.chronoHard.run_started.connect(self.slot_run_started)
            self.chronoHard.lap_finished.connect(self.slot_lap_finished)
            self.chronoHard.run_finished.connect(self.slot_run_finished)
            self.chronoHard.run_validated.connect(self.slot_run_validated)
            self.chronoHard.altitude_finished.connect(self.slot_altitude_finished)
            self.chronoHard.udpReceive.penalty_sig.connect(self.penalty_100)
            self.controllers['round'].get_alarm_sig().connect(self.slot_weather_alarm)
            if self.rpigpio.buzzer_next is not None:
                self.chronoHard.weather.beep_signal.connect(self.rpigpio.buzzer_next_slot_blink)
            self.signal_race = True

    def settings_valid(self):
        self.controllers['settings'].get_data()
        self.controllers['settingssound'].get_data()
        self.controllers['settingsadvanced'].get_data()
        self.controllers['settingsbase'].get_data()
        self.controllers['settingsbase'].btn_valid()
        self.controllers['settingswBtn'].get_data()
        self.controllers['settingswBtn'].btn_valid()
        if ConfigReader.config.conf['inStartBlackOut'] and ConfigReader.config.conf['competition_mode']:
            ConfigReader.config.conf['inStartBlackOut'] = False
        ConfigReader.config.write('config.json')
        self.show_config()
        # self.vocal.settings(ConfigReader.config.conf['sound'])
        self.noise.settings(ConfigReader.config.conf['noisesound'],
                            ConfigReader.config.conf['noisevolume'])
        self.chronoHard.set_buzzer_time(ConfigReader.config.conf['buzzer_duration'])
        self.enableConnectedDisplay = ConfigReader.config.conf['enableDisplay']
        self.launch_time = ConfigReader.config.conf['Launch_time']
        self.configSound = ConfigReader.config.conf["sound"]

    def settings_cancel(self):
        self.controllers['settingsbase'].btn_cancel()
        self.controllers['settingswBtn'].btn_cancel()
        self.show_config()

    def home_action(self):
        # print event data
        self.controllers['round'].wChronoCtrl.stoptime()
        self.vocal.stop_all()
        self.show_config()
        self.set_signal_mode(training=None)
        self.chronoHard.weather.enable_rules(enable=False)
        self.noise.stop()

    def home_training(self):
        self.show_config()
        self.set_signal_mode(training=None)
        self.noise.stop()

    def next_pilot(self, insert_database=False):
        current_round = self.event.get_current_round()
        self.controllers['round'].wPilotCtrl.set_data(current_round.next_pilot(insert_database, visited_competitors=[]),
                                                      current_round)
        self.controllers['round'].wChronoCtrl.reset_ui()
        self.vocal.signal_pilotname.emit(int(self.event.get_current_round().get_current_competitor().get_bib_number()))
        # Can't use current_group because it has changed
        if self.event.get_current_round().group_scoring_enabled():
            self.controllers['round'].handle_group_scoring_enabled(True)
        else:
            self.controllers['round'].handle_group_scoring_enabled(False)
        # Send this string using UDP ... using udpbeep
        if self.enableConnectedDisplay:
            if self.__debug:
                print(current_round.get_summary_as_json(self.event.get_current_round()))
            #self.udpsend.sendOrderData(current_round.get_summary_as_json(self.event.get_current_round()))
            self.tcp.orderDataSig.emit(current_round.get_summary_as_json(self.event.get_current_round()))


    def context_valuechanged(self):
        self.getcontextparameters(False)

    def random_bib_start(self):
        self.getcontextparameters(False)
        self.event.random_bib()
        self.controllers['config'].set_data(self.event)
        self.getcontextparameters(True)

    def bib_day_1(self):
        self.getcontextparameters(False)
        if self.event:
            del self.event
        self.event = self.daoEvent.get(self.controllers['config'].view.ContestList.currentData().id,
                                       fetch_competitors=True, fetch_rounds=True, fetch_runs=False)

        self.event.bib_day_1_compute()
        self.controllers['config'].set_data(self.event)
        self.getcontextparameters(True)

    def start(self):
        if self.event is not None:
            self.getcontextparameters(True)
            del self.event
            self.event = None

        self.chronoHard.reset()
        self.chronodata.reset()
        self.noise.start()

        eventData = self.controllers['config'].view.ContestList.currentData()
        if eventData is not None:
            self.event = self.daoEvent.get(eventData.id,
                                           fetch_competitors=True, fetch_rounds=True, fetch_runs=True,
                                           fetch_runs_lastround=True)
            current_round = self.event.get_current_round()
            if not current_round.has_run() and not current_round.group_scoring_enabled():
                current_round.set_flight_order_from_scratch()
                Round.round_dao.update(current_round)
            current_competitor = current_round.get_current_competitor()
            if not current_competitor.present:
                current_round.set_null_flight(current_competitor)
                current_competitor = current_round.next_pilot()
            self.controllers['round'].wPilotCtrl.set_data(current_competitor,
                                                          self.event.get_current_round())
            self.vocal.signal_pilotname.emit(int(current_competitor.get_bib_number()))
            self.chronoHard.set_mode(training=False)
            self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
            self.controllers['round'].wChronoCtrl.settime(self.launch_time, False, False,
                                                          to_launch=True)
            self.controllers['round'].wChronoCtrl.reset_ui()
            if current_round.group_scoring_enabled():
                self.controllers['round'].handle_group_scoring_enabled(True)
            else:
                self.controllers['round'].handle_group_scoring_enabled(False)
            self.chronoHard.weather.set_rules_limit(self.event.min_allowed_wind_speed,
                                                    self.event.max_allowed_wind_speed,
                                                    self.event.max_wind_dir_dev)
            self.chronoHard.weather.enable_rules(self.controllers['round'].isalarm_enable())
            self.set_signal_mode(training=False)
            self.show_chrono()
            if self.enableConnectedDisplay:
                if self.__debug:
                    print(current_round.get_summary_as_json(self.event.get_current_round()))
                #self.udpsend.sendOrderData(current_round.get_summary_as_json(self.event.get_current_round()))
                self.tcp.orderDataSig.emit(current_round.get_summary_as_json(self.event.get_current_round()))


        else:
            self.chronoHard.set_mode(training=True)
            self.controllers['training'].wChronoCtrl.reset()
            self.set_signal_mode(training=True)
            self.show_training()

    def getcontextparameters(self, updateBDD=False):
        self.controllers['config'].get_data()
        self.event.max_interruption_time = self.controllers['config'].max_interruption_time
        self.event.min_allowed_wind_speed = self.controllers['config'].min_allowed_wind_speed
        self.event.max_allowed_wind_speed = self.controllers['config'].max_allowed_wind_speed
        self.event.max_wind_dir_dev = self.controllers['config'].max_wind_dir_dev
        self.event.flights_before_refly = self.controllers['config'].flights_before_refly
        self.event.bib_start = self.controllers['config'].bib_start
        self.event.dayduration = self.controllers['config'].dayduration
        self.event.groups_number = self.controllers['config'].groups_number
        if updateBDD:
            self.daoEvent.update(self.event)

    def next_action(self):
        if self.controllers['round'].is_show():
            self.chronoHard.handle_chrono_event("btnnext", "event", "btnnext")
        elif self.controllers['training'].is_show():
            self.controllers['training'].btn_reset()

        self.rpigpio.signal_buzzer_next.emit(1)
        print("MainUIController btn_next_action")

    def handle_time_elapsed(self):
        if self.__debug:
            print("time elapsed")
        if self.chronoHard.get_status() == chronoStatus.WaitLaunch:
            self.vocal.signal_penalty.emit()
            self.controllers['round'].wChronoCtrl.stoptime()
            self.chronoHard.set_status(chronoStatus.InWait)

    def slot_buzzer(self):
        self.rpigpio.signal_buzzer.emit(1)

    def penalty_100(self):
        # print("penalty event 100")
        self.vocal.signal_penalty.emit()
        self.chronoHard.addPenalty(100)
        self.controllers['round'].wChronoCtrl.set_penalty_value(self.chronoHard.getPenalty())

    def penalty_1000(self):
        self.vocal.signal_penalty.emit()
        self.chronoHard.addPenalty(1000)
        self.controllers['round'].wChronoCtrl.set_penalty_value(self.chronoHard.getPenalty())

    def clear_penalty(self):
        self.chronoHard.clearPenalty()
        self.controllers['round'].wChronoCtrl.set_penalty_value(self.chronoHard.getPenalty())

    def display_cancel_round(self):
        self.controllers['round'].set_cancelmode(True)

    def enable_group_scoring(self):
        self.event.get_current_round().enable_group_scoring()
        self.start()
        self.controllers['round'].handle_group_scoring_enabled(True)

    def cancel_round(self):
        self.event.get_current_round().cancel_current_group()
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor(),
                                                      self.event.get_current_round())
        self.chronoHard.reset()
        self.chronodata.reset()
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.reset_ui()
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())

    def null_flight(self):
        self.chronoHard.set_status(chronoStatus.Finished)
        self.chronoHard.valid = False
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        self.controllers['round'].wChronoCtrl.set_null_flight(True)

    def refly(self):
        # TODO : get penalty value if any
        self.chronoHard.set_status(chronoStatus.Finished)
        self.chronoHard.valid = False
        self.chronoHard.setrefly()
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        self.controllers['round'].wChronoCtrl.set_refly(True)

    def contest_changed(self):
        if self.event is not None:
            self.getcontextparameters(updateBDD=True)
            del self.event
            self.event = None

        eventData = self.controllers['config'].view.ContestList.currentData()
        if eventData is not None:
            self.event = self.daoEvent.get(eventData.id, fetch_competitors=True, fetch_rounds=True, fetch_runs=False)
            self.controllers['config'].contest_valuechanged_sig.disconnect()
            self.controllers['config'].set_data(self.event)
            self.controllers['config'].contest_valuechanged_sig.connect(self.context_valuechanged)
            self.chronoHard.weather.set_rules_limit(self.event.min_allowed_wind_speed,
                                                    self.event.max_allowed_wind_speed,
                                                    self.event.max_wind_dir_dev)

    def slot_weather_alarm(self):
        self.chronoHard.weather.enable_rules(self.controllers['round'].isalarm_enable())
        if self.__debug:
            print("alarm enable : ", self.controllers['round'].isalarm_enable())

    def slot_switch_mode(self):
        if self.controllers['config'].is_show():
            if self.__debug:
                print('config')
            contest = self.controllers['config'].view.ContestList.count()
            self.controllers['config'].view.ContestList.setCurrentIndex(contest - 1)
            self.controllers['config'].contest_sig.emit()
            self.start()
        elif self.controllers['round'].is_show():
            if self.__debug:
                print("mode round")
            self.controllers['round'].btn_home_sig.emit()
            self.controllers['config'].view.ContestList.setCurrentIndex(0)
            self.controllers['config'].contest_sig.emit()
            self.start()

        elif self.controllers['training'].is_show():
            if self.__debug:
                print("mode training")
            self.controllers['training'].btn_home_sig.emit()
            contest = self.controllers['config'].view.ContestList.count()
            self.controllers['config'].view.ContestList.setCurrentIndex(contest - 1)
            self.controllers['config'].contest_sig.emit()
            self.start()

    def slot_status_changed(self, status):
        # print ("slot status", status)
        self.controllers['round'].wChronoCtrl.set_status(status)
        if (status == chronoStatus.WaitLaunch):
            self.controllers['round'].wChronoCtrl.settime(self.launch_time, False, to_launch=True)
        if (status == chronoStatus.Launched):
            self.vocal.stop_Timing()
            self.controllers['round'].wChronoCtrl.settime(self.launch_time, False)

    def slot_run_started(self):
        self.controllers['round'].wChronoCtrl.settime(0, True)
        self.vocal.stop_Timing()


    def slot_lap_finished(self, lap, last_lap_time):
        self.controllers['round'].wChronoCtrl.set_laptime(last_lap_time)
        self.vocal.signal_base.emit(lap)

    def slot_run_finished(self, run_time):
        # print("Main UI Controller slot run finished : ", time.time())
        self.controllers['round'].wChronoCtrl.stoptime()
        # print ('final time : ' + str(run_time))
        self.controllers['round'].wChronoCtrl.set_finaltime(run_time)
        self.controllers['round'].widgetBtn.update()
        if self.configSound:
            self.vocal.signal_time.emit(run_time, False)

    def slot_altitude_finished(self, run_time):
        if self.__debug:
            print("slot altitude finished")

    def slot_run_validated(self):
        # print("run validated")
        if self.chronoHard.isRefly():
            self.event.get_current_round().handle_refly(0, insert_database=True)
        else:
            self.chronoHard_to_chrono(self.chronoHard, self.chronodata)
            self.event.get_current_round().handle_terminated_flight(
                self.event.get_current_round().get_current_competitor(),
                self.chronodata, self.chronoHard.getPenalty(), self.chronoHard.valid, insert_database=True)

        self.chronoHard.reset()
        self.chronodata = Chrono()
        self.next_pilot(insert_database=True)
        self.controllers['round'].wChronoCtrl.settime(self.launch_time, False, False)
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        self.controllers['wind'].setLastRoundTime()

    def slot_contestRunning(self):
        print("slot contest Running : ", str(self.controllers['round'].is_show()))
        self.tcp.contestInRunSig.emit(self.controllers['round'].is_show())

    def slotPilotListRequest(self):
        print("PilotList Request")
        current_round = self.event.get_current_round()
        self.tcp.orderDataSig.emit(current_round.get_summary_as_json(self.event.get_current_round()))

    @staticmethod
    def chronoHard_to_chrono(chronoHard, chrono):
        chrono.run_time = chronoHard.get_time()
        chrono.climbout_time = chronoHard.get_climbout_time()
        chrono.start_time = chronoHard.getStartTime()
        chrono.end_time = chronoHard.getEndTime()
        chrono.max_wind_speed = chronoHard.weather.getMaxWindSpeed()
        chrono.min_wind_speed = chronoHard.weather.getMinWindSpeed()
        chrono.mean_wind_speed = chronoHard.weather.getMeanWindSpeed()
        chrono.wind_direction = chronoHard.weather.getWindDir()
        for lap in chronoHard.getLaps():
            chrono.add_lap_time(lap)
            #print(chrono.to_string())

    def slot_accu(self, voltage1, voltage2):
        self.controllers['wind'].set_voltage(voltage1, voltage2)
        if self.__debug:
            print(voltage1, voltage2)
        # adding for log voltage
        f = open("voltage_log.txt", "a+")
        f.write(str(self.startup_time) + ',' + str((time.time() - self.startup_time) / 60.0) +
                ',' + str(voltage1) + ',' + str(voltage2) + '\n')
        f.close()

    def closeEvent(self, event):
        self.close_signal.emit()
        event.accept()

    def shutdown_app(self):
        if self.rpigpio.buzzer_next is not None:
            self.rpigpio.buzzer_next_slot_blink("stop", 0)
        self.chronoHard.stop()
        if self.webserver_process is not None:
            if self.__debug:
                print('Kill process ' + str(self.webserver_process.pid))
            time.sleep(1)  # Wait for the process to be killed
            self.webserver_process.kill()
        exit()

    def shutdown_rpi(self):
        import os
        os.system('shutdown now')
        self.shutdown_app()


def main():
    ConfigReader.init()
    ConfigReader.config = ConfigReader.Configuration('../../config.json')
    dao = EventDAO()
    chronodata = Chrono()
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUiCtrl(dao, chronodata, "")

    # launched simulate mode
    if (ConfigReader.config.conf['simulate']):
        ui_simulate = SimulateBase()
        ui_simulate.close_signal.connect(ui.MainWindow.close)
        ui.close_signal.connect(ui_simulate.MainWindow.close)

    try:
        # writer.setupDecoder()
        print("lancement IHM")
        sys.exit(app.exec_())

    except KeyboardInterrupt:
        pass
    finally:
        pass


if __name__ == '__main__':
    main()
