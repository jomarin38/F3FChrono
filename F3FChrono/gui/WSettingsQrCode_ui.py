# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingsQrCode.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingsQrCode(object):
    def setupUi(self, WSettingsQrCode):
        WSettingsQrCode.setObjectName("WSettingsQrCode")
        WSettingsQrCode.resize(480, 253)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WSettingsQrCode.sizePolicy().hasHeightForWidth())
        WSettingsQrCode.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WSettingsQrCode)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(WSettingsQrCode)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(WSettingsQrCode)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)
        self.btn_back = QtWidgets.QPushButton(WSettingsQrCode)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setObjectName("btn_back")
        self.gridLayout.addWidget(self.btn_back, 2, 1, 1, 1)
        self.btn_AdminQRCode = QtWidgets.QPushButton(WSettingsQrCode)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_AdminQRCode.setFont(font)
        self.btn_AdminQRCode.setObjectName("btn_AdminQRCode")
        self.gridLayout.addWidget(self.btn_AdminQRCode, 2, 0, 1, 1)

        self.retranslateUi(WSettingsQrCode)
        QtCore.QMetaObject.connectSlotsByName(WSettingsQrCode)

    def retranslateUi(self, WSettingsQrCode):
        _translate = QtCore.QCoreApplication.translate
        WSettingsQrCode.setWindowTitle(_translate("WSettingsQrCode", "Form"))
        self.label.setText(_translate("WSettingsQrCode", "F3F Ranking QRCode"))
        self.label_2.setText(_translate("WSettingsQrCode", "Image display"))
        self.btn_back.setText(_translate("WSettingsQrCode", "Back to Settings"))
        self.btn_AdminQRCode.setText(_translate("WSettingsQrCode", "Admin QR Code"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingsQrCode = QtWidgets.QWidget()
    ui = Ui_WSettingsQrCode()
    ui.setupUi(WSettingsQrCode)
    WSettingsQrCode.show()
    sys.exit(app.exec_())
