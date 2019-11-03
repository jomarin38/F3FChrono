# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WBottom.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WBottom(object):
    def setupUi(self, WBottom):
        WBottom.setObjectName("WBottom")
        WBottom.resize(464, 125)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WBottom.sizePolicy().hasHeightForWidth())
        WBottom.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WBottom)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(WBottom)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        self.WindInfo = QtWidgets.QLabel(WBottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WindInfo.sizePolicy().hasHeightForWidth())
        self.WindInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.WindInfo.setFont(font)
        self.WindInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.WindInfo.setObjectName("WindInfo")
        self.gridLayout.addWidget(self.WindInfo, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(WBottom)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.RaceInfo = QtWidgets.QLabel(WBottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RaceInfo.sizePolicy().hasHeightForWidth())
        self.RaceInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.RaceInfo.setFont(font)
        self.RaceInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.RaceInfo.setObjectName("RaceInfo")
        self.gridLayout.addWidget(self.RaceInfo, 3, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(WBottom)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 4, 0, 1, 1)

        self.retranslateUi(WBottom)
        QtCore.QMetaObject.connectSlotsByName(WBottom)

    def retranslateUi(self, WBottom):
        _translate = QtCore.QCoreApplication.translate
        WBottom.setWindowTitle(_translate("WBottom", "Form"))
        self.WindInfo.setText(_translate("WBottom", "Wind : 6.2m/S, NNE"))
        self.RaceInfo.setText(_translate("WBottom", "Race In progress, Run : XX"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WBottom = QtWidgets.QWidget()
    ui = Ui_WBottom()
    ui.setupUi(WBottom)
    WBottom.show()
    sys.exit(app.exec_())

