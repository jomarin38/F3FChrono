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
        WTop.resize(684, 176)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WTop.sizePolicy().hasHeightForWidth())
        WTop.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(WTop)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line = QtWidgets.QFrame(WTop)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pilotNameLabel = QtWidgets.QLabel(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pilotNameLabel.sizePolicy().hasHeightForWidth())
        self.pilotNameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pilotNameLabel.setFont(font)
        self.pilotNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pilotNameLabel.setObjectName("pilotNameLabel")
        self.horizontalLayout.addWidget(self.pilotNameLabel)
        self.pilotName = QtWidgets.QLabel(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pilotName.sizePolicy().hasHeightForWidth())
        self.pilotName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pilotName.setFont(font)
        self.pilotName.setAlignment(QtCore.Qt.AlignCenter)
        self.pilotName.setObjectName("pilotName")
        self.horizontalLayout.addWidget(self.pilotName)
        self.bibLabel = QtWidgets.QLabel(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bibLabel.sizePolicy().hasHeightForWidth())
        self.bibLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.bibLabel.setFont(font)
        self.bibLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bibLabel.setObjectName("bibLabel")
        self.horizontalLayout.addWidget(self.bibLabel)
        self.bib = QtWidgets.QLabel(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bib.sizePolicy().hasHeightForWidth())
        self.bib.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.bib.setFont(font)
        self.bib.setAlignment(QtCore.Qt.AlignCenter)
        self.bib.setObjectName("bib")
        self.horizontalLayout.addWidget(self.bib)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(WTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)

        self.retranslateUi(WTop)
        QtCore.QMetaObject.connectSlotsByName(WTop)

    def retranslateUi(self, WTop):
        _translate = QtCore.QCoreApplication.translate
        WTop.setWindowTitle(_translate("WTop", "Form"))
        self.pilotNameLabel.setText(_translate("WTop", "Pilot Name :"))
        self.pilotName.setText(_translate("WTop", " _____ _______"))
        self.bibLabel.setText(_translate("WTop", "BIB : "))
        self.bib.setText(_translate("WTop", " XXX"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WTop = QtWidgets.QWidget()
    ui = Ui_WTop()
    ui.setupUi(WTop)
    WTop.show()
    sys.exit(app.exec_())

