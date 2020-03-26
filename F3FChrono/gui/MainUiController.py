from F3FChrono.chrono import ConfigReader
from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.gui.Simulate_base import SimulateBase
from F3FChrono.chrono.Chrono import *
from F3FChrono.data.dao.EventDAO import EventDAO, RoundDAO
from F3FChrono.data.Chrono import Chrono
from F3FChrono.chrono.Sound import *
from F3FChrono.chrono.GPIOPort import rpi_gpio


class MainUiCtrl (QtWidgets.QMainWindow):
    close_signal = pyqtSignal()
    signal_btnnext = pyqtSignal(int)
    def __init__(self, eventdao, chronodata, rpi, webserver_process):
        super().__init__()

        self.webserver_process = webserver_process
        self.daoEvent = eventdao
        self.daoRound = RoundDAO()
        self.event = None
        self.chronodata = chronodata
        self.chronoRpi=ChronoRpi(self.signal_btnnext)
        self.chronoArduino=ChronoArduino(self.signal_btnnext)
        self.rpigpio=rpi_gpio(rpi, self.btn_next_action, self.btn_baseA, self.btn_baseB)
        self.chronoHard = self.chronoRpi
        self.base_test = -10
        self.vocal = chronoQSound()

        self.signal_btnnext.connect(self.btn_next_action)
        self.chronoHard.status_changed.connect(self.slot_status_changed)
        self.chronoHard.lap_finished.connect(self.slot_lap_finished)
        self.chronoHard.run_finished.connect(self.slot_run_finished)
        self.chronoHard.run_validated.connect(self.slot_run_validated)
        self.chronoHard.wind_signal.connect(self.slot_wind_ui)
        self.chronoHard.rssi_signal.connect(self.slot_rssi)
        self.chronoHard.accu_signal.connect(self.slot_accu)
        self.chronoHard.buzzer_validated.connect(self.slot_buzzer)
        self.initUI()

    def initUI(self):
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
        self.controllers['round'] = WRoundCtrl("panel Chrono", self.ui.centralwidget)
        self.controllers['settings'] = WSettings("panel Settings", self.ui.centralwidget)
        self.controllers['settingsadvanced'] = WSettingsAdvanced("panel SettingsAdvanced", self.ui.centralwidget)
        self.controllers['picampair'] = WPiCamPair("panel picam", self.ui.centralwidget)
        self.controllers['wind'] = WWindCtrl("panel Wind", self.ui.centralwidget)

        for key, ctrl in self.controllers.items():
            for x in ctrl.get_widget():
                self.ui.verticalLayout.addWidget(x)

        round_widgets_list = self.controllers['round'].get_widget()
        self.ui.verticalLayout.setStretchFactor(round_widgets_list[0], 1)
        self.ui.verticalLayout.setStretchFactor(round_widgets_list[1], 12)
        self.ui.verticalLayout.setStretchFactor(round_widgets_list[2], 3)


        #connect signal event to method
        self.controllers['config'].btn_settings_sig.connect(self.set_show_settings)
        self.controllers['config'].btn_next_sig.connect(self.start)
        self.controllers['config'].contest_sig.connect(self.contest_changed)
        self.controllers['config'].chrono_sig.connect(self.chronotype_changed)
        self.controllers['config'].btn_picampair_sig.connect(self.show_picampair)
        self.controllers['config'].btn_random_sig.connect(self.random_bib_start)
        self.controllers['config'].btn_day_1_sig.connect(self.bib_day_1)
        self.controllers['round'].btn_next_sig.connect(self.next_action)
        self.controllers['round'].btn_home_sig.connect(self.home_action)
        self.controllers['round'].btn_refly_sig.connect(self.refly)
        self.controllers['round'].wChronoCtrl.btn_penalty_100_sig.connect(self.penalty_100)
        self.controllers['round'].wChronoCtrl.btn_penalty_1000_sig.connect(self.penalty_1000)
        self.controllers['round'].wChronoCtrl.btn_clear_penalty_sig.connect(self.clear_penalty)
        self.controllers['round'].wChronoCtrl.btn_null_flight_sig.connect(self.null_flight)
        self.controllers['round'].wChronoCtrl.time_elapsed_sig.connect(self.handle_time_elapsed)
        self.controllers['round'].btn_cancel_flight_sig.connect(self.cancel_round)
        self.controllers['settings'].btn_settingsadvanced_sig.connect(self.show_settingsadvanced)
        self.controllers['settings'].btn_cancel_sig.connect(self.show_config)
        self.controllers['settings'].btn_valid_sig.connect(self.settings_valid)
        self.controllers['settings'].btn_quitapp_sig.connect(self.shutdown_app)
        self.controllers['settingsadvanced'].btn_settings_sig.connect(self.show_settings)
        self.controllers['picampair'].btn_valid_sig.connect(self.picampair_valid)
        self.controllers['picampair'].btn_cancel_sig.connect(self.show_config)

        self.show_config()
        self.MainWindow.show()
        self.controllers['config'].set_contest(self.daoEvent.get_list())
        self.controllers['wind'].set_data(0, 0, 0)

    def show_config(self):
        self.controllers['round'].hide()
        self.controllers['settings'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['picampair'].hide()
        self.controllers['config'].show()
        self.controllers['wind'].show()
        print(self.MainWindow.size())

    def show_chrono(self):
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['picampair'].hide()
        self.controllers['round'].show()
        self.controllers['wind'].show()
        print(self.MainWindow.size())

    def show_settings(self):
        self.controllers['config'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['round'].hide()
        self.controllers['picampair'].hide()
        self.controllers['settings'].show()
        self.controllers['wind'].show()
        print(self.MainWindow.size())

    def show_picampair(self):
        self.controllers['config'].hide()
        self.controllers['settingsadvanced'].hide()
        self.controllers['round'].hide()
        self.controllers['settings'].hide()
        self.controllers['picampair'].show()
        self.controllers['wind'].show()
        print(self.MainWindow.size())

    def show_settingsadvanced(self):
        self.controllers['config'].hide()
        self.controllers['settings'].hide()
        self.controllers['round'].hide()
        self.controllers['picampair'].hide()
        self.controllers['settingsadvanced'].show()
        self.controllers['wind'].show()
        print(self.MainWindow.size())

    def set_show_settings(self):
        self.controllers['settings'].set_data()
        self.controllers['settingsadvanced'].set_data()
        self.show_settings()

    def settings_valid(self):
        self.controllers['settings'].get_data()
        self.controllers['settingsadvanced'].get_data()
        ConfigReader.config.write('config.json')
        self.show_config()

    def picampair_valid(self):
        print ("todo add picampair valid action")
        self.show_config()

    def home_action(self):
        #print event data
        self.controllers['round'].wChronoCtrl.stoptime()
        self.vocal.stop_all()
        print(self.event.to_string())

        self.show_config()

    def next_pilot(self, insert_database=False):
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().next_pilot(insert_database),
                                                      self.event.get_current_round())
        self.controllers['round'].wChronoCtrl.reset_ui()

    def refly(self):
        #TODO : get penalty value if any
        self.event.get_current_round().handle_refly(0)
        self.chronoHard.reset()
        self.chronodata.reset()
        self.next_pilot()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def random_bib_start(self):
        self.getcontextparameters(False)
        self.event.random_bib()
        self.controllers['config'].set_data(self.event)
        self.getcontextparameters(True)

    def bib_day_1(self):
        self.getcontextparameters(False)
        if self.event:
            del self.event
        self.event = self.daoEvent.get(self.controllers['config'].view.ContestList.currentIndex(),
                    fetch_competitors=True, fetch_rounds=True, fetch_runs=False)

        self.event.bib_day_1_compute()
        self.controllers['config'].set_data(self.event)
        self.getcontextparameters(True)

    def start(self):
        self.getcontextparameters(True)
        if self.event:
            del self.event
        self.event = self.daoEvent.get(self.controllers['config'].view.ContestList.currentIndex(),
                    fetch_competitors=True, fetch_rounds=True, fetch_runs=True, fetch_runs_lastround=True)

        self.chronoHard.reset()
        self.chronodata.reset()
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor(),
                                                      self.event.get_current_round())
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        self.show_chrono()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def getcontextparameters(self, updateBDD=False):
        self.controllers['config'].get_data()
        self.event.max_interruption_time=self.controllers['config'].max_interruption_time
        self.event.min_allowed_wind_speed=self.controllers['config'].min_allowed_wind_speed
        self.event.max_allowed_wind_speed=self.controllers['config'].max_allowed_wind_speed
        self.event.max_wind_dir_dev=self.controllers['config'].max_wind_dir_dev
        self.event.flights_before_refly=self.controllers['config'].flights_before_refly
        self.event.bib_start=self.controllers['config'].bib_start
        self.event.dayduration=self.controllers['config'].dayduration
        if updateBDD:
            self.daoEvent.update(self.event)

    def next_action(self):
        self.chronoHard.chrono_signal.emit("btnnext", "event", "btnnext")
        self.rpigpio.signal_buzzer_next.emit()

    def btn_next_action(self, port):
        if self.controllers['round'].is_show():
            self.chronoHard.chrono_signal.emit("btnnext", "event", "btnnext")
            self.rpigpio.signal_buzzer_next.emit()

    def btn_baseA(self, port):
        print("btn base A")
        self.chronoHard.chrono_signal.emit("udpreceive", "event", "baseA")

    def btn_baseB(self, port):
        print("btn base B")
        self.chronoHard.chrono_signal.emit("udpreceive", "event", "baseB")

    def handle_time_elapsed(self):
        print("time elapsed")
        if self.chronoHard.get_status()==chronoStatus.WaitLaunch:
            self.vocal.signal_penalty.emit()
            self.controllers['round'].wChronoCtrl.stoptime()
            self.vocal.signal_waitlaunch_stop.emit()

        if self.chronoHard.get_status()==chronoStatus.Launched or self.chronoHard.get_status()==chronoStatus.InStart:
            self.chronoHard.chrono_signal.emit("btnnext", "event", "btnnext")


    def slot_buzzer(self):
        self.rpigpio.signal_buzzer.emit()

    def penalty_100(self):
        #print("penalty event 100")
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

    def cancel_round(self):
        self.event.get_current_round().cancel_round()
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor(),
                                                      self.event.get_current_round())
        self.chronoHard.reset()
        self.chronodata.reset()
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.reset_ui()
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())

    def null_flight(self):
        self.chronoHard.set_status(chronoStatus.Finished)
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        self.controllers['round'].wChronoCtrl.set_null_flight(True)

    def contest_changed(self):
        if self.event:
            self.getcontextparameters(updateBDD=True)
            del self.event
        self.event = self.daoEvent.get(self.controllers['config'].view.ContestList.currentIndex(),
                                  fetch_competitors=True, fetch_rounds=False, fetch_runs=False)

        self.controllers['config'].set_data(self.event)

    def chronotype_changed(self):
        if (self.controllers['config'].view.ChronoType.currentIndex()==0):
            self.chronoHard = self.chronoRpi
        else:
            self.chronoHard = self.chronoArduino
        self.chronoHard.reset()

    def slot_status_changed(self, status):
        self.controllers['round'].wChronoCtrl.set_status(status)
        if (status==chronoStatus.WaitLaunch):
            self.vocal.signal_waitlaunch.emit()
            time.sleep(0.7)
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (status == chronoStatus.Launched):
            self.vocal.signal_waitstart.emit()
            time.sleep(1)
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (status==chronoStatus.InStart):
            self.vocal.signal_entry.emit()
        if (status == chronoStatus.InProgress):
            self.vocal.signal_base.emit(0)
            self.controllers['round'].wChronoCtrl.settime(0, True)

    def slot_lap_finished (self, lap, last_lap_time):
        self.controllers['round'].wChronoCtrl.set_laptime(last_lap_time)
        self.vocal.signal_base.emit(lap)

    def slot_run_finished(self, run_time):
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.set_finaltime(run_time)
        self.rpigpio.signal_buzzer_end.emit()
        if ConfigReader.config.conf["voice"]:
            time.sleep(0.5)     #wait gui has been refresh otherwise the time is updated after vocal sound
            self.vocal.signal_time.emit(run_time)

    def slot_run_validated(self):
        self.chronoHard_to_chrono(self.chronoHard, self.chronodata)
        self.event.get_current_round().handle_terminated_flight(
            self.event.get_current_round().get_current_competitor(),
            self.chronodata, self.chronoHard.getPenalty(), True, insert_database=True)
        self.chronoHard.reset()
        self.chronodata = Chrono()
        self.next_pilot(insert_database=True)
        self.controllers['round'].wChronoCtrl.settime(30000, False, False)
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())

    @staticmethod
    def chronoHard_to_chrono(chronoHard, chrono):
        chrono.run_time=chronoHard.get_time()
        chrono.start_time=chronoHard.getStartTime()
        chrono.end_time=chronoHard.getEndTime()
        chrono.max_wind_speed=chronoHard.getMaxWindSpeed()
        chrono.min_wind_speed=chronoHard.getMinWindSpeed()
        chrono.mean_wind_speed=chronoHard.getMeanWindSpeed()
        chrono.wind_direction=chronoHard.getWindDir()
        for lap in chronoHard.getLaps():
            chrono.add_lap_time(lap)
        print(chrono.to_string())

    '''def process_ui(self, caller, data, address):
        print("process ui : \n"+"\tdata : "+data+"\n\taddress : "+address)
        #config page Wait detection on picam
        if (self.controllers['config'].is_piCamA_onConfig()):
            self.controllers['config'].piCamA_config=False
            self.controllers['config'].set_piCamA(address)
        elif (self.controllers['config'].is_piCamB_onConfig()):
            self.controllers['config'].piCamB_config=False
            self.controllers['config'].set_piCamB(address)
    '''
    def slot_wind_ui(self, wind, angle, rain=False):
        print("Wind UI")
        self.controllers['wind'].set_data(wind, angle, rain)
        self.controllers['wind'].check_rules(self.event.max_wind_dir_dev,\
                                    self.event.min_allowed_wind_speed, self.event.max_allowed_wind_speed,\
                                    self.event.max_interruption_time)

    def slot_accu(self, voltage):
        self.controllers['wind'].set_voltage(voltage)

    def slot_rssi(self, rssi1, rssi2):
        self.controllers['wind'].set_rssi(rssi1, rssi2)

    def closeEvent(self, event):
        self.close_signal.emit()
        event.accept()

    def shutdown_app(self):
        if self.webserver_process is not None:
            print('Kill process ' + str(self.webserver_process.pid))
            time.sleep(1)  # Wait for the process to be killed
            self.webserver_process.kill()
        exit()

def main ():

    ConfigReader.init()
    ConfigReader.config = ConfigReader.Configuration ('../../config.json')
    dao = EventDAO()
    chronodata = Chrono()
    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(dao, chronodata, '')
    #launched simulate mode
    if (ConfigReader.config.conf['simulate']):
        ui_simulate=SimulateBase()
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
