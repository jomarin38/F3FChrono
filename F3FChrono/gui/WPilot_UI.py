# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WPilot.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WPilot(object):
    def setupUi(self, WPilot):
        WPilot.setObjectName("WPilot")
        WPilot.resize(480, 35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WPilot.sizePolicy().hasHeightForWidth())
        WPilot.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WPilot)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pilotName = QtWidgets.QLabel(WPilot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pilotName.sizePolicy().hasHeightForWidth())
        self.pilotName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pilotName.setFont(font)
        self.pilotName.setAlignment(QtCore.Qt.AlignCenter)
        self.pilotName.setObjectName("pilotName")
        self.horizontalLayout.addWidget(self.pilotName)
        self.bib = QtWidgets.QLabel(WPilot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bib.sizePolicy().hasHeightForWidth())
        self.bib.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.bib.setFont(font)
        self.bib.setAlignment(QtCore.Qt.AlignCenter)
        self.bib.setObjectName("bib")
        self.horizontalLayout.addWidget(self.bib)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(WPilot)
        QtCore.QMetaObject.connectSlotsByName(WPilot)

    def retranslateUi(self, WPilot):
        _translate = QtCore.QCoreApplication.translate
        WPilot.setWindowTitle(_translate("WPilot", "Form"))
        self.pilotName.setText(_translate("WPilot", " _____ _______"))
        self.bib.setText(_translate("WPilot", " XXX"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WPilot = QtWidgets.QWidget()
    ui = Ui_WPilot()
    ui.setupUi(WPilot)
    WPilot.show()
    sys.exit(app.exec_())

