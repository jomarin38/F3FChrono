# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WPilot.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WPilot(object):
    def setupUi(self, WPilot):
        WPilot.setObjectName("WPilot")
        WPilot.resize(429, 52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WPilot.sizePolicy().hasHeightForWidth())
        WPilot.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WPilot)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.round = QtWidgets.QLabel(WPilot)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.round.setFont(font)
        self.round.setAlignment(QtCore.Qt.AlignCenter)
        self.round.setObjectName("round")
        self.gridLayout.addWidget(self.round, 0, 1, 1, 1)
        self.Btn_CancelRound = QtWidgets.QPushButton(WPilot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_CancelRound.sizePolicy().hasHeightForWidth())
        self.Btn_CancelRound.setSizePolicy(sizePolicy)
        self.Btn_CancelRound.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Btn_CancelRound.setFont(font)
        self.Btn_CancelRound.setObjectName("Btn_CancelRound")
        self.gridLayout.addWidget(self.Btn_CancelRound, 0, 2, 1, 1)
        self.bib = QtWidgets.QLabel(WPilot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bib.sizePolicy().hasHeightForWidth())
        self.bib.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bib.setFont(font)
        self.bib.setAlignment(QtCore.Qt.AlignCenter)
        self.bib.setObjectName("bib")
        self.gridLayout.addWidget(self.bib, 1, 2, 1, 1)
        self.Btn_Alarm = QtWidgets.QPushButton(WPilot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Alarm.sizePolicy().hasHeightForWidth())
        self.Btn_Alarm.setSizePolicy(sizePolicy)
        self.Btn_Alarm.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Btn_Alarm.setFont(font)
        self.Btn_Alarm.setObjectName("Btn_Alarm")
        self.gridLayout.addWidget(self.Btn_Alarm, 0, 0, 1, 1)
        self.pilotName = QtWidgets.QLabel(WPilot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pilotName.sizePolicy().hasHeightForWidth())
        self.pilotName.setSizePolicy(sizePolicy)
        self.pilotName.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pilotName.setFont(font)
        self.pilotName.setAlignment(QtCore.Qt.AlignCenter)
        self.pilotName.setObjectName("pilotName")
        self.gridLayout.addWidget(self.pilotName, 1, 0, 1, 2)

        self.retranslateUi(WPilot)
        QtCore.QMetaObject.connectSlotsByName(WPilot)

    def retranslateUi(self, WPilot):
        _translate = QtCore.QCoreApplication.translate
        WPilot.setWindowTitle(_translate("WPilot", "Form"))
        self.round.setText(_translate("WPilot", "Round : "))
        self.Btn_CancelRound.setText(_translate("WPilot", "Cancel Round"))
        self.bib.setText(_translate("WPilot", "bib : XXX"))
        self.Btn_Alarm.setText(_translate("WPilot", "Disable Alarm"))
        self.pilotName.setText(_translate("WPilot", " _____ _______"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WPilot = QtWidgets.QWidget()
    ui = Ui_WPilot()
    ui.setupUi(WPilot)
    WPilot.show()
    sys.exit(app.exec_())
