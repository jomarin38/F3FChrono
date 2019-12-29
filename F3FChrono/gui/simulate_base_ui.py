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
        MainWindow.resize(480, 246)
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
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.ip_A = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_A.setObjectName("ip_A")
        self.verticalLayout.addWidget(self.ip_A)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.data_A = QtWidgets.QLineEdit(self.centralwidget)
        self.data_A.setObjectName("data_A")
        self.verticalLayout.addWidget(self.data_A)
        self.btn_send_A = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_A.setObjectName("btn_send_A")
        self.verticalLayout.addWidget(self.btn_send_A)
        self.horizontalLayout.addLayout(self.verticalLayout)
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
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.ip_B = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_B.setObjectName("ip_B")
        self.verticalLayout_2.addWidget(self.ip_B)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.data_B = QtWidgets.QLineEdit(self.centralwidget)
        self.data_B.setObjectName("data_B")
        self.verticalLayout_2.addWidget(self.data_B)
        self.btn_send_B = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_B.setObjectName("btn_send_B")
        self.verticalLayout_2.addWidget(self.btn_send_B)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Base A"))
        self.label_3.setText(_translate("MainWindow", "IP Address"))
        self.ip_A.setText(_translate("MainWindow", "192.168.0.10"))
        self.label_5.setText(_translate("MainWindow", "Data"))
        self.data_A.setText(_translate("MainWindow", "Event"))
        self.btn_send_A.setText(_translate("MainWindow", "Send UDP"))
        self.label_2.setText(_translate("MainWindow", "Base B"))
        self.label_4.setText(_translate("MainWindow", "IP Address"))
        self.ip_B.setText(_translate("MainWindow", "192.168.0.11"))
        self.label_6.setText(_translate("MainWindow", "Data"))
        self.data_B.setText(_translate("MainWindow", "Event"))
        self.btn_send_B.setText(_translate("MainWindow", "Send UDP"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
