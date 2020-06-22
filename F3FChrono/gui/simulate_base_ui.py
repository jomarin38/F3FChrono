# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulate_base.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1016, 231)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listBaseA = QtWidgets.QListWidget(self.centralwidget)
        self.listBaseA.setObjectName("listBaseA")
        self.verticalLayout.addWidget(self.listBaseA)
        self.btn_gpio_A = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gpio_A.setObjectName("btn_gpio_A")
        self.verticalLayout.addWidget(self.btn_gpio_A)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.listBaseB = QtWidgets.QListWidget(self.centralwidget)
        self.listBaseB.setObjectName("listBaseB")
        self.verticalLayout_2.addWidget(self.listBaseB)
        self.btn_gpio_B = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gpio_B.setObjectName("btn_gpio_B")
        self.verticalLayout_2.addWidget(self.btn_gpio_B)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.btn_next = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next.setObjectName("btn_next")
        self.horizontalLayout.addWidget(self.btn_next)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_5.addWidget(self.label_9)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setMinimumSize(QtCore.QSize(0, 15))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8)
        self.wind_speed = QtWidgets.QSpinBox(self.centralwidget)
        self.wind_speed.setMaximum(30)
        self.wind_speed.setProperty("value", 3)
        self.wind_speed.setObjectName("wind_speed")
        self.verticalLayout_4.addWidget(self.wind_speed)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setMinimumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.wind_dir = QtWidgets.QSpinBox(self.centralwidget)
        self.wind_dir.setEnabled(True)
        self.wind_dir.setMinimum(-90)
        self.wind_dir.setMaximum(90)
        self.wind_dir.setObjectName("wind_dir")
        self.verticalLayout_6.addWidget(self.wind_dir)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        self.rain = QtWidgets.QCheckBox(self.centralwidget)
        self.rain.setText("")
        self.rain.setObjectName("rain")
        self.verticalLayout_3.addWidget(self.rain)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setMinimumSize(QtCore.QSize(0, 15))
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_14.addWidget(self.label_22)
        self.AccuRace = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.AccuRace.setDecimals(1)
        self.AccuRace.setMinimum(9.0)
        self.AccuRace.setMaximum(12.6)
        self.AccuRace.setSingleStep(0.1)
        self.AccuRace.setProperty("value", 11.8)
        self.AccuRace.setObjectName("AccuRace")
        self.verticalLayout_14.addWidget(self.AccuRace)
        self.horizontalLayout_6.addLayout(self.verticalLayout_14)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setMinimumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_15.addWidget(self.label_23)
        self.rssi_picam1 = QtWidgets.QSpinBox(self.centralwidget)
        self.rssi_picam1.setEnabled(True)
        self.rssi_picam1.setMinimum(0)
        self.rssi_picam1.setMaximum(100)
        self.rssi_picam1.setProperty("value", 90)
        self.rssi_picam1.setObjectName("rssi_picam1")
        self.verticalLayout_15.addWidget(self.rssi_picam1)
        self.horizontalLayout_6.addLayout(self.verticalLayout_15)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_16.addWidget(self.label_24)
        self.rssi_picam2 = QtWidgets.QSpinBox(self.centralwidget)
        self.rssi_picam2.setEnabled(True)
        self.rssi_picam2.setMinimum(0)
        self.rssi_picam2.setMaximum(100)
        self.rssi_picam2.setProperty("value", 95)
        self.rssi_picam2.setObjectName("rssi_picam2")
        self.verticalLayout_16.addWidget(self.rssi_picam2)
        self.horizontalLayout_13.addLayout(self.verticalLayout_16)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_13)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.btn_send_wind = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_wind.setObjectName("btn_send_wind")
        self.verticalLayout_5.addWidget(self.btn_send_wind)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chrono Simulate Bases"))
        self.label.setText(_translate("MainWindow", "Base A"))
        self.btn_gpio_A.setText(_translate("MainWindow", "GPIO Btn"))
        self.label_2.setText(_translate("MainWindow", "Base B"))
        self.btn_gpio_B.setText(_translate("MainWindow", "GPIO Btn"))
        self.btn_next.setText(_translate("MainWindow", "btn Next"))
        self.label_9.setText(_translate("MainWindow", "Info"))
        self.label_8.setText(_translate("MainWindow", "Speed\n"
"(m/s)"))
        self.label_7.setText(_translate("MainWindow", "Dir (°)"))
        self.label_10.setText(_translate("MainWindow", "Rain"))
        self.label_22.setText(_translate("MainWindow", "Accu"))
        self.label_23.setText(_translate("MainWindow", "PiCAM1 RSSI"))
        self.label_24.setText(_translate("MainWindow", "PICAM2 RSSI"))
        self.btn_send_wind.setText(_translate("MainWindow", "Send info"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
