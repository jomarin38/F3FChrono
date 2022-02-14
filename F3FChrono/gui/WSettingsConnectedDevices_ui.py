# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingsConnectedDevices.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingsConnectedDevices(object):
    def setupUi(self, WSettingsConnectedDevices):
        WSettingsConnectedDevices.setObjectName("WSettingsConnectedDevices")
        WSettingsConnectedDevices.resize(434, 282)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WSettingsConnectedDevices.sizePolicy().hasHeightForWidth())
        WSettingsConnectedDevices.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WSettingsConnectedDevices)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.AnemometerComboBox = QtWidgets.QComboBox(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.AnemometerComboBox.setFont(font)
        self.AnemometerComboBox.setObjectName("AnemometerComboBox")
        self.AnemometerComboBox.addItem("")
        self.AnemometerComboBox.addItem("")
        self.AnemometerComboBox.addItem("")
        self.gridLayout.addWidget(self.AnemometerComboBox, 2, 0, 1, 1)
        self.btn_AnemometerConnect = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_AnemometerConnect.setFont(font)
        self.btn_AnemometerConnect.setObjectName("btn_AnemometerConnect")
        self.gridLayout.addWidget(self.btn_AnemometerConnect, 1, 1, 1, 1)
        self.webserver = QtWidgets.QCheckBox(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.webserver.setFont(font)
        self.webserver.setObjectName("webserver")
        self.gridLayout.addWidget(self.webserver, 10, 0, 1, 1)
        self.btn_base_settings = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_base_settings.setFont(font)
        self.btn_base_settings.setObjectName("btn_base_settings")
        self.gridLayout.addWidget(self.btn_base_settings, 13, 0, 1, 1)
        self.btn_valid = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_valid.setFont(font)
        self.btn_valid.setObjectName("btn_valid")
        self.gridLayout.addWidget(self.btn_valid, 15, 1, 1, 1)
        self.btn_cancel = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayout.addWidget(self.btn_cancel, 15, 0, 1, 1)
        self.label = QtWidgets.QLabel(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.wbtn_settings = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.wbtn_settings.setFont(font)
        self.wbtn_settings.setObjectName("wbtn_settings")
        self.gridLayout.addWidget(self.wbtn_settings, 13, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(WSettingsConnectedDevices)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 11, 0, 1, 2)
        self.btn_back = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setObjectName("btn_back")
        self.gridLayout.addWidget(self.btn_back, 14, 0, 1, 2)
        self.AnemometerStatus = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.AnemometerStatus.setFont(font)
        self.AnemometerStatus.setInputMethodHints(QtCore.Qt.ImhNone)
        self.AnemometerStatus.setCheckable(False)
        self.AnemometerStatus.setObjectName("AnemometerStatus")
        self.gridLayout.addWidget(self.AnemometerStatus, 2, 1, 1, 1)
        self.btn_AnemometerGetList = QtWidgets.QPushButton(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_AnemometerGetList.setFont(font)
        self.btn_AnemometerGetList.setObjectName("btn_AnemometerGetList")
        self.gridLayout.addWidget(self.btn_AnemometerGetList, 1, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(WSettingsConnectedDevices)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 9, 0, 1, 2)
        self.WeatherStation_Speed = QtWidgets.QLabel(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.WeatherStation_Speed.setFont(font)
        self.WeatherStation_Speed.setObjectName("WeatherStation_Speed")
        self.gridLayout.addWidget(self.WeatherStation_Speed, 8, 0, 1, 1)
        self.line = QtWidgets.QFrame(WSettingsConnectedDevices)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 7, 0, 1, 2)
        self.WeatherStation_Dir = QtWidgets.QLabel(WSettingsConnectedDevices)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.WeatherStation_Dir.setFont(font)
        self.WeatherStation_Dir.setObjectName("WeatherStation_Dir")
        self.gridLayout.addWidget(self.WeatherStation_Dir, 8, 1, 1, 1)

        self.retranslateUi(WSettingsConnectedDevices)
        QtCore.QMetaObject.connectSlotsByName(WSettingsConnectedDevices)

    def retranslateUi(self, WSettingsConnectedDevices):
        _translate = QtCore.QCoreApplication.translate
        WSettingsConnectedDevices.setWindowTitle(_translate("WSettingsConnectedDevices", "Form"))
        self.AnemometerComboBox.setItemText(0, _translate("WSettingsConnectedDevices", "SDA"))
        self.AnemometerComboBox.setItemText(1, _translate("WSettingsConnectedDevices", "PRO"))
        self.AnemometerComboBox.setItemText(2, _translate("WSettingsConnectedDevices", "JMA"))
        self.btn_AnemometerConnect.setText(_translate("WSettingsConnectedDevices", "Connect"))
        self.webserver.setText(_translate("WSettingsConnectedDevices", "F3F Display"))
        self.btn_base_settings.setText(_translate("WSettingsConnectedDevices", "Base Settings"))
        self.btn_valid.setText(_translate("WSettingsConnectedDevices", "Valid"))
        self.btn_cancel.setText(_translate("WSettingsConnectedDevices", "Cancel"))
        self.label.setText(_translate("WSettingsConnectedDevices", "Connected Devices Settings"))
        self.wbtn_settings.setText(_translate("WSettingsConnectedDevices", "WBtn Settings"))
        self.btn_back.setText(_translate("WSettingsConnectedDevices", "Back to Settings"))
        self.AnemometerStatus.setText(_translate("WSettingsConnectedDevices", "Not connected"))
        self.btn_AnemometerGetList.setText(_translate("WSettingsConnectedDevices", "Get Anemometer List"))
        self.WeatherStation_Speed.setText(_translate("WSettingsConnectedDevices", "Wind Speed : -1 m/s"))
        self.WeatherStation_Dir.setText(_translate("WSettingsConnectedDevices", "Dir : Nan, 5V"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingsConnectedDevices = QtWidgets.QWidget()
    ui = Ui_WSettingsConnectedDevices()
    ui.setupUi(WSettingsConnectedDevices)
    WSettingsConnectedDevices.show()
    sys.exit(app.exec_())
