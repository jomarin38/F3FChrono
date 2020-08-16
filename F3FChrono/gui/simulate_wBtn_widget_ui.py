# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulate_wBtn_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wBtn_widget(object):
    def setupUi(self, wBtn_widget):
        wBtn_widget.setObjectName("wBtn_widget")
        wBtn_widget.resize(263, 25)
        self.gridLayout = QtWidgets.QGridLayout(wBtn_widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonSendSP = QtWidgets.QPushButton(wBtn_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSendSP.sizePolicy().hasHeightForWidth())
        self.buttonSendSP.setSizePolicy(sizePolicy)
        self.buttonSendSP.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.buttonSendSP.setObjectName("buttonSendSP")
        self.gridLayout.addWidget(self.buttonSendSP, 0, 1, 1, 1)
        self.ipAddress = QtWidgets.QLineEdit(wBtn_widget)
        self.ipAddress.setObjectName("ipAddress")
        self.gridLayout.addWidget(self.ipAddress, 0, 0, 1, 1)
        self.buttonSendLP = QtWidgets.QPushButton(wBtn_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSendLP.sizePolicy().hasHeightForWidth())
        self.buttonSendLP.setSizePolicy(sizePolicy)
        self.buttonSendLP.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.buttonSendLP.setObjectName("buttonSendLP")
        self.gridLayout.addWidget(self.buttonSendLP, 0, 2, 1, 1)

        self.retranslateUi(wBtn_widget)
        QtCore.QMetaObject.connectSlotsByName(wBtn_widget)
        wBtn_widget.setTabOrder(self.ipAddress, self.buttonSendSP)

    def retranslateUi(self, wBtn_widget):
        _translate = QtCore.QCoreApplication.translate
        wBtn_widget.setWindowTitle(_translate("wBtn_widget", "Form"))
        self.buttonSendSP.setText(_translate("wBtn_widget", "SP"))
        self.ipAddress.setText(_translate("wBtn_widget", "192.168.0.16"))
        self.buttonSendLP.setText(_translate("wBtn_widget", "LP"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wBtn_widget = QtWidgets.QWidget()
    ui = Ui_wBtn_widget()
    ui.setupUi(wBtn_widget)
    wBtn_widget.show()
    sys.exit(app.exec_())
