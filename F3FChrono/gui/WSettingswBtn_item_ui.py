# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingswBtn_item.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingwBtn_item(object):
    def setupUi(self, WSettingwBtn_item):
        WSettingwBtn_item.setObjectName("WSettingwBtn_item")
        WSettingwBtn_item.resize(398, 27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WSettingwBtn_item.sizePolicy().hasHeightForWidth())
        WSettingwBtn_item.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WSettingwBtn_item)
        self.gridLayout.setContentsMargins(-1, 1, -1, 1)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(WSettingwBtn_item)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.buttonDelete = QtWidgets.QPushButton(WSettingwBtn_item)
        self.buttonDelete.setMaximumSize(QtCore.QSize(33, 16777215))
        self.buttonDelete.setObjectName("buttonDelete")
        self.gridLayout.addWidget(self.buttonDelete, 0, 1, 1, 1)
        self.comboBox_SP = QtWidgets.QComboBox(WSettingwBtn_item)
        self.comboBox_SP.setObjectName("comboBox_SP")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.gridLayout.addWidget(self.comboBox_SP, 0, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ipAddress = QtWidgets.QLabel(WSettingwBtn_item)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ipAddress.sizePolicy().hasHeightForWidth())
        self.ipAddress.setSizePolicy(sizePolicy)
        self.ipAddress.setObjectName("ipAddress")
        self.horizontalLayout.addWidget(self.ipAddress)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(WSettingwBtn_item)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 4, 1, 1)
        self.comboBox_LP = QtWidgets.QComboBox(WSettingwBtn_item)
        self.comboBox_LP.setObjectName("comboBox_LP")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.gridLayout.addWidget(self.comboBox_LP, 0, 5, 1, 1)

        self.retranslateUi(WSettingwBtn_item)
        QtCore.QMetaObject.connectSlotsByName(WSettingwBtn_item)

    def retranslateUi(self, WSettingwBtn_item):
        _translate = QtCore.QCoreApplication.translate
        WSettingwBtn_item.setWindowTitle(_translate("WSettingwBtn_item", "Form"))
        self.label.setText(_translate("WSettingwBtn_item", "SP"))
        self.buttonDelete.setText(_translate("WSettingwBtn_item", "Del"))
        self.comboBox_SP.setItemText(0, _translate("WSettingwBtn_item", "None"))
        self.comboBox_SP.setItemText(1, _translate("WSettingwBtn_item", "Base A"))
        self.comboBox_SP.setItemText(2, _translate("WSettingwBtn_item", "Base B"))
        self.comboBox_SP.setItemText(3, _translate("WSettingwBtn_item", "Next Btn"))
        self.comboBox_SP.setItemText(4, _translate("WSettingwBtn_item", "Switch Mode"))
        self.ipAddress.setText(_translate("WSettingwBtn_item", "192.168.0.16"))
        self.label_2.setText(_translate("WSettingwBtn_item", "LP"))
        self.comboBox_LP.setItemText(0, _translate("WSettingwBtn_item", "None"))
        self.comboBox_LP.setItemText(1, _translate("WSettingwBtn_item", "Base A"))
        self.comboBox_LP.setItemText(2, _translate("WSettingwBtn_item", "Base B"))
        self.comboBox_LP.setItemText(3, _translate("WSettingwBtn_item", "Next Btn"))
        self.comboBox_LP.setItemText(4, _translate("WSettingwBtn_item", "Switch Mode"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingwBtn_item = QtWidgets.QWidget()
    ui = Ui_WSettingwBtn_item()
    ui.setupUi(WSettingwBtn_item)
    WSettingwBtn_item.show()
    sys.exit(app.exec_())
