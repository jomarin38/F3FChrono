# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WWind.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WWind(object):
    def setupUi(self, WWind):
        WWind.setObjectName("WWind")
        WWind.resize(559, 25)
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
        self.voltage = QtWidgets.QLabel(WWind)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voltage.sizePolicy().hasHeightForWidth())
        self.voltage.setSizePolicy(sizePolicy)
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
        self.Elapsedtime = QtWidgets.QLabel(WWind)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Elapsedtime.setFont(font)
        self.Elapsedtime.setObjectName("Elapsedtime")
        self.gridLayout.addWidget(self.Elapsedtime, 0, 3, 1, 1)
        self.rssi = QtWidgets.QLabel(WWind)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rssi.sizePolicy().hasHeightForWidth())
        self.rssi.setSizePolicy(sizePolicy)
        self.rssi.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rssi.setFont(font)
        self.rssi.setAlignment(QtCore.Qt.AlignCenter)
        self.rssi.setObjectName("rssi")
        self.gridLayout.addWidget(self.rssi, 0, 1, 1, 1)

        self.retranslateUi(WWind)
        QtCore.QMetaObject.connectSlotsByName(WWind)

    def retranslateUi(self, WWind):
        _translate = QtCore.QCoreApplication.translate
        WWind.setWindowTitle(_translate("WWind", "Form"))
        self.WindInfo.setText(_translate("WWind", "Wind : 6.2m/s, 10°, No rain"))
        self.voltage.setText(_translate("WWind", "12.6 V"))
        self.btn_clear.setText(_translate("WWind", "X"))
        self.Elapsedtime.setText(_translate("WWind", "Elapsed time : "))
        self.rssi.setText(_translate("WWind", "rssi1, 2 : 90%, 95%"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WWind = QtWidgets.QWidget()
    ui = Ui_WWind()
    ui.setupUi(WWind)
    WWind.show()
    sys.exit(app.exec_())
