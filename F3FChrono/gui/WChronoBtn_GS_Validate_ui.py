# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WChronoBtn_GS_Validate.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WChronoGSEnable(object):
    def setupUi(self, WChronoGSEnable):
        WChronoGSEnable.setObjectName("WChronoGSEnable")
        WChronoGSEnable.resize(480, 40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WChronoGSEnable.sizePolicy().hasHeightForWidth())
        WChronoGSEnable.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WChronoGSEnable)
        self.gridLayout.setContentsMargins(3, 1, 3, 1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Btn_Home = QtWidgets.QPushButton(WChronoGSEnable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Home.sizePolicy().hasHeightForWidth())
        self.Btn_Home.setSizePolicy(sizePolicy)
        self.Btn_Home.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Btn_Home.setFont(font)
        self.Btn_Home.setFlat(False)
        self.Btn_Home.setObjectName("Btn_Home")
        self.horizontalLayout.addWidget(self.Btn_Home)
        self.label_cancelround = QtWidgets.QLabel(WChronoGSEnable)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_cancelround.setFont(font)
        self.label_cancelround.setObjectName("label_cancelround")
        self.horizontalLayout.addWidget(self.label_cancelround)
        self.Btn_Next = QtWidgets.QPushButton(WChronoGSEnable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Next.sizePolicy().hasHeightForWidth())
        self.Btn_Next.setSizePolicy(sizePolicy)
        self.Btn_Next.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Btn_Next.setFont(font)
        self.Btn_Next.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_Next.setFlat(False)
        self.Btn_Next.setObjectName("Btn_Next")
        self.horizontalLayout.addWidget(self.Btn_Next)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(WChronoGSEnable)
        QtCore.QMetaObject.connectSlotsByName(WChronoGSEnable)

    def retranslateUi(self, WChronoGSEnable):
        _translate = QtCore.QCoreApplication.translate
        WChronoGSEnable.setWindowTitle(_translate("WChronoGSEnable", "Form"))
        self.Btn_Home.setText(_translate("WChronoGSEnable", "Exit"))
        self.label_cancelround.setText(_translate("WChronoGSEnable", "Enable Group Scoring ?"))
        self.Btn_Next.setText(_translate("WChronoGSEnable", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChronoGSEnable = QtWidgets.QWidget()
    ui = Ui_WChronoGSEnable()
    ui.setupUi(WChronoGSEnable)
    WChronoGSEnable.show()
    sys.exit(app.exec_())
