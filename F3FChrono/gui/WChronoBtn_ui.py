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
        WChronoBtn.resize(288, 43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WChronoBtn.sizePolicy().hasHeightForWidth())
        WChronoBtn.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WChronoBtn)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.Btn_Next = QtWidgets.QPushButton(WChronoBtn)
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
        self.gridLayout.addWidget(self.Btn_Next, 1, 2, 1, 1)
        self.Btn_gscoring = QtWidgets.QPushButton(WChronoBtn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_gscoring.sizePolicy().hasHeightForWidth())
        self.Btn_gscoring.setSizePolicy(sizePolicy)
        self.Btn_gscoring.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Btn_gscoring.setFont(font)
        self.Btn_gscoring.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_gscoring.setFlat(False)
        self.Btn_gscoring.setObjectName("Btn_gscoring")
        self.gridLayout.addWidget(self.Btn_gscoring, 1, 1, 1, 1)
        self.Btn_Home = QtWidgets.QPushButton(WChronoBtn)
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
        self.gridLayout.addWidget(self.Btn_Home, 1, 0, 1, 1)

        self.retranslateUi(WChronoBtn)
        QtCore.QMetaObject.connectSlotsByName(WChronoBtn)

    def retranslateUi(self, WChronoBtn):
        _translate = QtCore.QCoreApplication.translate
        WChronoBtn.setWindowTitle(_translate("WChronoBtn", "Form"))
        self.Btn_Next.setText(_translate("WChronoBtn", "Next"))
        self.Btn_gscoring.setText(_translate("WChronoBtn", "G Scoring"))
        self.Btn_Home.setText(_translate("WChronoBtn", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChronoBtn = QtWidgets.QWidget()
    ui = Ui_WChronoBtn()
    ui.setupUi(WChronoBtn)
    WChronoBtn.show()
    sys.exit(app.exec_())
