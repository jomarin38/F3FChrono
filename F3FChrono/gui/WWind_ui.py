# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WWind.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WWind(object):
    def setupUi(self, WWind):
        WWind.setObjectName("WWind")
        WWind.resize(389, 26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WWind.sizePolicy().hasHeightForWidth())
        WWind.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WWind)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.WindInfo = QtWidgets.QLabel(WWind)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WindInfo.sizePolicy().hasHeightForWidth())
        self.WindInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.WindInfo.setFont(font)
        self.WindInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.WindInfo.setObjectName("WindInfo")
        self.gridLayout.addWidget(self.WindInfo, 0, 2, 1, 1)
        self.Elapsedtime = QtWidgets.QLabel(WWind)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Elapsedtime.setFont(font)
        self.Elapsedtime.setObjectName("Elapsedtime")
        self.gridLayout.addWidget(self.Elapsedtime, 0, 3, 1, 1)
        self.voltage = QtWidgets.QLabel(WWind)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voltage.sizePolicy().hasHeightForWidth())
        self.voltage.setSizePolicy(sizePolicy)
        self.voltage.setMinimumSize(QtCore.QSize(75, 0))
        self.voltage.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.voltage.setFont(font)
        self.voltage.setAlignment(QtCore.Qt.AlignCenter)
        self.voltage.setObjectName("voltage")
        self.gridLayout.addWidget(self.voltage, 0, 0, 1, 1)
        self.btn_clear = QtWidgets.QPushButton(WWind)
        self.btn_clear.setMaximumSize(QtCore.QSize(19, 16777215))
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 0, 4, 1, 1)
        self.lastRun = QtWidgets.QLabel(WWind)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastRun.sizePolicy().hasHeightForWidth())
        self.lastRun.setSizePolicy(sizePolicy)
        self.lastRun.setMinimumSize(QtCore.QSize(65, 0))
        self.lastRun.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lastRun.setFont(font)
        self.lastRun.setAlignment(QtCore.Qt.AlignCenter)
        self.lastRun.setObjectName("lastRun")
        self.gridLayout.addWidget(self.lastRun, 0, 1, 1, 1)

        self.retranslateUi(WWind)
        QtCore.QMetaObject.connectSlotsByName(WWind)

    def retranslateUi(self, WWind):
        _translate = QtCore.QCoreApplication.translate
        WWind.setWindowTitle(_translate("WWind", "Form"))
        self.WindInfo.setText(_translate("WWind", "Wind : 6.2m/s, 10°, No rain"))
        self.Elapsedtime.setText(_translate("WWind", "Elapsed time : "))
        self.voltage.setText(_translate("WWind", "12.6V, 12,6V"))
        self.btn_clear.setText(_translate("WWind", "X"))
        self.lastRun.setText(_translate("WWind", "--"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WWind = QtWidgets.QWidget()
    ui = Ui_WWind()
    ui.setupUi(WWind)
    WWind.show()
    sys.exit(app.exec_())
