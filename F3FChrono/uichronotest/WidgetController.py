import sys
from PyQt5 import QtWidgets, QtCore


from WBottom_UI import Ui_WBottom
from WTop_UI import Ui_WTop
from WChrono_ui import Ui_WChrono
from WHome_ui import Ui_WHome



class WBottomCtrl:
    def __init__(self, name, parent):
        self.view = Ui_WBottom ()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)

    def get_widget(self):
        return self.widget

    def btnFct(self):
        print(self.name + "Btn Fct")

    def set_data(self, wind, race_info):
        self.view.WindInfo.setText(wind)
        self.view.RaceInfo.setText(race_info)


class WTopCtrl:
    def __init__(self, name, parent):
        self.view = Ui_WTop()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.set_data("Pilot : ___ ____", 'Run : XX')

    def get_widget(self):
        return self.widget

    def set_data(self, pilot, run):
        self.view.PilotName.setText(pilot)
        self.view.RaceInfo.setText(run)

class WChronoCtrl:
    def __init__(self, name, parent):
        self.view = Ui_WChrono()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)

        # Event connect
        self.view.Btn_Home.clicked.connect(self.btn_home)

    def get_widget(self):
        return self.widget

    def btn_home(self):
        print(self.name + "Btn Home")



class WHomeCtrl:
    def __init__(self, name, parent):
        self.view = Ui_WHome()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)

        # Event connect
        #self.view.pushButton.clicked.connect(self.btnFct)

    def get_widget(self):
        return self.widget

    def btnFct(self):
        print(self.name + "Btn Fct")