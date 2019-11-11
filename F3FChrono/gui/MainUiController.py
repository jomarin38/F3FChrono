import collections

from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.data.Event import Event
from F3FChrono.chrono.Chrono import *


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
        self.controllers['round'].btn_penalty_sig.connect(self.penalty)
        self.controllers['round'].btn_revol_sig.connect(self.reflight)
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

    def start(self):
        self.controllers['config'].get_data()
        self.event._max_interruption_time=self.controllers['config'].interruption_time_max
        self.event._max_wind_dir_dev=self.controllers['config'].wind_orientation
        self.event._min_allowed_wind_speed=self.controllers['config'].wind_speed_min
        self.event._max_allowed_wind_speed=self.controllers['config'].wind_speed_max
        self.chrono.reset()
        self.controllers['round'].wChronoCtrl.set_status(self.chrono.get_status())
        self.show_chrono()

    def next_action(self):
        print ("Fctnext_action begin\tchrono status"+str(self.chrono.get_status())+'\tNb lap : '+str(self.chrono.getLapCount()))
        if (self.chrono.get_status()<chronoStatus.Finished):
            if (self.chrono.get_status()==chronoStatus.InProgress and self.chrono.getLapCount()<10):
                self.chrono.declareBase(self.base_test)
                self.base_test=~self.base_test
            else:
                self.chrono.next_status()
        elif(self.chrono.getLapCount()>=10):
            self.chrono.reset()
            self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().next_pilot())
        self.controllers['round'].wChronoCtrl.set_status(self.chrono.get_status())
        print ("Fctnext_action end\tchrono status"+str(self.chrono.get_status())+'\tNb lap : '+str(self.chrono.getLapCount()))

    def penalty(self):
        "TODO Insert event class penalty function"
        print("penalty event")

    def reflight(self):
        "TODO Insert event class reflight function"
        print("reflight event")

    def null_flight(self):
        "TODO Insert event class null flight function"
        print("null flight event")

    def set_initial_data(self):
        print("initial_data method")
        self.controllers['round'].wPilotCtrl.set_data(self.event.get_current_round().get_current_competitor())
        self.controllers['wind'].set_data(0, 0)
        self.controllers['config'].set_data(self.event._location,
                                            self.event._min_allowed_wind_speed,
                                            self.event._max_allowed_wind_speed,
                                            self.event._max_wind_dir_dev,
                                            self.event._max_interruption_time)

def main ():

    login = input('F3X Vault login : ')
    password = input('F3X Vault password : ')
    contest_id = 1706

    event = Event.from_f3x_vault(login, password, contest_id, max_rounds=1)
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