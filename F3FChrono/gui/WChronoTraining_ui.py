# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WChronoTraining.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WTraining(object):
    def setupUi(self, WTraining):
        WTraining.setObjectName("WTraining")
        WTraining.resize(352, 143)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WTraining.sizePolicy().hasHeightForWidth())
        WTraining.setSizePolicy(sizePolicy)
        WTraining.setInputMethodHints(QtCore.Qt.ImhNone)
        self.gridLayout = QtWidgets.QGridLayout(WTraining)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.Lap9 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap9.sizePolicy().hasHeightForWidth())
        self.Lap9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap9.setFont(font)
        self.Lap9.setObjectName("Lap9")
        self.gridLayout.addWidget(self.Lap9, 6, 1, 1, 1)
        self.runMin = QtWidgets.QLabel(WTraining)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.runMin.setFont(font)
        self.runMin.setObjectName("runMin")
        self.gridLayout.addWidget(self.runMin, 4, 0, 1, 1)
        self.Status = QtWidgets.QLabel(WTraining)
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
        self.gridLayout.addWidget(self.Status, 6, 0, 1, 1)
        self.runMean = QtWidgets.QLabel(WTraining)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.runMean.setFont(font)
        self.runMean.setObjectName("runMean")
        self.gridLayout.addWidget(self.runMean, 3, 0, 1, 1)
        self.Lap5 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap5.sizePolicy().hasHeightForWidth())
        self.Lap5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap5.setFont(font)
        self.Lap5.setObjectName("Lap5")
        self.gridLayout.addWidget(self.Lap5, 4, 1, 1, 1)
        self.Lap3 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap3.sizePolicy().hasHeightForWidth())
        self.Lap3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap3.setFont(font)
        self.Lap3.setObjectName("Lap3")
        self.gridLayout.addWidget(self.Lap3, 3, 1, 1, 1)
        self.Lap7 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap7.sizePolicy().hasHeightForWidth())
        self.Lap7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap7.setFont(font)
        self.Lap7.setObjectName("Lap7")
        self.gridLayout.addWidget(self.Lap7, 5, 1, 1, 1)
        self.lapNumber = QtWidgets.QLabel(WTraining)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lapNumber.setFont(font)
        self.lapNumber.setObjectName("lapNumber")
        self.gridLayout.addWidget(self.lapNumber, 0, 0, 1, 1)
        self.runMax = QtWidgets.QLabel(WTraining)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.runMax.setFont(font)
        self.runMax.setObjectName("runMax")
        self.gridLayout.addWidget(self.runMax, 5, 0, 1, 1)
        self.Lap1 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap1.sizePolicy().hasHeightForWidth())
        self.Lap1.setSizePolicy(sizePolicy)
        self.Lap1.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap1.setFont(font)
        self.Lap1.setObjectName("Lap1")
        self.gridLayout.addWidget(self.Lap1, 1, 1, 1, 1)
        self.Lap2 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap2.sizePolicy().hasHeightForWidth())
        self.Lap2.setSizePolicy(sizePolicy)
        self.Lap2.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap2.setFont(font)
        self.Lap2.setObjectName("Lap2")
        self.gridLayout.addWidget(self.Lap2, 1, 2, 1, 1)
        self.Lap4 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap4.sizePolicy().hasHeightForWidth())
        self.Lap4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap4.setFont(font)
        self.Lap4.setObjectName("Lap4")
        self.gridLayout.addWidget(self.Lap4, 3, 2, 1, 1)
        self.Lap6 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap6.sizePolicy().hasHeightForWidth())
        self.Lap6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap6.setFont(font)
        self.Lap6.setObjectName("Lap6")
        self.gridLayout.addWidget(self.Lap6, 4, 2, 1, 1)
        self.Lap8 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap8.sizePolicy().hasHeightForWidth())
        self.Lap8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap8.setFont(font)
        self.Lap8.setObjectName("Lap8")
        self.gridLayout.addWidget(self.Lap8, 5, 2, 1, 1)
        self.Lap10 = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Lap10.sizePolicy().hasHeightForWidth())
        self.Lap10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Lap10.setFont(font)
        self.Lap10.setObjectName("Lap10")
        self.gridLayout.addWidget(self.Lap10, 6, 2, 1, 1)
        self.LapTimeLabel = QtWidgets.QLabel(WTraining)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LapTimeLabel.sizePolicy().hasHeightForWidth())
        self.LapTimeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.LapTimeLabel.setFont(font)
        self.LapTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LapTimeLabel.setObjectName("LapTimeLabel")
        self.gridLayout.addWidget(self.LapTimeLabel, 0, 1, 1, 2)

        self.retranslateUi(WTraining)
        QtCore.QMetaObject.connectSlotsByName(WTraining)

    def retranslateUi(self, WTraining):
        _translate = QtCore.QCoreApplication.translate
        WTraining.setWindowTitle(_translate("WTraining", "Form"))
        self.Lap9.setText(_translate("WTraining", "9 : XX.XXX"))
        self.runMin.setText(_translate("WTraining", "Min : "))
        self.Status.setText(_translate("WTraining", "Wait New Run"))
        self.runMean.setText(_translate("WTraining", "Mean : "))
        self.Lap5.setText(_translate("WTraining", "5 : XX.XXX"))
        self.Lap3.setText(_translate("WTraining", "3 : XX.XXX"))
        self.Lap7.setText(_translate("WTraining", "7 : XX.XXX"))
        self.lapNumber.setText(_translate("WTraining", "Lap Number : 0"))
        self.runMax.setText(_translate("WTraining", "Max : "))
        self.Lap1.setText(_translate("WTraining", "1 : XX.XXX"))
        self.Lap2.setText(_translate("WTraining", "2 : XX.XXX"))
        self.Lap4.setText(_translate("WTraining", "4 : XX.XXX"))
        self.Lap6.setText(_translate("WTraining", "6 : XX.XXX"))
        self.Lap8.setText(_translate("WTraining", "8 : XX.XXX"))
        self.Lap10.setText(_translate("WTraining", "10 : XX.XXX"))
        self.LapTimeLabel.setText(_translate("WTraining", "Run(s) Time (s)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WTraining = QtWidgets.QWidget()
    ui = Ui_WTraining()
    ui.setupUi(WTraining)
    WTraining.show()
    sys.exit(app.exec_())
