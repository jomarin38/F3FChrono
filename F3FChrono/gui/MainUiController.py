import collections

from F3FChrono.gui.MainUi_UI import *
from F3FChrono.gui.WidgetController import *
from F3FChrono.data.Event import Event


class MainUiCtrl (QtWidgets.QMainWindow):

    def __init__(self, event):
        super().__init__()
        self.event = event
        self.initUI()

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

        self.controllers['config'].btn_next_sig.connect(self.show_chrono)
        self.controllers['round'].btn_next_sig.connect(self.next_pilot)
        self.controllers['round'].btn_home_sig.connect(self.show_config)
        self.controllers['round'].btn_refly_sig.connect(self.refly)

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

    def refly(self):
        #TODO : get penalty value if any
        self.event.get_current_round().handle_refly(0)
        self.next_pilot()

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

    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl(event)

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