# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WChrono.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WChrono(object):
    def setupUi(self, WChrono):
        WChrono.setObjectName("WChrono")
        WChrono.resize(480, 153)
        self.formLayout = QtWidgets.QFormLayout(WChrono)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Time_label = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
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
        self.comboBox = QtWidgets.QComboBox(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.Lap3 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap3.setFont(font)
        self.Lap3.setObjectName("Lap3")
        self.gridLayout.addWidget(self.Lap3, 2, 0, 1, 1)
        self.Lap4 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap4.setFont(font)
        self.Lap4.setObjectName("Lap4")
        self.gridLayout.addWidget(self.Lap4, 2, 1, 1, 1)
        self.Lap1 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap1.setFont(font)
        self.Lap1.setObjectName("Lap1")
        self.gridLayout.addWidget(self.Lap1, 1, 0, 1, 1)
        self.Lap2 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap2.setFont(font)
        self.Lap2.setObjectName("Lap2")
        self.gridLayout.addWidget(self.Lap2, 1, 1, 1, 1)
        self.Lap7 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap7.setFont(font)
        self.Lap7.setObjectName("Lap7")
        self.gridLayout.addWidget(self.Lap7, 4, 0, 1, 1)
        self.Lap10 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap10.setFont(font)
        self.Lap10.setObjectName("Lap10")
        self.gridLayout.addWidget(self.Lap10, 5, 1, 1, 1)
        self.Lap9 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap9.setFont(font)
        self.Lap9.setObjectName("Lap9")
        self.gridLayout.addWidget(self.Lap9, 5, 0, 1, 1)
        self.Lap6 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap6.setFont(font)
        self.Lap6.setObjectName("Lap6")
        self.gridLayout.addWidget(self.Lap6, 3, 1, 1, 1)
        self.Lap8 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap8.setFont(font)
        self.Lap8.setObjectName("Lap8")
        self.gridLayout.addWidget(self.Lap8, 4, 1, 1, 1)
        self.Lap5 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Lap5.setFont(font)
        self.Lap5.setObjectName("Lap5")
        self.gridLayout.addWidget(self.Lap5, 3, 0, 1, 1)
        self.LapTimeLabel = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.LapTimeLabel.setFont(font)
        self.LapTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LapTimeLabel.setObjectName("LapTimeLabel")
        self.gridLayout.addWidget(self.LapTimeLabel, 0, 0, 1, 2)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.gridLayout)

        self.retranslateUi(WChrono)
        QtCore.QMetaObject.connectSlotsByName(WChrono)

    def retranslateUi(self, WChrono):
        _translate = QtCore.QCoreApplication.translate
        WChrono.setWindowTitle(_translate("WChrono", "Form"))
        self.Time_label.setText(_translate("WChrono", "30.000"))
        self.comboBox.setItemText(0, _translate("WChrono", "Wait to launch"))
        self.comboBox.setItemText(1, _translate("WChrono", "Launch"))
        self.comboBox.setItemText(2, _translate("WChrono", "In start"))
        self.comboBox.setItemText(3, _translate("WChrono", "Started"))
        self.comboBox.setItemText(4, _translate("WChrono", "In progress"))
        self.comboBox.setItemText(5, _translate("WChrono", "Finish"))
        self.Lap3.setText(_translate("WChrono", "3 : XX.XXX"))
        self.Lap4.setText(_translate("WChrono", "4 : XX.XXX"))
        self.Lap1.setText(_translate("WChrono", "1 : XX.XXX"))
        self.Lap2.setText(_translate("WChrono", "2 : XX.XXX"))
        self.Lap7.setText(_translate("WChrono", "7 : XX.XXX"))
        self.Lap10.setText(_translate("WChrono", "10 : XX.XXX"))
        self.Lap9.setText(_translate("WChrono", "9 : XX.XXX"))
        self.Lap6.setText(_translate("WChrono", "6 : XX.XXX"))
        self.Lap8.setText(_translate("WChrono", "8 : XX.XXX"))
        self.Lap5.setText(_translate("WChrono", "5 : XX.XXX"))
        self.LapTimeLabel.setText(_translate("WChrono", "Lap Time (s)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChrono = QtWidgets.QWidget()
    ui = Ui_WChrono()
    ui.setupUi(WChrono)
    WChrono.show()
    sys.exit(app.exec_())

