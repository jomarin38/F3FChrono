import collections

from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.chrono.Chrono import *
from F3FChrono.data.dao.EventDAO import EventDAO, RoundDAO
from F3FChrono.data.Chrono import Chrono
from F3FChrono.chrono.Sound import chronoVocal
from F3FChrono.chrono.GPIOPort import *


class MainUiCtrl (QtWidgets.QMainWindow):
    def __init__(self, dao, chronodata, sound, rpi):
        super().__init__()

        self.dao = dao
        self.daoRound = RoundDAO()
        self.event = None
        self.chronodata = chronodata
        self.chronoRpi=ChronoRpi()
        self.chronoArduino=ChronoArduino()
        self.buzzer=None
        if rpi!='':
            self.buzzer=gpioPort(19, duration=1000,start_blinks=2)
            #btn_next callback
            addCallback(12, self.btn_next_action, False)
            #btn_baseA
            addCallback(5, self.btn_baseA, False)
            #btn_baseB
            addCallback(6, self.btn_baseB, False)

        self.chronoHard = self.chronoRpi
        self.initUI()
        self.base_test = -10

        if sound:
            self.vocal = chronoVocal()

        self.chronoHard.status_changed.connect(self.slot_status_changed)
        self.chronoHard.lap_finished.connect(self.slot_lap_finished)
        self.chronoHard.run_finished.connect(self.slot_run_finished)
        self.chronoHard.run_validated.connect(self.slot_run_validated)
        self.chronoHard.wind_signal.connect(self.slot_wind_ui)
        self.chronoHard.rssi_signal.connect(self.slot_rssi)
        self.chronoHard.accu_signal.connect(self.slot_accu)
        self.chronoHard.buzzer_validated.connect(self.slot_buzzer)

    def __del__(self):
        if self.buzzer!=None:
            self.buzzer.terminated=True
            self.buzzer.join()

    def initUI(self):
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.MainWindow)
        #self.MainWindow.showFullScreen()
        self.controllers = collections.OrderedDict()

        self.controllers['config'] = WConfigCtrl("panel Config", self.ui.centralwidget)
        self.controllers['round'] = WRoundCtrl("panel Chrono", self.ui.centralwidget)
        self.controllers['wind'] = WWindCtrl("panel Wind", self.ui.centralwidget)

        for key, ctrl in self.controllers.items():
            for x in ctrl.get_widget():
                self.ui.verticalLayout.addWidget(x)

        #connect signal event to method
        self.controllers['config'].btn_next_sig.connect(self.start)
        self.controllers['config'].contest_sig.connect(self.contest_changed)
        self.controllers['config'].chrono_sig.connect(self.chronotype_changed)
        self.controllers['round'].btn_next_sig.connect(self.next_action)
        self.controllers['round'].btn_home_sig.connect(self.home_action)
        self.controllers['round'].btn_refly_sig.connect(self.refly)
        self.controllers['round'].wChronoCtrl.btn_penalty_100_sig.connect(self.penalty_100)
        self.controllers['round'].wChronoCtrl.btn_penalty_1000_sig.connect(self.penalty_1000)
        self.controllers['round'].wChronoCtrl.btn_clear_penalty_sig.connect(self.clear_penalty)
        self.controllers['round'].wChronoCtrl.btn_null_flight_sig.connect(self.null_flight)
        self.controllers['round'].btn_cancel_flight_sig.connect(self.cancel_round)

        self.show_config()
        self.MainWindow.show()
        self.controllers['config'].set_contest(self.dao.get_list())
        self.controllers['wind'].set_data(0, 0, 0)

    def show_config(self):
        self.controllers['round'].hide()
        self.controllers['config'].show()
        self.controllers['wind'].show()
        print(self.MainWindow.size())

    def show_chrono(self):
        self.controllers['config'].hide()
        self.controllers['round'].show()
        self.controllers['wind'].show()
        print(self.MainWindow.size())

    def home_action(self):
        #print event data
        self.controllers['round'].wChronoCtrl.stoptime()
        print(self.event.to_string())

        self.show_config()

    def next_pilot(self, insert_database=False):
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().next_pilot(insert_database),
                                                      self.event.get_current_round().round_number)
        self.controllers['round'].wChronoCtrl.reset_ui()

    def refly(self):
        #TODO : get penalty value if any
        self.event.get_current_round().handle_refly(0)
        self.chronoHard.reset()
        self.chronodata.reset()
        self.next_pilot()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def start(self):
        self.event = self.dao.get(self.controllers['config'].view.ContestList.currentIndex(),\
                                  fetch_competitors=True, fetch_rounds=True, fetch_runs=True)
        self.controllers['config'].get_data()
        self.event.max_interruption_time=self.controllers['config'].interruption_time_max
        self.event.max_wind_dir_dev=self.controllers['config'].wind_orientation
        self.event.min_allowed_wind_speed=self.controllers['config'].wind_speed_min
        self.event.max_allowed_wind_speed=self.controllers['config'].wind_speed_max

        self.chronoHard.reset()
        self.chronodata.reset()
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor(),
                                                      self.event.get_current_round().round_number)
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        self.show_chrono()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def next_action(self):
        self.chronoHard.chrono_signal.emit("btnnext","event","btnnext")

    def btn_next_action(self, port):
        self.chronoHard.chrono_signal.emit("btnnext","event","btnnext")

    def btn_baseA(self, port):
        print("btn base A")
        self.chronoHard.chrono_signal.emit("udpreceive","event","baseA")

    def btn_baseB(self, port):
        print("btn base B")
        self.chronoHard.chrono_signal.emit("udpreceive","event","baseB")
    
    def slot_buzzer(self):
        if (self.buzzer):
            self.buzzer.event.set()

    def penalty_100(self):
        #print("penalty event 100")
        self.vocal.sound_penalty()
        self.chronoHard.addPenalty(100)
        self.controllers['round'].wChronoCtrl.set_penalty_value(self.chronoHard.getPenalty())

    def penalty_1000(self):
        self.vocal.sound_penalty()
        self.chronoHard.addPenalty(1000)
        self.controllers['round'].wChronoCtrl.set_penalty_value(self.chronoHard.getPenalty())

    def clear_penalty(self):
        self.chronoHard.clearPenalty()
        self.controllers['round'].wChronoCtrl.set_penalty_value(self.chronoHard.getPenalty())

    def cancel_round(self):
        self.event.get_current_round().cancel_round()
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor(),
                                                      self.event.get_current_round().round_number)
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
        self.event = self.dao.get(self.controllers['config'].view.ContestList.currentIndex())

        self.controllers['config'].set_data(self.event.min_allowed_wind_speed,
                                            self.event.max_allowed_wind_speed,
                                            self.event.max_wind_dir_dev,
                                            self.event.max_interruption_time)

    def chronotype_changed(self):
        if (self.controllers['config'].view.ChronoType.currentIndex()==0):
            self.chronoHard = self.chronoRpi
        else:
            self.chronoHard = self.chronoArduino
        self.chronoHard.reset()

    def slot_status_changed(self, status):
        self.controllers['round'].wChronoCtrl.set_status(status)
        if (status==chronoStatus.WaitLaunch):
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (status == chronoStatus.Launched):
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (status == chronoStatus.InProgress):
            self.controllers['round'].wChronoCtrl.settime(0, True)

    def slot_lap_finished (self, lap, last_lap_time):
        self.controllers['round'].wChronoCtrl.set_laptime(last_lap_time)
        self.vocal.sound_base(lap)

    def slot_run_finished(self, run_time):
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.set_finaltime(run_time)
        self.vocal.sound_time(run_time)

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

def main ():

    dao = EventDAO()
    chronodata = Chrono()
    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(dao, chronodata, False)



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
