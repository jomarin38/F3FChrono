# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingsAdvanced.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingsAdvanced(object):
    def setupUi(self, WSettingsAdvanced):
        WSettingsAdvanced.setObjectName("WSettingsAdvanced")
        WSettingsAdvanced.resize(480, 271)
        self.gridLayout = QtWidgets.QGridLayout(WSettingsAdvanced)
        self.gridLayout.setContentsMargins(-1, 3, -1, 3)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(WSettingsAdvanced)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.port_buzzer = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.port_buzzer.setObjectName("port_buzzer")
        self.horizontalLayout_9.addWidget(self.port_buzzer)
        self.label_7 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.port_btn_next = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.port_btn_next.setObjectName("port_btn_next")
        self.horizontalLayout_7.addWidget(self.port_btn_next)
        self.label_5 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.buzzer_next_duration = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.buzzer_next_duration.setMaximum(65535)
        self.buzzer_next_duration.setObjectName("buzzer_next_duration")
        self.horizontalLayout_21.addWidget(self.buzzer_next_duration)
        self.label_19 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_21.addWidget(self.label_19)
        self.gridLayout_2.addLayout(self.horizontalLayout_21, 1, 1, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.port_ledB = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.port_ledB.setObjectName("port_ledB")
        self.horizontalLayout_12.addWidget(self.port_ledB)
        self.label_10 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_12.addWidget(self.label_10)
        self.gridLayout_2.addLayout(self.horizontalLayout_12, 2, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.port_btn_baseA = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.port_btn_baseA.setObjectName("port_btn_baseA")
        self.horizontalLayout_4.addWidget(self.port_btn_baseA)
        self.label_2 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 1, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.port_btn_baseB = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.port_btn_baseB.setObjectName("port_btn_baseB")
        self.horizontalLayout_6.addWidget(self.port_btn_baseB)
        self.label_4 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 4, 1, 1, 1)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.buzzer_duration = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.buzzer_duration.setMaximum(65535)
        self.buzzer_duration.setObjectName("buzzer_duration")
        self.horizontalLayout_20.addWidget(self.buzzer_duration)
        self.label_18 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_20.addWidget(self.label_18)
        self.gridLayout_2.addLayout(self.horizontalLayout_20, 0, 1, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.port_buzzer_next = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.port_buzzer_next.setObjectName("port_buzzer_next")
        self.horizontalLayout_8.addWidget(self.port_buzzer_next)
        self.label_6 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.port_ledA = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.port_ledA.setObjectName("port_ledA")
        self.horizontalLayout_11.addWidget(self.port_ledA)
        self.label_9 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_11.addWidget(self.label_9)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 2, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.udp_port = QtWidgets.QSpinBox(WSettingsAdvanced)
        self.udp_port.setMaximum(65535)
        self.udp_port.setObjectName("udp_port")
        self.horizontalLayout_10.addWidget(self.udp_port)
        self.label_8 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.voltagemin = QtWidgets.QDoubleSpinBox(WSettingsAdvanced)
        self.voltagemin.setDecimals(1)
        self.voltagemin.setSingleStep(0.1)
        self.voltagemin.setObjectName("voltagemin")
        self.horizontalLayout_5.addWidget(self.voltagemin)
        self.label_3 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.voltagecoef = QtWidgets.QDoubleSpinBox(WSettingsAdvanced)
        self.voltagecoef.setDecimals(3)
        self.voltagecoef.setSingleStep(0.1)
        self.voltagecoef.setObjectName("voltagecoef")
        self.horizontalLayout_13.addWidget(self.voltagecoef)
        self.label_11 = QtWidgets.QLabel(WSettingsAdvanced)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_13.addWidget(self.label_11)
        self.gridLayout_2.addLayout(self.horizontalLayout_13, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_back = QtWidgets.QPushButton(WSettingsAdvanced)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_back.setFont(font)
        self.btn_back.setObjectName("btn_back")
        self.horizontalLayout.addWidget(self.btn_back)
        self.btn_cancel = QtWidgets.QPushButton(WSettingsAdvanced)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.btn_valid = QtWidgets.QPushButton(WSettingsAdvanced)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_valid.setFont(font)
        self.btn_valid.setObjectName("btn_valid")
        self.horizontalLayout.addWidget(self.btn_valid)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(WSettingsAdvanced)
        QtCore.QMetaObject.connectSlotsByName(WSettingsAdvanced)
        WSettingsAdvanced.setTabOrder(self.port_buzzer, self.port_buzzer_next)
        WSettingsAdvanced.setTabOrder(self.port_buzzer_next, self.port_ledA)
        WSettingsAdvanced.setTabOrder(self.port_ledA, self.port_ledB)
        WSettingsAdvanced.setTabOrder(self.port_ledB, self.port_btn_next)
        WSettingsAdvanced.setTabOrder(self.port_btn_next, self.port_btn_baseA)
        WSettingsAdvanced.setTabOrder(self.port_btn_baseA, self.udp_port)

    def retranslateUi(self, WSettingsAdvanced):
        _translate = QtCore.QCoreApplication.translate
        WSettingsAdvanced.setWindowTitle(_translate("WSettingsAdvanced", "Form"))
        self.label.setText(_translate("WSettingsAdvanced", "Advanced Settings"))
        self.label_7.setText(_translate("WSettingsAdvanced", "Buzzer"))
        self.label_5.setText(_translate("WSettingsAdvanced", "Button Next"))
        self.label_19.setText(_translate("WSettingsAdvanced", "duration (ms)"))
        self.label_10.setText(_translate("WSettingsAdvanced", "Led B"))
        self.label_2.setText(_translate("WSettingsAdvanced", "Button Base A"))
        self.label_4.setText(_translate("WSettingsAdvanced", "Button Base B"))
        self.label_18.setText(_translate("WSettingsAdvanced", "duration (ms)"))
        self.label_6.setText(_translate("WSettingsAdvanced", "Buzzer Next"))
        self.label_9.setText(_translate("WSettingsAdvanced", "Led A"))
        self.label_8.setText(_translate("WSettingsAdvanced", "UDP Port"))
        self.label_3.setText(_translate("WSettingsAdvanced", "Min Voltage"))
        self.label_11.setText(_translate("WSettingsAdvanced", "ADC coef"))
        self.btn_back.setText(_translate("WSettingsAdvanced", "Back to Settings"))
        self.btn_cancel.setText(_translate("WSettingsAdvanced", "Cancel"))
        self.btn_valid.setText(_translate("WSettingsAdvanced", "Valid"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingsAdvanced = QtWidgets.QWidget()
    ui = Ui_WSettingsAdvanced()
    ui.setupUi(WSettingsAdvanced)
    WSettingsAdvanced.show()
    sys.exit(app.exec_())
