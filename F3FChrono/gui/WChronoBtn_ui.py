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
        WChronoBtn.resize(575, 45)
        self.gridLayout = QtWidgets.QGridLayout(WChronoBtn)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Btn_Home = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_Home.setMaximumSize(QtCore.QSize(63, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Home.setFont(font)
        self.Btn_Home.setFlat(False)
        self.Btn_Home.setObjectName("Btn_Home")
        self.horizontalLayout.addWidget(self.Btn_Home)
        self.Btn_CancelRound = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_CancelRound.setMaximumSize(QtCore.QSize(72, 16777215))
        self.Btn_CancelRound.setObjectName("Btn_CancelRound")
        self.horizontalLayout.addWidget(self.Btn_CancelRound)
        self.Btn_reflight = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_reflight.setMaximumSize(QtCore.QSize(63, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_reflight.setFont(font)
        self.Btn_reflight.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_reflight.setFlat(False)
        self.Btn_reflight.setObjectName("Btn_reflight")
        self.horizontalLayout.addWidget(self.Btn_reflight)
        self.Btn_Penalty = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_Penalty.setMaximumSize(QtCore.QSize(63, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Penalty.setFont(font)
        self.Btn_Penalty.setFlat(False)
        self.Btn_Penalty.setObjectName("Btn_Penalty")
        self.horizontalLayout.addWidget(self.Btn_Penalty)
        self.Btn_Penalty_1 = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_Penalty_1.setEnabled(True)
        self.Btn_Penalty_1.setMaximumSize(QtCore.QSize(63, 16777215))
        self.Btn_Penalty_1.setObjectName("Btn_Penalty_1")
        self.horizontalLayout.addWidget(self.Btn_Penalty_1)
        self.Btn_Penalty_2 = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_Penalty_2.setMaximumSize(QtCore.QSize(63, 16777215))
        self.Btn_Penalty_2.setObjectName("Btn_Penalty_2")
        self.horizontalLayout.addWidget(self.Btn_Penalty_2)
        self.Btn_NullFlight = QtWidgets.QPushButton(WChronoBtn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_NullFlight.sizePolicy().hasHeightForWidth())
        self.Btn_NullFlight.setSizePolicy(sizePolicy)
        self.Btn_NullFlight.setMinimumSize(QtCore.QSize(0, 0))
        self.Btn_NullFlight.setMaximumSize(QtCore.QSize(63, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_NullFlight.setFont(font)
        self.Btn_NullFlight.setFlat(False)
        self.Btn_NullFlight.setObjectName("Btn_NullFlight")
        self.horizontalLayout.addWidget(self.Btn_NullFlight)
        self.Btn_Next = QtWidgets.QPushButton(WChronoBtn)
        self.Btn_Next.setMaximumSize(QtCore.QSize(63, 16777215))
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
        self.Btn_CancelRound.setText(_translate("WChronoBtn", "Cancel R.."))
        self.Btn_reflight.setText(_translate("WChronoBtn", "Reflight"))
        self.Btn_Penalty.setText(_translate("WChronoBtn", "Penalty"))
        self.Btn_Penalty_1.setText(_translate("WChronoBtn", "100"))
        self.Btn_Penalty_2.setText(_translate("WChronoBtn", "1000"))
        self.Btn_NullFlight.setText(_translate("WChronoBtn", "O Flight"))
        self.Btn_Next.setText(_translate("WChronoBtn", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChronoBtn = QtWidgets.QWidget()
    ui = Ui_WChronoBtn()
    ui.setupUi(WChronoBtn)
    WChronoBtn.show()
    sys.exit(app.exec_())
