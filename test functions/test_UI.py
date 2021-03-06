# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(323, 330)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.end_file = QtWidgets.QSpinBox(self.centralwidget)
        self.end_file.setMaximum(65535)
        self.end_file.setProperty("value", 100)
        self.end_file.setObjectName("end_file")
        self.gridLayout_2.addWidget(self.end_file, 8, 1, 1, 1)
        self.button_lowvoltage = QtWidgets.QPushButton(self.centralwidget)
        self.button_lowvoltage.setObjectName("button_lowvoltage")
        self.gridLayout_2.addWidget(self.button_lowvoltage, 7, 2, 1, 1)
        self.base = QtWidgets.QSpinBox(self.centralwidget)
        self.base.setObjectName("base")
        self.gridLayout_2.addWidget(self.base, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.button_time = QtWidgets.QPushButton(self.centralwidget)
        self.button_time.setObjectName("button_time")
        self.gridLayout_2.addWidget(self.button_time, 2, 2, 1, 1)
        self.pilotnumber = QtWidgets.QSpinBox(self.centralwidget)
        self.pilotnumber.setObjectName("pilotnumber")
        self.gridLayout_2.addWidget(self.pilotnumber, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.start_file = QtWidgets.QSpinBox(self.centralwidget)
        self.start_file.setMaximum(65535)
        self.start_file.setProperty("value", 1)
        self.start_file.setObjectName("start_file")
        self.gridLayout_2.addWidget(self.start_file, 8, 0, 1, 1)
        self.finaltime = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.finaltime.setMaximum(100000.0)
        self.finaltime.setObjectName("finaltime")
        self.gridLayout_2.addWidget(self.finaltime, 2, 1, 1, 1)
        self.buttonconvert = QtWidgets.QPushButton(self.centralwidget)
        self.buttonconvert.setObjectName("buttonconvert")
        self.gridLayout_2.addWidget(self.buttonconvert, 8, 2, 1, 1)
        self.button_pilot = QtWidgets.QPushButton(self.centralwidget)
        self.button_pilot.setObjectName("button_pilot")
        self.gridLayout_2.addWidget(self.button_pilot, 1, 2, 1, 1)
        self.button_quit = QtWidgets.QPushButton(self.centralwidget)
        self.button_quit.setObjectName("button_quit")
        self.gridLayout_2.addWidget(self.button_quit, 9, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.button_base = QtWidgets.QPushButton(self.centralwidget)
        self.button_base.setObjectName("button_base")
        self.gridLayout_2.addWidget(self.button_base, 3, 2, 1, 1)
        self.button_penalty = QtWidgets.QPushButton(self.centralwidget)
        self.button_penalty.setObjectName("button_penalty")
        self.gridLayout_2.addWidget(self.button_penalty, 6, 2, 1, 1)
        self.elapsed_time = QtWidgets.QSpinBox(self.centralwidget)
        self.elapsed_time.setObjectName("elapsed_time")
        self.gridLayout_2.addWidget(self.elapsed_time, 4, 1, 1, 1)
        self.button_instart = QtWidgets.QPushButton(self.centralwidget)
        self.button_instart.setObjectName("button_instart")
        self.gridLayout_2.addWidget(self.button_instart, 5, 2, 1, 1)
        self.button_elapsedtime = QtWidgets.QPushButton(self.centralwidget)
        self.button_elapsedtime.setObjectName("button_elapsedtime")
        self.gridLayout_2.addWidget(self.button_elapsedtime, 4, 2, 1, 1)
        self.button_reload = QtWidgets.QPushButton(self.centralwidget)
        self.button_reload.setObjectName("button_reload")
        self.gridLayout_2.addWidget(self.button_reload, 0, 2, 1, 1)
        self.comboBox_language = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_language.setObjectName("comboBox_language")
        self.comboBox_language.addItem("")
        self.comboBox_language.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_language, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_lowvoltage.setText(_translate("MainWindow", "LowVoltage"))
        self.label.setText(_translate("MainWindow", "Pilote Number"))
        self.button_time.setText(_translate("MainWindow", "PlaySound"))
        self.label_4.setText(_translate("MainWindow", "Elapsed time"))
        self.label_2.setText(_translate("MainWindow", "Final Time"))
        self.buttonconvert.setText(_translate("MainWindow", "Convertfile"))
        self.button_pilot.setText(_translate("MainWindow", "PlaySound"))
        self.button_quit.setText(_translate("MainWindow", "Quit"))
        self.label_3.setText(_translate("MainWindow", "Base"))
        self.button_base.setText(_translate("MainWindow", "PlaySound"))
        self.button_penalty.setText(_translate("MainWindow", "Penalty"))
        self.button_instart.setText(_translate("MainWindow", "inStart"))
        self.button_elapsedtime.setText(_translate("MainWindow", "PlaySound"))
        self.button_reload.setText(_translate("MainWindow", "Reload"))
        self.comboBox_language.setItemText(0, _translate("MainWindow", "French"))
        self.comboBox_language.setItemText(1, _translate("MainWindow", "English"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
