import collections

from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.chrono.Chrono import *
from F3FChrono.data.dao.EventDAO import EventDAO, RoundDAO
from F3FChrono.data.Chrono import Chrono



class MainUiCtrl (QtWidgets.QMainWindow, QObject):

    refresh_chronoui = pyqtSignal(str, str, str)
    refresh_windui = pyqtSignal(int, int)

    def __init__(self, dao, chronodata, chronohard):
        super(QObject, self).__init__()
        self.dao = dao
        self.daoRound = RoundDAO()
        self.event = None
        self.chronodata = chronodata
        self.chronoHard = chronohard
        self.initUI()
        self.base_test = -10

        self.refresh_chronoui.connect(self.process_ui)
        self.refresh_windui.connect(self.wind_ui)


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
        self.controllers['wind'].set_data(0, 0)

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
        #add event to database
        '''for f3f_round in self.event.rounds:
            self.daoRound.insert(f3f_round)
        '''
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
        self.refresh_chronoui.emit("btnnext","event","btnnext")
        '''if (self.chronoHard.get_status()<chronoStatus.Finished):
            if (self.chronoHard.get_status()==chronoStatus.InStart):
                self.chronoHard.declareBase(self.base_test)
                self.base_test = ~self.base_test
                self.controllers['round'].wChronoCtrl.settime(0, True)

            if (self.chronoHard.get_status()==chronoStatus.InProgress and self.chronoHard.getLapCount()<=10):
                self.chronoHard.declareBase(self.base_test)
                self.base_test=~self.base_test
                self.controllers['round'].wChronoCtrl.set_laptime(self.chronoHard.getLastLapTime())
                self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
                if (self.chronoHard.getLapCount() == 10):
                    self.controllers['round'].wChronoCtrl.stoptime()
                    self.chronoHard.next_status()
                    self.controllers['round'].wChronoCtrl.set_finaltime(self.chronoHard.get_time())
                    self.chronoHard_to_chrono(self.chronoHard, self.chronodata)

            else:
                self.chronoHard.next_status()

            self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        else:
            self.event.get_current_round().handle_terminated_flight(self.event.get_current_round().get_current_competitor(),
                                                                    self.chronodata, self.chronoHard.getPenalty(), True, insert_database=True)
            self.chronoHard.reset()
            self.chronodata=Chrono()
            self.next_pilot(insert_database=True)
            self.controllers['round'].wChronoCtrl.settime(30000, False, False)
            self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        if (self.chronoHard.get_status() == chronoStatus.WaitLaunch):
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (self.chronoHard.get_status() == chronoStatus.Launched):
            self.controllers['round'].wChronoCtrl.settime(30000, False)
'''

    def penalty_100(self):
        #print("penalty event 100")
        self.chronoHard.addPenalty(100)
        self.controllers['round'].wChronoCtrl.set_penalty_value(self.chronoHard.getPenalty())

    def penalty_1000(self):
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

    def process_ui(self, caller, data, address):
        print("process ui : \n"+"\tdata : "+data+"\n\taddress : "+address)
        status=self.chronoHard.get_status()
        if (status< chronoStatus.Finished):
            if (status == chronoStatus.InStart):
                self.chronoHard.declareBase(address)
                self.controllers['round'].wChronoCtrl.settime(0, True)

            if (status == chronoStatus.InProgress and self.chronoHard.getLapCount() <= 10):
                if self.chronoHard.declareBase(address):
                    #detection is not the same base : processing
                    self.controllers['round'].wChronoCtrl.set_laptime(self.chronoHard.getLastLapTime())
                    self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
                    if (self.chronoHard.getLapCount() == 10):
                        self.controllers['round'].wChronoCtrl.stoptime()
                        self.chronoHard.next_status()
                        self.controllers['round'].wChronoCtrl.set_finaltime(self.chronoHard.get_time())
                        self.chronoHard_to_chrono(self.chronoHard, self.chronodata)
            else:
                if caller=="btnnext" or \
                        (caller=="udpreceive" and  (status == chronoStatus.InStart or status==chronoStatus.Launched)):
                    self.chronoHard.next_status()
            self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        else:
            if (caller=='btnnext'):
                self.event.get_current_round().handle_terminated_flight(
                    self.event.get_current_round().get_current_competitor(),
                    self.chronodata, self.chronoHard.getPenalty(), True, insert_database=True)
                self.chronoHard.reset()
                self.chronodata = Chrono()
                self.next_pilot(insert_database=True)
                self.controllers['round'].wChronoCtrl.settime(30000, False, False)
                self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        if (self.chronoHard.get_status() == chronoStatus.WaitLaunch):
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (self.chronoHard.get_status() == chronoStatus.Launched):
            self.controllers['round'].wChronoCtrl.settime(30000, False)

    def wind_ui(self, wind, angle):
        print ("Wind UI")
        self.controllers['wind'].set_data(wind, angle)

def main ():

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
    main()
