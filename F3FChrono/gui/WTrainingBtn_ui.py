# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WTrainingBtn.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WTrainingBtn(object):
    def setupUi(self, WTrainingBtn):
        WTrainingBtn.setObjectName("WTrainingBtn")
        WTrainingBtn.resize(480, 45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WTrainingBtn.sizePolicy().hasHeightForWidth())
        WTrainingBtn.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WTrainingBtn)
        self.gridLayout.setContentsMargins(3, 1, 3, 1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Btn_Home = QtWidgets.QPushButton(WTrainingBtn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Home.sizePolicy().hasHeightForWidth())
        self.Btn_Home.setSizePolicy(sizePolicy)
        self.Btn_Home.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Home.setFont(font)
        self.Btn_Home.setFlat(False)
        self.Btn_Home.setObjectName("Btn_Home")
        self.horizontalLayout.addWidget(self.Btn_Home)
        self.Btn_reset = QtWidgets.QPushButton(WTrainingBtn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_reset.sizePolicy().hasHeightForWidth())
        self.Btn_reset.setSizePolicy(sizePolicy)
        self.Btn_reset.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_reset.setFont(font)
        self.Btn_reset.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_reset.setFlat(False)
        self.Btn_reset.setObjectName("Btn_reset")
        self.horizontalLayout.addWidget(self.Btn_reset)
        self.Btn_Next = QtWidgets.QPushButton(WTrainingBtn)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Next.sizePolicy().hasHeightForWidth())
        self.Btn_Next.setSizePolicy(sizePolicy)
        self.Btn_Next.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Btn_Next.setFont(font)
        self.Btn_Next.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Btn_Next.setFlat(False)
        self.Btn_Next.setObjectName("Btn_Next")
        self.horizontalLayout.addWidget(self.Btn_Next)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(WTrainingBtn)
        QtCore.QMetaObject.connectSlotsByName(WTrainingBtn)

    def retranslateUi(self, WTrainingBtn):
        _translate = QtCore.QCoreApplication.translate
        WTrainingBtn.setWindowTitle(_translate("WTrainingBtn", "Form"))
        self.Btn_Home.setText(_translate("WTrainingBtn", "Home"))
        self.Btn_reset.setText(_translate("WTrainingBtn", "Reset"))
        self.Btn_Next.setText(_translate("WTrainingBtn", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WTrainingBtn = QtWidgets.QWidget()
    ui = Ui_WTrainingBtn()
    ui.setupUi(WTrainingBtn)
    WTrainingBtn.show()
    sys.exit(app.exec_())
