import collections

from F3FChrono.uichronotest.MainUi_UI import *
from F3FChrono.uichronotest.WidgetController import *
from F3FChrono.data.Event import Event

global ui


class MainUiCtrl (QtWidgets.QMainWindow):

    def __init__(self, event):
        super().__init__()
        self.initUI()
        self.event = event

    def initUI(self):
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self.MainWindow)

        self.controllers = collections.OrderedDict()

        self.controllers['competitor'] = WTopCtrl("panel Top", self.ui.centralwidget)
        self.controllers['chrono'] = WChronoCtrl("panel Chrono", self.ui.centralwidget)

        self.controllers['config'] = WHomeCtrl("panel Home", self.ui.centralwidget)

        self.controllers['bottom'] = WBottomCtrl("panel Bottom", self.ui.centralwidget)

        for key, ctrl in self.controllers.items():
            self.ui.verticalLayout.addWidget(ctrl.get_widget())

        self.set_page(0)
        self.MainWindow.show()

    def set_page(self, page):
        if page==0:
            self.controllers['competitor'].widget.show()
            self.controllers['chrono'].widget.show()
            self.controllers['config'].widget.hide()
        if page==1:
            self.controllers['competitor'].widget.hide()
            self.controllers['chrono'].widget.hide()
            self.controllers['config'].widget.show()

    def set_initial_data(self):
        self.controllers['competitor'].set_data(self.event.get_current_round().get_current_competitor())

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