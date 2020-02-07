# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WChronoBtn.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WChronoBtn(object):
    def setupUi(self, WChronoBtn):
        WChronoBtn.setObjectName("WChronoBtn")
        WChronoBtn.resize(480, 45)
        self.gridLayout = QtWidgets.QGridLayout(WChronoBtn)
        self.gridLayout.setContentsMargins(-1, 3, -1, 3)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Btn_Home = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_Home.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Home.setFont(font)
        self.Btn_Home.setFlat(False)
        self.Btn_Home.setObjectName("Btn_Home")
        self.horizontalLayout.addWidget(self.Btn_Home)
        self.Btn_CancelRound = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_CancelRound.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Btn_CancelRound.setObjectName("Btn_CancelRound")
        self.horizontalLayout.addWidget(self.Btn_CancelRound)
        self.Btn_reflight = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_reflight.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_reflight.setFont(font)
        self.Btn_reflight.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_reflight.setFlat(False)
        self.Btn_reflight.setObjectName("Btn_reflight")
        self.horizontalLayout.addWidget(self.Btn_reflight)
        self.Btn_Next = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_Next.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Next.setFont(font)
        self.Btn_Next.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_Next.setFlat(False)
        self.Btn_Next.setObjectName("Btn_Next")
        self.horizontalLayout.addWidget(self.Btn_Next)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(WChronoBtn)
        QtCore.QMetaObject.connectSlotsByName(WChronoBtn)

    def retranslateUi(self, WChronoBtn):
        _translate = QtCore.QCoreApplication.translate
        WChronoBtn.setWindowTitle(_translate("WChronoBtn", "Form"))
        self.Btn_Home.setText(_translate("WChronoBtn", "Home"))
        self.Btn_CancelRound.setText(_translate("WChronoBtn", "Cancel Round"))
        self.Btn_reflight.setText(_translate("WChronoBtn", "Reflight"))
        self.Btn_Next.setText(_translate("WChronoBtn", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChronoBtn = QtWidgets.QWidget()
    ui = Ui_WChronoBtn()
    ui.setupUi(WChronoBtn)
    WChronoBtn.show()
    sys.exit(app.exec_())
