import collections

from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.data.Event import Event
from F3FChrono.chrono.Chrono import *

from F3FChrono.data.dao.EventDAO import EventDAO, RoundDAO
from F3FChrono.data.Chrono import Chrono



class MainUiCtrl (QtWidgets.QMainWindow):

    def __init__(self,dao,chrono):
        super().__init__()
        self.dao = dao
        self.daoRound = RoundDAO()
        self.event = None
        self.chrono = chrono
        self.chronoHard=ChronoHard()
        self.initUI()
        self.base_test=-10


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
        self.controllers['round'].btn_penalty_1_sig.connect(self.penalty_1)
        self.controllers['round'].btn_penalty_2_sig.connect(self.penalty_2)
        self.controllers['round'].btn_null_flight_sig.connect(self.null_flight)
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

    def next_pilot(self):
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().next_pilot(),
                                                      self.event.get_current_round().round_number)
        self.controllers['round'].wChronoCtrl.reset_ui()

    def refly(self):
        #TODO : get penalty value if any
        self.event.get_current_round().handle_refly(0)
        self.chronoHard.reset()
        self.chrono.reset()
        self.next_pilot()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def start(self):
        self.controllers['config'].get_data()
        self.event.max_interruption_time=self.controllers['config'].interruption_time_max
        self.event.max_wind_dir_dev=self.controllers['config'].wind_orientation
        self.event.min_allowed_wind_speed=self.controllers['config'].wind_speed_min
        self.event.max_allowed_wind_speed=self.controllers['config'].wind_speed_max

        self.chronoHard.reset()
        self.chrono.reset()
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor(),
                                                      self.event.get_current_round().round_number)
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        self.show_chrono()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def next_action(self):
        if (self.chronoHard.get_status()<chronoStatus.Finished):
            if (self.chronoHard.get_status()==chronoStatus.InStart):
                self.chronoHard.declareBase(self.base_test)
                self.base_test = ~self.base_test
                self.controllers['round'].wChronoCtrl.reset_ui()
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
                    self.chronoHard_to_chrono(self.chronoHard, self.chrono)

            else:
                self.chronoHard.next_status()

            self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        elif (self.chronoHard.getLapCount()>=10):
            self.event.get_current_round().handle_terminated_flight(self.event.get_current_round().get_current_competitor(),
                                                                    self.chrono, self.chronoHard.getPenalty(), True)

            self.chronoHard.reset()
            self.chrono=Chrono()
            self.next_pilot()
            self.controllers['round'].wChronoCtrl.settime(30000, False, False)
            self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())
        if (self.chronoHard.get_status() == chronoStatus.WaitLaunch):
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (self.chronoHard.get_status() == chronoStatus.Launched):
            self.controllers['round'].wChronoCtrl.settime(30000, False)


    def penalty_1(self):
        #print("penalty event 100")
        self.chronoHard.AddPenalty(100)

    def penalty_2(self):
        #print("penalty event 1000")
        self.chronoHard.AddPenalty(1000)

    def cancel_round(self):
        #print("cancel round event")
        self.event.get_current_round().cancel_round()
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor(),
                                                      self.event.get_current_round().round_number)
        self.chronoHard.reset()
        self.chrono.reset()
        self.controllers['round'].wChronoCtrl.stoptime()
        self.controllers['round'].wChronoCtrl.reset_ui()
        self.controllers['round'].wChronoCtrl.set_status(self.chronoHard.get_status())

    def null_flight(self):
        #TODO Insert event class null flight function
        print("null flight event")
        self.event.get_current_round().handle_terminated_flight(self.event.get_competitors(),
                                                                None, None, self.chrono.penalty, True)
        self.controllers['round'].wChronoCtrl.set_status(chronoStatus.Finished)
        self.chronoHard.reset()
        self.chrono.reset()
        self.next_pilot()

    def contest_changed(self):
        self.event=self.dao.get(self.controllers['config'].view.ContestList.currentIndex(),
                                fetch_competitors=True, fetch_rounds=True, fetch_runs=True)

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


def main ():

    dao = EventDAO()
    chrono = Chrono()

    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(dao, chrono)



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
