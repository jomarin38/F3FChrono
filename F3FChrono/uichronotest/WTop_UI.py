# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WTop.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WTop(object):
    def setupUi(self, WTop):
        WTop.setObjectName("WTop")
        WTop.resize(462, 125)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WTop.sizePolicy().hasHeightForWidth())
        WTop.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WTop)
        self.gridLayout.setObjectName("gridLayout")
        self.RaceInfo = QtWidgets.QLabel(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RaceInfo.sizePolicy().hasHeightForWidth())
        self.RaceInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.RaceInfo.setFont(font)
        self.RaceInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.RaceInfo.setObjectName("RaceInfo")
        self.gridLayout.addWidget(self.RaceInfo, 1, 1, 1, 1)
        self.PilotName = QtWidgets.QLabel(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PilotName.sizePolicy().hasHeightForWidth())
        self.PilotName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.PilotName.setFont(font)
        self.PilotName.setAlignment(QtCore.Qt.AlignCenter)
        self.PilotName.setObjectName("PilotName")
        self.gridLayout.addWidget(self.PilotName, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 2)
        self.line = QtWidgets.QFrame(WTop)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 0, 1, 2)

        self.retranslateUi(WTop)
        QtCore.QMetaObject.connectSlotsByName(WTop)

    def retranslateUi(self, WTop):
        _translate = QtCore.QCoreApplication.translate
        WTop.setWindowTitle(_translate("WTop", "Form"))
        self.RaceInfo.setText(_translate("WTop", "Run : XXX"))
        self.PilotName.setText(_translate("WTop", "Pilot Name : _____ _______"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WTop = QtWidgets.QWidget()
    ui = Ui_WTop()
    ui.setupUi(WTop)
    WTop.show()
    sys.exit(app.exec_())

