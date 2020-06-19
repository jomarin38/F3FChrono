# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulate_base_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_base_widget(object):
    def setupUi(self, base_widget):
        base_widget.setObjectName("base_widget")
        base_widget.resize(225, 25)
        self.gridLayout = QtWidgets.QGridLayout(base_widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ipAddress = QtWidgets.QLineEdit(base_widget)
        self.ipAddress.setObjectName("ipAddress")
        self.gridLayout.addWidget(self.ipAddress, 0, 0, 1, 1)
        self.buttonSend = QtWidgets.QPushButton(base_widget)
        self.buttonSend.setMaximumSize(QtCore.QSize(45, 16777215))
        self.buttonSend.setObjectName("buttonSend")
        self.gridLayout.addWidget(self.buttonSend, 0, 2, 1, 1)
        self.event = QtWidgets.QLineEdit(base_widget)
        self.event.setMaximumSize(QtCore.QSize(50, 16777215))
        self.event.setObjectName("event")
        self.gridLayout.addWidget(self.event, 0, 1, 1, 1)

        self.retranslateUi(base_widget)
        QtCore.QMetaObject.connectSlotsByName(base_widget)
        base_widget.setTabOrder(self.ipAddress, self.event)
        base_widget.setTabOrder(self.event, self.buttonSend)

    def retranslateUi(self, base_widget):
        _translate = QtCore.QCoreApplication.translate
        base_widget.setWindowTitle(_translate("base_widget", "Form"))
        self.ipAddress.setText(_translate("base_widget", "192.168.0.16"))
        self.buttonSend.setText(_translate("base_widget", "Send"))
        self.event.setText(_translate("base_widget", "Event"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    base_widget = QtWidgets.QWidget()
    ui = Ui_base_widget()
    ui.setupUi(base_widget)
    base_widget.show()
    sys.exit(app.exec_())
