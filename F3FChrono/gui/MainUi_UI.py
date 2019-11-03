# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUi.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(636, 624)
        MainWindow.setMaximumSize(QtCore.QSize(1024, 768))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3.addLayout(self.verticalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionInStart = QtWidgets.QAction(MainWindow)
        self.actionInStart.setObjectName("actionInStart")
        self.actionResetChrono = QtWidgets.QAction(MainWindow)
        self.actionResetChrono.setObjectName("actionResetChrono")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionHomeNext = QtWidgets.QAction(MainWindow)
        self.actionHomeNext.setObjectName("actionHomeNext")
        self.actionCheckPicam = QtWidgets.QAction(MainWindow)
        self.actionCheckPicam.setObjectName("actionCheckPicam")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.actionInStart.setText(_translate("MainWindow", "InStart"))
        self.actionResetChrono.setText(_translate("MainWindow", "ResetChrono"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save"))
        self.actionHomeNext.setText(_translate("MainWindow", "HomeNext"))
        self.actionCheckPicam.setText(_translate("MainWindow", "CheckPicam"))
        self.actionCheckPicam.setToolTip(_translate("MainWindow", "CheckPicam"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

