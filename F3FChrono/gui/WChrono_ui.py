# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WChrono.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WChrono(object):
    def setupUi(self, WChrono):
        WChrono.setObjectName("WChrono")
        WChrono.resize(428, 179)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WChrono.sizePolicy().hasHeightForWidth())
        WChrono.setSizePolicy(sizePolicy)
        WChrono.setInputMethodHints(QtCore.Qt.ImhNone)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(WChrono)
        self.horizontalLayout_3.setContentsMargins(3, 1, 3, 1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Time_label = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Time_label.sizePolicy().hasHeightForWidth())
        self.Time_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.Time_label.setFont(font)
        self.Time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Time_label.setObjectName("Time_label")
        self.verticalLayout.addWidget(self.Time_label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
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
        self.horizontalLayout_4.addWidget(self.penalty_value)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.Status = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Status.sizePolicy().hasHeightForWidth())
        self.Status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Status.setFont(font)
        self.Status.setScaledContents(False)
        self.Status.setAlignment(QtCore.Qt.AlignCenter)
        self.Status.setWordWrap(False)
        self.Status.setObjectName("Status")
        self.verticalLayout.addWidget(self.Status)
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
        self.verticalLayout.addWidget(self.nullFlightLabel)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_penalty_100 = QtWidgets.QPushButton(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_penalty_100.sizePolicy().hasHeightForWidth())
        self.btn_penalty_100.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_penalty_100.setFont(font)
        self.btn_penalty_100.setObjectName("btn_penalty_100")
        self.horizontalLayout.addWidget(self.btn_penalty_100)
        self.line_5 = QtWidgets.QFrame(WChrono)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout.addWidget(self.line_5)
        self.btn_penalty_1000 = QtWidgets.QPushButton(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_penalty_1000.sizePolicy().hasHeightForWidth())
        self.btn_penalty_1000.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_penalty_1000.setFont(font)
        self.btn_penalty_1000.setObjectName("btn_penalty_1000")
        self.horizontalLayout.addWidget(self.btn_penalty_1000)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(WChrono)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
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
        self.verticalLayout_2.addWidget(self.btn_clear_penalty)
        self.line_3 = QtWidgets.QFrame(WChrono)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.line_2 = QtWidgets.QFrame(WChrono)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_6.addWidget(self.line_2)
        self.nullFlight = QtWidgets.QPushButton(WChrono)
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
        self.nullFlight.setObjectName("nullFlight")
        self.horizontalLayout_6.addWidget(self.nullFlight)
        self.line_4 = QtWidgets.QFrame(WChrono)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_6.addWidget(self.line_4)
        self.Btn_reflight = QtWidgets.QPushButton(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_reflight.sizePolicy().hasHeightForWidth())
        self.Btn_reflight.setSizePolicy(sizePolicy)
        self.Btn_reflight.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Btn_reflight.setFont(font)
        self.Btn_reflight.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_reflight.setFlat(False)
        self.Btn_reflight.setObjectName("Btn_reflight")
        self.horizontalLayout_6.addWidget(self.Btn_reflight)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(WChrono)
        QtCore.QMetaObject.connectSlotsByName(WChrono)

    def retranslateUi(self, WChrono):
        _translate = QtCore.QCoreApplication.translate
        WChrono.setWindowTitle(_translate("WChrono", "Form"))
        self.Time_label.setText(_translate("WChrono", "30.00"))
        self.label.setText(_translate("WChrono", "Penalty :"))
        self.penalty_value.setText(_translate("WChrono", "0"))
        self.Status.setText(_translate("WChrono", "Wait New Run"))
        self.btn_penalty_100.setText(_translate("WChrono", "100"))
        self.btn_penalty_1000.setText(_translate("WChrono", "1000"))
        self.btn_clear_penalty.setText(_translate("WChrono", "Clear Penalty"))
        self.nullFlight.setText(_translate("WChrono", "0 Flight"))
        self.Btn_reflight.setText(_translate("WChrono", "Reflight"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChrono = QtWidgets.QWidget()
    ui = Ui_WChrono()
    ui.setupUi(WChrono)
    WChrono.show()
    sys.exit(app.exec_())
