# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WChronoBtn_cancel.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WChronoBtn_Cancel(object):
    def setupUi(self, WChronoBtn_Cancel):
        WChronoBtn_Cancel.setObjectName("WChronoBtn_Cancel")
        WChronoBtn_Cancel.resize(480, 40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WChronoBtn_Cancel.sizePolicy().hasHeightForWidth())
        WChronoBtn_Cancel.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(WChronoBtn_Cancel)
        self.gridLayout.setContentsMargins(3, 1, 3, 1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Btn_Home = QtWidgets.QPushButton(WChronoBtn_Cancel)
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
        self.label_cancelround = QtWidgets.QLabel(WChronoBtn_Cancel)
        self.label_cancelround.setObjectName("label_cancelround")
        self.horizontalLayout.addWidget(self.label_cancelround)
        self.Btn_Next = QtWidgets.QPushButton(WChronoBtn_Cancel)
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

        self.retranslateUi(WChronoBtn_Cancel)
        QtCore.QMetaObject.connectSlotsByName(WChronoBtn_Cancel)

    def retranslateUi(self, WChronoBtn_Cancel):
        _translate = QtCore.QCoreApplication.translate
        WChronoBtn_Cancel.setWindowTitle(_translate("WChronoBtn_Cancel", "Form"))
        self.Btn_Home.setText(_translate("WChronoBtn_Cancel", "Exit"))
        self.label_cancelround.setText(_translate("WChronoBtn_Cancel", "Cancel round wait Next button"))
        self.Btn_Next.setText(_translate("WChronoBtn_Cancel", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WChronoBtn_Cancel = QtWidgets.QWidget()
    ui = Ui_WChronoBtn_Cancel()
    ui.setupUi(WChronoBtn_Cancel)
    WChronoBtn_Cancel.show()
    sys.exit(app.exec_())
