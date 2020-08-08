# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WPilot.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WPilot(object):
    def setupUi(self, WPilot):
        WPilot.setObjectName("WPilot")
        WPilot.resize(429, 34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WPilot.sizePolicy().hasHeightForWidth())
        WPilot.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WPilot)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
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
        self.horizontalLayout.addWidget(self.pilotName)
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
        self.horizontalLayout.addWidget(self.bib)
        self.round = QtWidgets.QLabel(WPilot)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.round.setFont(font)
        self.round.setObjectName("round")
        self.horizontalLayout.addWidget(self.round)
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
        self.horizontalLayout.addWidget(self.Btn_CancelRound)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(WPilot)
        QtCore.QMetaObject.connectSlotsByName(WPilot)

    def retranslateUi(self, WPilot):
        _translate = QtCore.QCoreApplication.translate
        WPilot.setWindowTitle(_translate("WPilot", "Form"))
        self.pilotName.setText(_translate("WPilot", " _____ _______"))
        self.bib.setText(_translate("WPilot", "bib : XXX"))
        self.round.setText(_translate("WPilot", "Round : "))
        self.Btn_CancelRound.setText(_translate("WPilot", "Cancel Round"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WPilot = QtWidgets.QWidget()
    ui = Ui_WPilot()
    ui.setupUi(WPilot)
    WPilot.show()
    sys.exit(app.exec_())
