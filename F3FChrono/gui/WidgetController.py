import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject

from F3FChrono.gui.WWind_UI import Ui_WWind
from F3FChrono.gui.WPilot_UI import Ui_WPilot
from F3FChrono.gui.WChrono_ui import Ui_WChrono
from F3FChrono.gui.WChronoBtn_ui import Ui_WChronoBtn
from F3FChrono.gui.WConfig_ui import Ui_WConfig


class WRoundCtrl(QObject):
    btn_next_sig = pyqtSignal()
    btn_home_sig = pyqtSignal()
    btn_refly_sig = pyqtSignal()

    widgetList = []

    def __init__(self, name, parent):
        super(QObject, self).__init__(parent)
        self.wPilotCtrl = WPilotCtrl("PilotCtrl", parent)
        self.wChronoCtrl = WChronoCtrl("ChronoCtrl", parent)
        self.view = Ui_WChronoBtn()
        self.name = name
        self.parent = parent
        self.widget=QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.wPilotCtrl.get_widget())
        self.widgetList.append(self.wChronoCtrl.get_widget())
        self.widgetList.append(self.widget)
        # Event connect
        self.view.Btn_Home.clicked.connect(self.btn_home)
        self.view.Btn_Next.clicked.connect(self.btn_next_pilot)
        self.view.Btn_reflight.clicked.connect(self.btn_refly)

    def get_widget(self):
        return (self.widgetList)

    def show(self):
        self.widget.show()
        self.wPilotCtrl.show()
        self.wChronoCtrl.show()

    def hide(self):
        self.widget.hide()
        self.wPilotCtrl.hide()
        self.wChronoCtrl.hide()

    def btn_next_pilot(self):
        self.btn_next_sig.emit()

    def btn_home(self):
        self.btn_home_sig.emit()

    def btn_refly(self):
        self.btn_refly_sig.emit()

    def set_data(self):
        """
            TODO: roundCtrl.set_data
        """

class WWindCtrl:
    widgetList = []

    def __init__(self, name, parent):
        self.view = Ui_WWind()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)
    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def set_data(self, wind, angle):
        self.view.WindInfo.setText('Wind : '+str(wind)+'m.s, Angle : '+str(angle)+'°')

class WPilotCtrl:
    def __init__(self, name, parent):
        self.view = Ui_WPilot()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)

    def get_widget(self):
        return(self.widget)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def set_data(self, competitor):
        self.view.pilotName.setText(competitor.display_name())
        self.view.bib.setText(str(competitor.get_bib_number()))

class WChronoCtrl():

    def __init__(self, name, parent):
        self.view = Ui_WChrono()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)

    def get_widget(self):
        return (self.widget)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

class WConfigCtrl(QObject):
    btn_next_sig = pyqtSignal()
    widgetList = []

    def __init__(self, name, parent):
        super(QObject, self).__init__(parent)
        self.view = Ui_WConfig()
        self.name = name
        self.parent = parent
        self.widget = QtWidgets.QWidget(parent)
        self.view.setupUi(self.widget)
        self.widgetList.append(self.widget)

        # Event connect
        self.view.StartBtn.clicked.connect(self.btn_next)

    def get_widget(self):
        return(self.widgetList)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def btn_next(self):
        self.btn_next_sig.emit()

    def set_data(self, contest, min_speed, max_speed, dir_dev, max_interrupt, revol=5):
        self.view.ContestList.addItem(contest)
        self.view.ContestList.setCurrentText(contest)
        self.view.WindMinValue.setValue(min_speed)
        self.view.WindMaxValue.setValue(max_speed)
        self.view.OrientationValue.setValue(dir_dev)
        self.view.RevolValue.setValue(revol)
        self.view.MaxInterruptValue.setValue(max_interrupt)