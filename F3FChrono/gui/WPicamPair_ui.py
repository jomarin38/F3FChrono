# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WPicamPair.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WPicamPair(object):
    def setupUi(self, WPicamPair):
        WPicamPair.setObjectName("WPicamPair")
        WPicamPair.resize(480, 268)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WPicamPair.sizePolicy().hasHeightForWidth())
        WPicamPair.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WPicamPair)
        self.gridLayout.setContentsMargins(-1, 3, -1, 3)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(WPicamPair)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.picamB = QtWidgets.QLineEdit(WPicamPair)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.picamB.sizePolicy().hasHeightForWidth())
        self.picamB.setSizePolicy(sizePolicy)
        self.picamB.setMinimumSize(QtCore.QSize(0, 0))
        self.picamB.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.picamB.setObjectName("picamB")
        self.horizontalLayout_6.addWidget(self.picamB)
        self.label_4 = QtWidgets.QLabel(WPicamPair)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)
        self.btn_invertpicam = QtWidgets.QPushButton(WPicamPair)
        self.btn_invertpicam.setObjectName("btn_invertpicam")
        self.gridLayout_2.addWidget(self.btn_invertpicam, 1, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.picamA = QtWidgets.QLineEdit(WPicamPair)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.picamA.sizePolicy().hasHeightForWidth())
        self.picamA.setSizePolicy(sizePolicy)
        self.picamA.setMinimumSize(QtCore.QSize(0, 0))
        self.picamA.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.picamA.setObjectName("picamA")
        self.horizontalLayout_7.addWidget(self.picamA)
        self.label_5 = QtWidgets.QLabel(WPicamPair)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 2, 0, 1, 1)
        self.btn_invert_bases = QtWidgets.QPushButton(WPicamPair)
        self.btn_invert_bases.setObjectName("btn_invert_bases")
        self.gridLayout_2.addWidget(self.btn_invert_bases, 1, 1, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.baseA = QtWidgets.QLineEdit(WPicamPair)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseA.sizePolicy().hasHeightForWidth())
        self.baseA.setSizePolicy(sizePolicy)
        self.baseA.setMinimumSize(QtCore.QSize(0, 0))
        self.baseA.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.baseA.setObjectName("baseA")
        self.horizontalLayout_8.addWidget(self.baseA)
        self.label_6 = QtWidgets.QLabel(WPicamPair)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 2, 1, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.baseB = QtWidgets.QLineEdit(WPicamPair)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseB.sizePolicy().hasHeightForWidth())
        self.baseB.setSizePolicy(sizePolicy)
        self.baseB.setMinimumSize(QtCore.QSize(0, 0))
        self.baseB.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.baseB.setObjectName("baseB")
        self.horizontalLayout_9.addWidget(self.baseB)
        self.label_7 = QtWidgets.QLabel(WPicamPair)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_cancel = QtWidgets.QPushButton(WPicamPair)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.btn_valid = QtWidgets.QPushButton(WPicamPair)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_valid.setFont(font)
        self.btn_valid.setObjectName("btn_valid")
        self.horizontalLayout.addWidget(self.btn_valid)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(WPicamPair)
        QtCore.QMetaObject.connectSlotsByName(WPicamPair)
        WPicamPair.setTabOrder(self.btn_invertpicam, self.btn_invert_bases)
        WPicamPair.setTabOrder(self.btn_invert_bases, self.picamA)
        WPicamPair.setTabOrder(self.picamA, self.baseA)
        WPicamPair.setTabOrder(self.baseA, self.picamB)
        WPicamPair.setTabOrder(self.picamB, self.baseB)
        WPicamPair.setTabOrder(self.baseB, self.btn_cancel)
        WPicamPair.setTabOrder(self.btn_cancel, self.btn_valid)

    def retranslateUi(self, WPicamPair):
        _translate = QtCore.QCoreApplication.translate
        WPicamPair.setWindowTitle(_translate("WPicamPair", "Form"))
        self.label.setText(_translate("WPicamPair", "piCAMs & buttons paired"))
        self.picamB.setText(_translate("WPicamPair", "192.168.0.16"))
        self.label_4.setText(_translate("WPicamPair", "piCamB"))
        self.btn_invertpicam.setText(_translate("WPicamPair", "Invert piCam"))
        self.picamA.setText(_translate("WPicamPair", "192.168.0.17"))
        self.label_5.setText(_translate("WPicamPair", "piCamA"))
        self.btn_invert_bases.setText(_translate("WPicamPair", "Invert Buttons"))
        self.baseA.setText(_translate("WPicamPair", "Port 17"))
        self.label_6.setText(_translate("WPicamPair", "BaseA"))
        self.baseB.setText(_translate("WPicamPair", "Port 18"))
        self.label_7.setText(_translate("WPicamPair", "BaseB"))
        self.btn_cancel.setText(_translate("WPicamPair", "Cancel"))
        self.btn_valid.setText(_translate("WPicamPair", "Valid"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WPicamPair = QtWidgets.QWidget()
    ui = Ui_WPicamPair()
    ui.setupUi(WPicamPair)
    WPicamPair.show()
    sys.exit(app.exec_())
