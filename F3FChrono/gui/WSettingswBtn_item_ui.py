# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingswBtn_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingwBtn_item(object):
    def setupUi(self, WSettingwBtn_item):
        WSettingwBtn_item.setObjectName("WSettingwBtn_item")
        WSettingwBtn_item.resize(493, 27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WSettingwBtn_item.sizePolicy().hasHeightForWidth())
        WSettingwBtn_item.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WSettingwBtn_item)
        self.gridLayout.setContentsMargins(0, 1, 0, 1)
        self.gridLayout.setHorizontalSpacing(1)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.ipAddress = QtWidgets.QLabel(WSettingwBtn_item)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ipAddress.sizePolicy().hasHeightForWidth())
        self.ipAddress.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ipAddress.setFont(font)
        self.ipAddress.setObjectName("ipAddress")
        self.gridLayout.addWidget(self.ipAddress, 0, 0, 3, 1)
        self.buttonDelete = QtWidgets.QPushButton(WSettingwBtn_item)
        self.buttonDelete.setMaximumSize(QtCore.QSize(33, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonDelete.setFont(font)
        self.buttonDelete.setObjectName("buttonDelete")
        self.gridLayout.addWidget(self.buttonDelete, 0, 1, 3, 1)
        self.label = QtWidgets.QLabel(WSettingwBtn_item)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(WSettingwBtn_item)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 6, 1, 1)
        self.comboBox_LP = QtWidgets.QComboBox(WSettingwBtn_item)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_LP.setFont(font)
        self.comboBox_LP.setObjectName("comboBox_LP")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.comboBox_LP.addItem("")
        self.gridLayout.addWidget(self.comboBox_LP, 0, 7, 3, 1)
        self.label_3 = QtWidgets.QLabel(WSettingwBtn_item)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 3, 1)
        self.comboBox_CL = QtWidgets.QComboBox(WSettingwBtn_item)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_CL.setFont(font)
        self.comboBox_CL.setObjectName("comboBox_CL")
        self.comboBox_CL.addItem("")
        self.comboBox_CL.addItem("")
        self.comboBox_CL.addItem("")
        self.comboBox_CL.addItem("")
        self.comboBox_CL.addItem("")
        self.comboBox_CL.addItem("")
        self.gridLayout.addWidget(self.comboBox_CL, 0, 3, 3, 1)
        self.comboBox_SP = QtWidgets.QComboBox(WSettingwBtn_item)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox_SP.setFont(font)
        self.comboBox_SP.setObjectName("comboBox_SP")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.comboBox_SP.addItem("")
        self.gridLayout.addWidget(self.comboBox_SP, 0, 5, 3, 1)

        self.retranslateUi(WSettingwBtn_item)
        QtCore.QMetaObject.connectSlotsByName(WSettingwBtn_item)

    def retranslateUi(self, WSettingwBtn_item):
        _translate = QtCore.QCoreApplication.translate
        WSettingwBtn_item.setWindowTitle(_translate("WSettingwBtn_item", "Form"))
        self.ipAddress.setText(_translate("WSettingwBtn_item", "192.168.0.16"))
        self.buttonDelete.setText(_translate("WSettingwBtn_item", "Del"))
        self.label.setText(_translate("WSettingwBtn_item", "S"))
        self.label_2.setText(_translate("WSettingwBtn_item", "L"))
        self.comboBox_LP.setItemText(0, _translate("WSettingwBtn_item", "None"))
        self.comboBox_LP.setItemText(1, _translate("WSettingwBtn_item", "Base A"))
        self.comboBox_LP.setItemText(2, _translate("WSettingwBtn_item", "Base B"))
        self.comboBox_LP.setItemText(3, _translate("WSettingwBtn_item", "Next Btn"))
        self.comboBox_LP.setItemText(4, _translate("WSettingwBtn_item", "Switch Mode"))
        self.comboBox_LP.setItemText(5, _translate("WSettingwBtn_item", "Penalty"))
        self.label_3.setText(_translate("WSettingwBtn_item", "C"))
        self.comboBox_CL.setItemText(0, _translate("WSettingwBtn_item", "None"))
        self.comboBox_CL.setItemText(1, _translate("WSettingwBtn_item", "Base A"))
        self.comboBox_CL.setItemText(2, _translate("WSettingwBtn_item", "Base B"))
        self.comboBox_CL.setItemText(3, _translate("WSettingwBtn_item", "Next Btn"))
        self.comboBox_CL.setItemText(4, _translate("WSettingwBtn_item", "Switch Mode"))
        self.comboBox_CL.setItemText(5, _translate("WSettingwBtn_item", "Penalty"))
        self.comboBox_SP.setItemText(0, _translate("WSettingwBtn_item", "None"))
        self.comboBox_SP.setItemText(1, _translate("WSettingwBtn_item", "Base A"))
        self.comboBox_SP.setItemText(2, _translate("WSettingwBtn_item", "Base B"))
        self.comboBox_SP.setItemText(3, _translate("WSettingwBtn_item", "Next Btn"))
        self.comboBox_SP.setItemText(4, _translate("WSettingwBtn_item", "Switch Mode"))
        self.comboBox_SP.setItemText(5, _translate("WSettingwBtn_item", "Penalty"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingwBtn_item = QtWidgets.QWidget()
    ui = Ui_WSettingwBtn_item()
    ui.setupUi(WSettingwBtn_item)
    WSettingwBtn_item.show()
    sys.exit(app.exec_())
