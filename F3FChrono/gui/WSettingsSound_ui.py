# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WSettingsSound.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WSettingsSound(object):
    def setupUi(self, WSettingsSound):
        WSettingsSound.setObjectName("WSettingsSound")
        WSettingsSound.resize(480, 270)
        self.gridLayout = QtWidgets.QGridLayout(WSettingsSound)
        self.gridLayout.setContentsMargins(-1, 3, -1, 3)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(WSettingsSound)
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
        self.sound = QtWidgets.QCheckBox(WSettingsSound)
        self.sound.setObjectName("sound")
        self.gridLayout_2.addWidget(self.sound, 0, 0, 1, 1)
        self.voice = QtWidgets.QCheckBox(WSettingsSound)
        self.voice.setObjectName("voice")
        self.gridLayout_2.addWidget(self.voice, 1, 0, 1, 1)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.noisevolume = QtWidgets.QDoubleSpinBox(WSettingsSound)
        self.noisevolume.setDecimals(3)
        self.noisevolume.setProperty("value", 0.005)
        self.noisevolume.setObjectName("noisevolume")
        self.horizontalLayout_24.addWidget(self.noisevolume)
        self.label_22 = QtWidgets.QLabel(WSettingsSound)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_24.addWidget(self.label_22)
        self.gridLayout_2.addLayout(self.horizontalLayout_24, 4, 1, 1, 1)
        self.buzzer = QtWidgets.QCheckBox(WSettingsSound)
        self.buzzer.setObjectName("buzzer")
        self.gridLayout_2.addWidget(self.buzzer, 2, 0, 1, 1)
        self.noiseSound = QtWidgets.QCheckBox(WSettingsSound)
        self.noiseSound.setObjectName("noiseSound")
        self.gridLayout_2.addWidget(self.noiseSound, 4, 0, 1, 1)
        self.buzzernext = QtWidgets.QCheckBox(WSettingsSound)
        self.buzzernext.setObjectName("buzzernext")
        self.gridLayout_2.addWidget(self.buzzernext, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_back = QtWidgets.QPushButton(WSettingsSound)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_back.setFont(font)
        self.btn_back.setObjectName("btn_back")
        self.horizontalLayout.addWidget(self.btn_back)
        self.btn_cancel = QtWidgets.QPushButton(WSettingsSound)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.btn_valid = QtWidgets.QPushButton(WSettingsSound)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_valid.setFont(font)
        self.btn_valid.setObjectName("btn_valid")
        self.horizontalLayout.addWidget(self.btn_valid)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(WSettingsSound)
        QtCore.QMetaObject.connectSlotsByName(WSettingsSound)

    def retranslateUi(self, WSettingsSound):
        _translate = QtCore.QCoreApplication.translate
        WSettingsSound.setWindowTitle(_translate("WSettingsSound", "Form"))
        self.label.setText(_translate("WSettingsSound", "Sound Settings"))
        self.sound.setText(_translate("WSettingsSound", "Sound"))
        self.voice.setText(_translate("WSettingsSound", "Voice"))
        self.label_22.setText(_translate("WSettingsSound", "Noise Volume"))
        self.buzzer.setText(_translate("WSettingsSound", "Buzzer"))
        self.noiseSound.setText(_translate("WSettingsSound", "Noise Sound"))
        self.buzzernext.setText(_translate("WSettingsSound", "Buzzer Next button"))
        self.btn_back.setText(_translate("WSettingsSound", "Back to Settings"))
        self.btn_cancel.setText(_translate("WSettingsSound", "Cancel"))
        self.btn_valid.setText(_translate("WSettingsSound", "Valid"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WSettingsSound = QtWidgets.QWidget()
    ui = Ui_WSettingsSound()
    ui.setupUi(WSettingsSound)
    WSettingsSound.show()
    sys.exit(app.exec_())
