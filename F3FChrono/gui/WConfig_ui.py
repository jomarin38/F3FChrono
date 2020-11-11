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
        WConfig.resize(446, 279)
        font = QtGui.QFont()
        font.setPointSize(12)
        WConfig.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WConfig)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.RevolLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.RevolLabel.setFont(font)
        self.RevolLabel.setObjectName("RevolLabel")
        self.gridLayout_2.addWidget(self.RevolLabel, 3, 2, 1, 1)
        self.day_1btn = QtWidgets.QPushButton(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.day_1btn.setFont(font)
        self.day_1btn.setObjectName("day_1btn")
        self.gridLayout_2.addWidget(self.day_1btn, 6, 2, 1, 2)
        self.ContestList = QtWidgets.QComboBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ContestList.setFont(font)
        self.ContestList.setObjectName("ContestList")
        self.ContestList.addItem("")
        self.gridLayout_2.addWidget(self.ContestList, 1, 0, 1, 4)
        self.WindMinValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.WindMinValue.setFont(font)
        self.WindMinValue.setObjectName("WindMinValue")
        self.gridLayout_2.addWidget(self.WindMinValue, 2, 1, 1, 1)
        self.WindMaxValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.WindMaxValue.setFont(font)
        self.WindMaxValue.setObjectName("WindMaxValue")
        self.gridLayout_2.addWidget(self.WindMaxValue, 3, 1, 1, 1)
        self.WindMaxLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.WindMaxLabel.setFont(font)
        self.WindMaxLabel.setObjectName("WindMaxLabel")
        self.gridLayout_2.addWidget(self.WindMaxLabel, 3, 0, 1, 1)
        self.RevolValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.RevolValue.setFont(font)
        self.RevolValue.setObjectName("RevolValue")
        self.gridLayout_2.addWidget(self.RevolValue, 3, 3, 1, 1)
        self.OrientationValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.OrientationValue.setFont(font)
        self.OrientationValue.setObjectName("OrientationValue")
        self.gridLayout_2.addWidget(self.OrientationValue, 4, 1, 1, 1)
        self.daydurationvalue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.daydurationvalue.setFont(font)
        self.daydurationvalue.setObjectName("daydurationvalue")
        self.gridLayout_2.addWidget(self.daydurationvalue, 5, 1, 1, 1)
        self.bib_start_label = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bib_start_label.setFont(font)
        self.bib_start_label.setObjectName("bib_start_label")
        self.gridLayout_2.addWidget(self.bib_start_label, 4, 2, 1, 1)
        self.MaxInterruptLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.MaxInterruptLabel.setFont(font)
        self.MaxInterruptLabel.setObjectName("MaxInterruptLabel")
        self.gridLayout_2.addWidget(self.MaxInterruptLabel, 2, 2, 1, 1)
        self.StartBtn = QtWidgets.QPushButton(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.StartBtn.setFont(font)
        self.StartBtn.setObjectName("StartBtn")
        self.gridLayout_2.addWidget(self.StartBtn, 7, 0, 1, 4)
        self.bib_start = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bib_start.setFont(font)
        self.bib_start.setObjectName("bib_start")
        self.gridLayout_2.addWidget(self.bib_start, 4, 3, 1, 1)
        self.MaxInterruptValue = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.MaxInterruptValue.setFont(font)
        self.MaxInterruptValue.setMaximum(100)
        self.MaxInterruptValue.setObjectName("MaxInterruptValue")
        self.gridLayout_2.addWidget(self.MaxInterruptValue, 2, 3, 1, 1)
        self.btn_settings = QtWidgets.QPushButton(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_settings.setFont(font)
        self.btn_settings.setObjectName("btn_settings")
        self.gridLayout_2.addWidget(self.btn_settings, 0, 0, 1, 4)
        self.dayduratiolabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.dayduratiolabel.setFont(font)
        self.dayduratiolabel.setObjectName("dayduratiolabel")
        self.gridLayout_2.addWidget(self.dayduratiolabel, 5, 0, 1, 1)
        self.WindMinLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.WindMinLabel.setFont(font)
        self.WindMinLabel.setObjectName("WindMinLabel")
        self.gridLayout_2.addWidget(self.WindMinLabel, 2, 0, 1, 1)
        self.OrientationLabel = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.OrientationLabel.setFont(font)
        self.OrientationLabel.setObjectName("OrientationLabel")
        self.gridLayout_2.addWidget(self.OrientationLabel, 4, 0, 1, 1)
        self.bib_startslider = QtWidgets.QSlider(WConfig)
        self.bib_startslider.setMinimum(1)
        self.bib_startslider.setMaximum(10)
        self.bib_startslider.setPageStep(2)
        self.bib_startslider.setOrientation(QtCore.Qt.Horizontal)
        self.bib_startslider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.bib_startslider.setTickInterval(1)
        self.bib_startslider.setObjectName("bib_startslider")
        self.gridLayout_2.addWidget(self.bib_startslider, 5, 2, 1, 1)
        self.randombtn = QtWidgets.QPushButton(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.randombtn.setFont(font)
        self.randombtn.setObjectName("randombtn")
        self.gridLayout_2.addWidget(self.randombtn, 5, 3, 1, 1)
        self.label = QtWidgets.QLabel(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 6, 0, 1, 1)
        self.groups_number_value = QtWidgets.QSpinBox(WConfig)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groups_number_value.setFont(font)
        self.groups_number_value.setObjectName("groups_number_value")
        self.gridLayout_2.addWidget(self.groups_number_value, 6, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(WConfig)
        QtCore.QMetaObject.connectSlotsByName(WConfig)

    def retranslateUi(self, WConfig):
        _translate = QtCore.QCoreApplication.translate
        WConfig.setWindowTitle(_translate("WConfig", "Form"))
        self.RevolLabel.setText(_translate("WConfig", "Revol"))
        self.day_1btn.setText(_translate("WConfig", "Day+1"))
        self.ContestList.setItemText(0, _translate("WConfig", "Training"))
        self.WindMaxLabel.setText(_translate("WConfig", "WindMax (m/s)"))
        self.bib_start_label.setText(_translate("WConfig", "BIB Starting"))
        self.MaxInterruptLabel.setText(_translate("WConfig", "Max Interrupt"))
        self.StartBtn.setText(_translate("WConfig", "Start"))
        self.btn_settings.setText(_translate("WConfig", "Race Management Settings"))
        self.dayduratiolabel.setText(_translate("WConfig", "Day duration"))
        self.WindMinLabel.setText(_translate("WConfig", "WindMin (m/s)"))
        self.OrientationLabel.setText(_translate("WConfig", "Orientation (°)"))
        self.randombtn.setText(_translate("WConfig", "Rand"))
        self.label.setText(_translate("WConfig", "Groups number"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WConfig = QtWidgets.QWidget()
    ui = Ui_WConfig()
    ui.setupUi(WConfig)
    WConfig.show()
    sys.exit(app.exec_())
