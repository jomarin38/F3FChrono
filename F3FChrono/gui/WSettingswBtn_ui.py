# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingswBtn.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingswBtn(object):
    def setupUi(self, WSettingswBtn):
        WSettingswBtn.setObjectName("WSettingswBtn")
        WSettingswBtn.resize(437, 264)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WSettingswBtn.sizePolicy().hasHeightForWidth())
        WSettingswBtn.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WSettingswBtn)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(WSettingswBtn)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.btn_back = QtWidgets.QPushButton(WSettingswBtn)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_back.setFont(font)
        self.btn_back.setObjectName("btn_back")
        self.gridLayout.addWidget(self.btn_back, 4, 0, 1, 1)
        self.btn_cancel = QtWidgets.QPushButton(WSettingswBtn)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayout.addWidget(self.btn_cancel, 4, 1, 1, 1)
        self.btn_valid = QtWidgets.QPushButton(WSettingswBtn)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_valid.setFont(font)
        self.btn_valid.setObjectName("btn_valid")
        self.gridLayout.addWidget(self.btn_valid, 4, 2, 1, 1)
        self.buttonDetect = QtWidgets.QPushButton(WSettingswBtn)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.buttonDetect.setFont(font)
        self.buttonDetect.setObjectName("buttonDetect")
        self.gridLayout.addWidget(self.buttonDetect, 1, 0, 1, 3)
        self.listWidget_wBtn = QtWidgets.QListWidget(WSettingswBtn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_wBtn.sizePolicy().hasHeightForWidth())
        self.listWidget_wBtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.listWidget_wBtn.setFont(font)
        self.listWidget_wBtn.setObjectName("listWidget_wBtn")
        self.gridLayout.addWidget(self.listWidget_wBtn, 2, 0, 1, 3)
        self.buttonClear = QtWidgets.QPushButton(WSettingswBtn)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.buttonClear.setFont(font)
        self.buttonClear.setObjectName("buttonClear")
        self.gridLayout.addWidget(self.buttonClear, 3, 0, 1, 3)

        self.retranslateUi(WSettingswBtn)
        QtCore.QMetaObject.connectSlotsByName(WSettingswBtn)

    def retranslateUi(self, WSettingswBtn):
        _translate = QtCore.QCoreApplication.translate
        WSettingswBtn.setWindowTitle(_translate("WSettingswBtn", "Form"))
        self.label.setText(_translate("WSettingswBtn", "Wireless button Settings"))
        self.btn_back.setText(_translate("WSettingswBtn", "Back to Settings"))
        self.btn_cancel.setText(_translate("WSettingswBtn", "Cancel"))
        self.btn_valid.setText(_translate("WSettingswBtn", "Valid"))
        self.buttonDetect.setText(_translate("WSettingswBtn", "Detect"))
        self.buttonClear.setText(_translate("WSettingswBtn", "Clear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingswBtn = QtWidgets.QWidget()
    ui = Ui_WSettingswBtn()
    ui.setupUi(WSettingswBtn)
    WSettingswBtn.show()
    sys.exit(app.exec_())
