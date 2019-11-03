import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot

from MainUi_UI import *
from WidgetController import *

global ui

class MainUiCtrl (QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.MainWindow = QtWidgets.QMainWindow()

        self.controllers = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.controllers.append(WTopCtrl("panel Top", self.ui.centralwidget))
        self.controllers.append(WHomeCtrl("panel Home", self.ui.centralwidget))
        self.controllers.append(WChronoCtrl("panel Chrono", self.ui.centralwidget))
        self.controllers.append(WBottomCtrl("panel Bottom", self.ui.centralwidget))

        for c in self.controllers:
            self.ui.verticalLayout.addWidget(c.get_widget())
        self.set_page(1)
        self.MainWindow.show()

    def set_page(self, page):
        if page==0:
            self.controllers[1].widget.show()
            self.controllers[2].widget.hide()
        if page==1:
            self.controllers[1].widget.hide()
            self.controllers[2].widget.show()

def main ():

    app = QtWidgets.QApplication(sys.argv)
    ui=MainUiCtrl()

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