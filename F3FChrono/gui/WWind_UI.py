# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WWind.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WWind(object):
    def setupUi(self, WWind):
        WWind.setObjectName("WWind")
        WWind.resize(480, 43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WWind.sizePolicy().hasHeightForWidth())
        WWind.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WWind)
        self.gridLayout.setObjectName("gridLayout")
        self.Elapsedtime = QtWidgets.QLabel(WWind)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Elapsedtime.setFont(font)
        self.Elapsedtime.setObjectName("Elapsedtime")
        self.gridLayout.addWidget(self.Elapsedtime, 0, 1, 1, 1)
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
        self.gridLayout.addWidget(self.WindInfo, 0, 0, 1, 1)
        self.btn_clear = QtWidgets.QPushButton(WWind)
        self.btn_clear.setMaximumSize(QtCore.QSize(19, 16777215))
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 0, 2, 1, 1)

        self.retranslateUi(WWind)
        QtCore.QMetaObject.connectSlotsByName(WWind)

    def retranslateUi(self, WWind):
        _translate = QtCore.QCoreApplication.translate
        WWind.setWindowTitle(_translate("WWind", "Form"))
        self.Elapsedtime.setText(_translate("WWind", "Elapsed time : "))
        self.WindInfo.setText(_translate("WWind", "Wind : 6.2m/s, 10°, No rain"))
        self.btn_clear.setText(_translate("WWind", "X"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WWind = QtWidgets.QWidget()
    ui = Ui_WWind()
    ui.setupUi(WWind)
    WWind.show()
    sys.exit(app.exec_())
