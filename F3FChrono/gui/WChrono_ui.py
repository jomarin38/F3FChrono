# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WChrono.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WChrono(object):
    def setupUi(self, WChrono):
        WChrono.setObjectName("WChrono")
        WChrono.resize(341, 186)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WChrono.sizePolicy().hasHeightForWidth())
        WChrono.setSizePolicy(sizePolicy)
        WChrono.setInputMethodHints(QtCore.Qt.ImhNone)
        self.gridLayout = QtWidgets.QGridLayout(WChrono)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.penalty_100 = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.penalty_100.sizePolicy().hasHeightForWidth())
        self.penalty_100.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.penalty_100.setFont(font)
        self.penalty_100.setAlignment(QtCore.Qt.AlignCenter)
        self.penalty_100.setObjectName("penalty_100")
        self.gridLayout.addWidget(self.penalty_100, 0, 3, 1, 1)
        self.reflight = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reflight.sizePolicy().hasHeightForWidth())
        self.reflight.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.reflight.setFont(font)
        self.reflight.setAlignment(QtCore.Qt.AlignCenter)
        self.reflight.setObjectName("reflight")
        self.gridLayout.addWidget(self.reflight, 3, 4, 2, 1)
        self.penalty_value = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.penalty_value.sizePolicy().hasHeightForWidth())
        self.penalty_value.setSizePolicy(sizePolicy)
        self.penalty_value.setMinimumSize(QtCore.QSize(0, 0))
        self.penalty_value.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.penalty_value.setFont(font)
        self.penalty_value.setAlignment(QtCore.Qt.AlignCenter)
        self.penalty_value.setObjectName("penalty_value")
        self.gridLayout.addWidget(self.penalty_value, 2, 1, 1, 1)
        self.btn_clear_penalty = QtWidgets.QPushButton(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_clear_penalty.sizePolicy().hasHeightForWidth())
        self.btn_clear_penalty.setSizePolicy(sizePolicy)
        self.btn_clear_penalty.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_clear_penalty.setFont(font)
        self.btn_clear_penalty.setObjectName("btn_clear_penalty")
        self.gridLayout.addWidget(self.btn_clear_penalty, 1, 3, 2, 2)
        self.nullFlight = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nullFlight.sizePolicy().hasHeightForWidth())
        self.nullFlight.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.nullFlight.setFont(font)
        self.nullFlight.setAlignment(QtCore.Qt.AlignCenter)
        self.nullFlight.setObjectName("nullFlight")
        self.gridLayout.addWidget(self.nullFlight, 3, 3, 2, 1)
        self.label = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.penalty_1000 = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.penalty_1000.sizePolicy().hasHeightForWidth())
        self.penalty_1000.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.penalty_1000.setFont(font)
        self.penalty_1000.setAlignment(QtCore.Qt.AlignCenter)
        self.penalty_1000.setObjectName("penalty_1000")
        self.gridLayout.addWidget(self.penalty_1000, 0, 4, 1, 1)
        self.nullFlightLabel = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nullFlightLabel.sizePolicy().hasHeightForWidth())
        self.nullFlightLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.nullFlightLabel.setFont(font)
        self.nullFlightLabel.setText("")
        self.nullFlightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nullFlightLabel.setObjectName("nullFlightLabel")
        self.gridLayout.addWidget(self.nullFlightLabel, 2, 2, 1, 1)
        self.Status = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Status.sizePolicy().hasHeightForWidth())
        self.Status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.Status.setFont(font)
        self.Status.setScaledContents(False)
        self.Status.setAlignment(QtCore.Qt.AlignCenter)
        self.Status.setWordWrap(False)
        self.Status.setObjectName("Status")
        self.gridLayout.addWidget(self.Status, 1, 0, 1, 3)
        self.Time_label = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Time_label.sizePolicy().hasHeightForWidth())
        self.Time_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(46)
        font.setBold(True)
        font.setWeight(75)
        self.Time_label.setFont(font)
        self.Time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Time_label.setObjectName("Time_label")
        self.gridLayout.addWidget(self.Time_label, 0, 0, 1, 3)
        self.WindInfo = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WindInfo.sizePolicy().hasHeightForWidth())
        self.WindInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.WindInfo.setFont(font)
        self.WindInfo.setText("")
        self.WindInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.WindInfo.setObjectName("WindInfo")
        self.gridLayout.addWidget(self.WindInfo, 4, 0, 1, 3)

        self.retranslateUi(WChrono)
        QtCore.QMetaObject.connectSlotsByName(WChrono)

    def retranslateUi(self, WChrono):
        _translate = QtCore.QCoreApplication.translate
        WChrono.setWindowTitle(_translate("WChrono", "Form"))
        self.penalty_100.setText(_translate("WChrono", "100"))
        self.reflight.setText(_translate("WChrono", "Reflight"))
        self.penalty_value.setText(_translate("WChrono", "0"))
        self.btn_clear_penalty.setText(_translate("WChrono", "Clear Penalty"))
        self.nullFlight.setText(_translate("WChrono", "0 Flight"))
        self.label.setText(_translate("WChrono", "Penalty :"))
        self.penalty_1000.setText(_translate("WChrono", "1000"))
        self.Status.setText(_translate("WChrono", "Wait New Run"))
        self.Time_label.setText(_translate("WChrono", "30.00"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChrono = QtWidgets.QWidget()
    ui = Ui_WChrono()
    ui.setupUi(WChrono)
    WChrono.show()
    sys.exit(app.exec_())
