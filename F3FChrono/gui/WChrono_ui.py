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
        WChrono.resize(480, 153)
        WChrono.setInputMethodHints(QtCore.Qt.ImhNone)
        self.formLayout = QtWidgets.QFormLayout(WChrono)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Time_label = QtWidgets.QLabel(WChrono)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.Status = QtWidgets.QComboBox(WChrono)
        self.Status.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Status.sizePolicy().hasHeightForWidth())
        self.Status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Status.setFont(font)
        self.Status.setAutoFillBackground(False)
        self.Status.setInputMethodHints(QtCore.Qt.ImhNone)
        self.Status.setEditable(False)
        self.Status.setFrame(True)
        self.Status.setObjectName("Status")
        self.Status.addItem("")
        self.Status.addItem("")
        self.Status.addItem("")
        self.Status.addItem("")
        self.Status.addItem("")
        self.Status.addItem("")
        self.verticalLayout.addWidget(self.Status)
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
        self.label_2 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.penalty_100 = QtWidgets.QPushButton(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.penalty_100.setFont(font)
        self.penalty_100.setObjectName("penalty_100")
        self.gridLayout.addWidget(self.penalty_100, 1, 2, 1, 1)
        self.penalty_1000 = QtWidgets.QPushButton(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.penalty_1000.setFont(font)
        self.penalty_1000.setObjectName("penalty_1000")
        self.gridLayout.addWidget(self.penalty_1000, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 2, 1, 1)
        self.nullFlight = QtWidgets.QPushButton(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.nullFlight.setFont(font)
        self.nullFlight.setObjectName("nullFlight")
        self.gridLayout.addWidget(self.nullFlight, 4, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(WChrono)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 2, 1, 1)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.gridLayout)

        self.retranslateUi(WChrono)
        QtCore.QMetaObject.connectSlotsByName(WChrono)

    def retranslateUi(self, WChrono):
        _translate = QtCore.QCoreApplication.translate
        WChrono.setWindowTitle(_translate("WChrono", "Form"))
        self.Time_label.setText(_translate("WChrono", "30.00"))
        self.Status.setItemText(0, _translate("WChrono", "Wait New Run"))
        self.Status.setItemText(1, _translate("WChrono", "Wait to launch"))
        self.Status.setItemText(2, _translate("WChrono", "Launched"))
        self.Status.setItemText(3, _translate("WChrono", "In start"))
        self.Status.setItemText(4, _translate("WChrono", "In progress"))
        self.Status.setItemText(5, _translate("WChrono", "Finished"))
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
        self.label_2.setText(_translate("WChrono", "Penalty"))
        self.penalty_100.setText(_translate("WChrono", "100"))
        self.penalty_1000.setText(_translate("WChrono", "1000"))
        self.label.setText(_translate("WChrono", "0"))
        self.nullFlight.setText(_translate("WChrono", "0 Flight"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChrono = QtWidgets.QWidget()
    ui = Ui_WChrono()
    ui.setupUi(WChrono)
    WChrono.show()
    sys.exit(app.exec_())
