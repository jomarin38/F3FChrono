# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulate_base.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(562, 160)
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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.ip_A = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_A.setObjectName("ip_A")
        self.horizontalLayout_2.addWidget(self.ip_A)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setMinimumSize(QtCore.QSize(72, 0))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.data_A = QtWidgets.QLineEdit(self.centralwidget)
        self.data_A.setObjectName("data_A")
        self.horizontalLayout_3.addWidget(self.data_A)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.btn_send_A = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_A.setObjectName("btn_send_A")
        self.verticalLayout.addWidget(self.btn_send_A)
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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.ip_B = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_B.setObjectName("ip_B")
        self.horizontalLayout_4.addWidget(self.ip_B)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setMinimumSize(QtCore.QSize(72, 0))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.data_B = QtWidgets.QLineEdit(self.centralwidget)
        self.data_B.setObjectName("data_B")
        self.horizontalLayout_5.addWidget(self.data_B)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.btn_send_B = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_B.setObjectName("btn_send_B")
        self.verticalLayout_2.addWidget(self.btn_send_B)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
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
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.btn_send_wind = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_wind.setObjectName("btn_send_wind")
        self.verticalLayout_5.addWidget(self.btn_send_wind)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chrono Simulate Bases"))
        self.label.setText(_translate("MainWindow", "Base A"))
        self.label_3.setText(_translate("MainWindow", "IP Address"))
        self.ip_A.setText(_translate("MainWindow", "192.168.0.10"))
        self.label_5.setText(_translate("MainWindow", "Data"))
        self.data_A.setText(_translate("MainWindow", "event"))
        self.btn_send_A.setText(_translate("MainWindow", "Send UDP"))
        self.label_2.setText(_translate("MainWindow", "Base B"))
        self.label_4.setText(_translate("MainWindow", "IP Address"))
        self.ip_B.setText(_translate("MainWindow", "192.168.0.11"))
        self.label_6.setText(_translate("MainWindow", "Data"))
        self.data_B.setText(_translate("MainWindow", "event"))
        self.btn_send_B.setText(_translate("MainWindow", "Send UDP"))
        self.label_9.setText(_translate("MainWindow", "Weather"))
        self.label_8.setText(_translate("MainWindow", "Speed\n"
"(m/s)"))
        self.label_7.setText(_translate("MainWindow", "Dir (°)"))
        self.label_10.setText(_translate("MainWindow", "Rain"))
        self.btn_send_wind.setText(_translate("MainWindow", "Send Weather"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
