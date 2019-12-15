import collections

from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.data.Event import Event
from F3FChrono.chrono.Chrono import *

from F3FChrono.data.dao.EventDAO import EventDAO


class MainUiCtrl (QtWidgets.QMainWindow):

    def __init__(self,event,chrono):
        super().__init__()
        self.event = event
        self.chrono = chrono
        self.initUI()
        self.base_test=0


    def initUI(self):
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.MainWindow)
        self.MainWindow.showFullScreen()
        self.controllers = collections.OrderedDict()

        self.controllers['config'] = WConfigCtrl("panel Config", self.ui.centralwidget)
        self.controllers['round'] = WRoundCtrl("panel Chrono", self.ui.centralwidget)
        self.controllers['wind'] = WWindCtrl("panel Wind", self.ui.centralwidget)

        for key, ctrl in self.controllers.items():
            for x in ctrl.get_widget():
                self.ui.verticalLayout.addWidget(x)

        self.controllers['config'].btn_next_sig.connect(self.start)
        self.controllers['round'].btn_next_sig.connect(self.next_action)
        self.controllers['round'].btn_home_sig.connect(self.show_config)
        self.controllers['round'].btn_refly_sig.connect(self.refly)
        self.controllers['round'].btn_penalty_sig.connect(self.penalty)
        self.controllers['round'].btn_null_flight_sig.connect(self.null_flight)

        self.show_config()
        self.MainWindow.show()

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

    def next_pilot(self):
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().next_pilot())
        self.controllers['round'].wChronoCtrl.reset_ui()

    def refly(self):
        #TODO : get penalty value if any
        self.event.get_current_round().handle_refly(0)
        self.chrono.reset()
        self.next_pilot()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def start(self):
        self.controllers['config'].get_data()
        self.event.max_interruption_time=self.controllers['config'].interruption_time_max
        self.event.max_wind_dir_dev=self.controllers['config'].wind_orientation
        self.event.min_allowed_wind_speed=self.controllers['config'].wind_speed_min
        self.event.max_allowed_wind_speed=self.controllers['config'].wind_speed_max
        self.chrono.reset()
        self.controllers['round'].wChronoCtrl.set_status(self.chrono.get_status())
        self.show_chrono()
        self.controllers['round'].wChronoCtrl.reset_ui()

    def next_action(self):
        if (self.chrono.get_status()<chronoStatus.Finished):
            if (self.chrono.get_status()==chronoStatus.InStart):
                self.chrono.startRace()
                self.chrono.declareBase(self.base_test)
                self.base_test = ~self.base_test
                self.controllers['round'].wChronoCtrl.reset_ui()
                self.controllers['round'].wChronoCtrl.settime(0, True)

            if (self.chrono.get_status()==chronoStatus.InProgress and self.chrono.getLapCount()<=10):
                if (self.chrono.getLapCount() == 10):
                    self.controllers['round'].wChronoCtrl.stoptime()
                    self.chrono.next_status()
                print("chronolapcount : "+str(self.chrono.getLapCount()))
                self.chrono.declareBase(self.base_test)
                self.base_test=~self.base_test
                self.controllers['round'].wChronoCtrl.set_laptime(self.chrono.getLastLapTime())
                self.controllers['round'].wChronoCtrl.set_status(self.chrono.get_status())

            else:
                self.chrono.next_status()

            self.controllers['round'].wChronoCtrl.set_status(self.chrono.get_status())
        elif (self.chrono.getLapCount()>=10):
            self.chrono.reset()
            self.next_pilot()
            self.controllers['round'].wChronoCtrl.set_status(self.chrono.get_status())
        if (self.chrono.get_status() == chronoStatus.WaitLaunch):
            self.controllers['round'].wChronoCtrl.settime(30000, False)
        if (self.chrono.get_status() == chronoStatus.Launched):
            self.controllers['round'].wChronoCtrl.settime(30000, False)


    def penalty(self):
        "TODO Insert event class penalty function"
        print("penalty event")

    def null_flight(self):
        "TODO Insert event class null flight function"
        print("null flight event")

    def set_initial_data(self):
        print("initial_data method")
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor())
        self.controllers['wind'].set_data(0, 0)
        self.controllers['config'].set_data(self.event.location,
                                            self.event.min_allowed_wind_speed,
                                            self.event.max_allowed_wind_speed,
                                            self.event.max_wind_dir_dev,
                                            self.event.max_interruption_time)

def main ():
    contest_id = 1

    dao = EventDAO()
    event = dao.get(contest_id, fetch_competitors=True, fetch_rounds=True, fetch_runs=True)
    chrono = Chrono()

    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(event, chrono)

    ui.set_initial_data()

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
