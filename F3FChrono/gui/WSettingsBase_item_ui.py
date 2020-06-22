# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingsBase_item.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingBase_item(object):
    def setupUi(self, WSettingBase_item):
        WSettingBase_item.setObjectName("WSettingBase_item")
        WSettingBase_item.resize(231, 27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WSettingBase_item.sizePolicy().hasHeightForWidth())
        WSettingBase_item.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WSettingBase_item)
        self.gridLayout.setContentsMargins(-1, 1, -1, 1)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonDelete = QtWidgets.QPushButton(WSettingBase_item)
        self.buttonDelete.setMaximumSize(QtCore.QSize(33, 16777215))
        self.buttonDelete.setObjectName("buttonDelete")
        self.gridLayout.addWidget(self.buttonDelete, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ipAddress = QtWidgets.QLabel(WSettingBase_item)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ipAddress.sizePolicy().hasHeightForWidth())
        self.ipAddress.setSizePolicy(sizePolicy)
        self.ipAddress.setObjectName("ipAddress")
        self.horizontalLayout.addWidget(self.ipAddress)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonMove = QtWidgets.QPushButton(WSettingBase_item)
        self.buttonMove.setMaximumSize(QtCore.QSize(33, 16777215))
        self.buttonMove.setObjectName("buttonMove")
        self.gridLayout.addWidget(self.buttonMove, 0, 2, 1, 1)

        self.retranslateUi(WSettingBase_item)
        QtCore.QMetaObject.connectSlotsByName(WSettingBase_item)

    def retranslateUi(self, WSettingBase_item):
        _translate = QtCore.QCoreApplication.translate
        WSettingBase_item.setWindowTitle(_translate("WSettingBase_item", "Form"))
        self.buttonDelete.setText(_translate("WSettingBase_item", "Del"))
        self.ipAddress.setText(_translate("WSettingBase_item", "192.168.0.16"))
        self.buttonMove.setText(_translate("WSettingBase_item", "-->"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingBase_item = QtWidgets.QWidget()
    ui = Ui_WSettingBase_item()
    ui.setupUi(WSettingBase_item)
    WSettingBase_item.show()
    sys.exit(app.exec_())
