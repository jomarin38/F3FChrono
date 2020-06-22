# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WConfig.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WConfig(object):
    def setupUi(self, WConfig):
        WConfig.setObjectName("WConfig")
        WConfig.resize(480, 287)
        self.gridLayout = QtWidgets.QGridLayout(WConfig)
        self.gridLayout.setContentsMargins(-1, 1, -1, 3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_settings = QtWidgets.QPushButton(WConfig)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.btn_settings.setFont(font)
        self.btn_settings.setObjectName("btn_settings")
        self.horizontalLayout_4.addWidget(self.btn_settings)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.Contest = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.Contest.setFont(font)
        self.Contest.setAlignment(QtCore.Qt.AlignCenter)
        self.Contest.setObjectName("Contest")
        self.verticalLayout.addWidget(self.Contest)
        self.ContestList = QtWidgets.QComboBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ContestList.setFont(font)
        self.ContestList.setObjectName("ContestList")
        self.ContestList.addItem("")
        self.verticalLayout.addWidget(self.ContestList)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ContestLimitLabel = QtWidgets.QLabel(WConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContestLimitLabel.sizePolicy().hasHeightForWidth())
        self.ContestLimitLabel.setSizePolicy(sizePolicy)
        self.ContestLimitLabel.setMinimumSize(QtCore.QSize(225, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.ContestLimitLabel.setFont(font)
        self.ContestLimitLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ContestLimitLabel.setObjectName("ContestLimitLabel")
        self.horizontalLayout_3.addWidget(self.ContestLimitLabel)
        self.MaxInterruptLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MaxInterruptLabel.setFont(font)
        self.MaxInterruptLabel.setObjectName("MaxInterruptLabel")
        self.horizontalLayout_3.addWidget(self.MaxInterruptLabel)
        self.MaxInterruptValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MaxInterruptValue.setFont(font)
        self.MaxInterruptValue.setMaximum(100)
        self.MaxInterruptValue.setObjectName("MaxInterruptValue")
        self.horizontalLayout_3.addWidget(self.MaxInterruptValue)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.WindMinLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.WindMinLabel.setFont(font)
        self.WindMinLabel.setObjectName("WindMinLabel")
        self.horizontalLayout_7.addWidget(self.WindMinLabel)
        self.WindMinValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.WindMinValue.setFont(font)
        self.WindMinValue.setObjectName("WindMinValue")
        self.horizontalLayout_7.addWidget(self.WindMinValue)
        self.WindMaxLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.WindMaxLabel.setFont(font)
        self.WindMaxLabel.setObjectName("WindMaxLabel")
        self.horizontalLayout_7.addWidget(self.WindMaxLabel)
        self.WindMaxValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.WindMaxValue.setFont(font)
        self.WindMaxValue.setObjectName("WindMaxValue")
        self.horizontalLayout_7.addWidget(self.WindMaxValue)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.OrientationLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OrientationLabel.setFont(font)
        self.OrientationLabel.setObjectName("OrientationLabel")
        self.horizontalLayout_9.addWidget(self.OrientationLabel)
        self.OrientationValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OrientationValue.setFont(font)
        self.OrientationValue.setObjectName("OrientationValue")
        self.horizontalLayout_9.addWidget(self.OrientationValue)
        self.RevolLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.RevolLabel.setFont(font)
        self.RevolLabel.setObjectName("RevolLabel")
        self.horizontalLayout_9.addWidget(self.RevolLabel)
        self.RevolValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.RevolValue.setFont(font)
        self.RevolValue.setObjectName("RevolValue")
        self.horizontalLayout_9.addWidget(self.RevolValue)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.dayduratiolabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dayduratiolabel.setFont(font)
        self.dayduratiolabel.setObjectName("dayduratiolabel")
        self.horizontalLayout_12.addWidget(self.dayduratiolabel)
        self.daydurationvalue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.daydurationvalue.setFont(font)
        self.daydurationvalue.setObjectName("daydurationvalue")
        self.horizontalLayout_12.addWidget(self.daydurationvalue)
        self.bib_start_label = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bib_start_label.setFont(font)
        self.bib_start_label.setObjectName("bib_start_label")
        self.horizontalLayout_12.addWidget(self.bib_start_label)
        self.bib_start = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bib_start.setFont(font)
        self.bib_start.setObjectName("bib_start")
        self.horizontalLayout_12.addWidget(self.bib_start)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.randombtn = QtWidgets.QPushButton(WConfig)
        self.randombtn.setObjectName("randombtn")
        self.horizontalLayout_11.addWidget(self.randombtn)
        self.day_1btn = QtWidgets.QPushButton(WConfig)
        self.day_1btn.setObjectName("day_1btn")
        self.horizontalLayout_11.addWidget(self.day_1btn)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.StartBtn = QtWidgets.QPushButton(WConfig)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.StartBtn.setFont(font)
        self.StartBtn.setObjectName("StartBtn")
        self.verticalLayout.addWidget(self.StartBtn)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(WConfig)
        QtCore.QMetaObject.connectSlotsByName(WConfig)

    def retranslateUi(self, WConfig):
        _translate = QtCore.QCoreApplication.translate
        WConfig.setWindowTitle(_translate("WConfig", "Form"))
        self.btn_settings.setText(_translate("WConfig", "Race Management Settings"))
        self.Contest.setText(_translate("WConfig", "Contest"))
        self.ContestList.setItemText(0, _translate("WConfig", "Training"))
        self.ContestLimitLabel.setText(_translate("WConfig", "Contest settings"))
        self.MaxInterruptLabel.setText(_translate("WConfig", "Max Interrupt (mn)"))
        self.WindMinLabel.setText(_translate("WConfig", "WindMin (m/s)"))
        self.WindMaxLabel.setText(_translate("WConfig", "WindMax (m/s)"))
        self.OrientationLabel.setText(_translate("WConfig", "Orientation (°)"))
        self.RevolLabel.setText(_translate("WConfig", "Revol"))
        self.dayduratiolabel.setText(_translate("WConfig", "Day duration"))
        self.bib_start_label.setText(_translate("WConfig", "BIB Starting"))
        self.randombtn.setText(_translate("WConfig", "Random"))
        self.day_1btn.setText(_translate("WConfig", "Day+1"))
        self.StartBtn.setText(_translate("WConfig", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WConfig = QtWidgets.QWidget()
    ui = Ui_WConfig()
    ui.setupUi(WConfig)
    WConfig.show()
    sys.exit(app.exec_())
