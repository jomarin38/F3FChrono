from PyQt5 import QtWidgets
from F3FChrono.chrono.Sound import *
from test.test_UI import Ui_MainWindow
import wave

class testSound(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainWindow)
        self.pathname = os.path.dirname(os.path.realpath('testfile.py'))
        self.sound = None
        self.__loadsoundClass()


        self.ui.button_time.clicked.connect(self.time_event)
        self.ui.button_pilot.clicked.connect(self.pilot_event)
        self.ui.buttonconvert.clicked.connect(self.convert)
        self.ui.button_base.clicked.connect(self.base)
        self.ui.button_elapsedtime.clicked.connect(self.elapsed_time)
        self.ui.button_lowvoltage.clicked.connect(self.sound.signal_lowVoltage.emit)
        self.ui.button_reload.clicked.connect(self.reload)
        self.ui.comboBox_language.currentIndexChanged.connect(self.reload)
        self.ui.button_instart.clicked.connect(self.sound.signal_entry.emit)
        self.ui.button_penalty.clicked.connect(self.sound.signal_penalty.emit)
        self.ui.button_quit.clicked.connect(self.quit)
        self.mainWindow.show()


    def elapsed_time(self):
        print("elapsed time")
        self.sound.signal_elapsedTime.emit(self.ui.elapsed_time.value())

    def base(self):
        print("base")
        self.sound.signal_base.emit(self.ui.base.value())

    def time_event(self):
        print("time")
        self.sound.signal_time.emit(self.ui.finaltime.value())

    def pilot_event(self):
        print("pilot")
        self.sound.signal_pilotname.emit(self.ui.pilotnumber.value())

    def reload(self):
        print("reload")
        self.__loadsoundClass()

    def convert(self):
        print("convert")
        try:
            pathname = os.path.normpath(self.pathname + '/../')
            language = self.ui.comboBox_language.currentText()
            for i in range(0, 101):
                file = wave.Wave_read(os.path.join(pathname, 'Languages', language, '{:04d}.wav'.format(i)))
                file1 = wave.Wave_write(os.path.join(pathname, 'Languages', language, 'work', str(i)+'.wav'))

                file1.setparams(file.getparams())
                file1.writeframes(file.readframes(file.getnframes()))
                file1.close()
                file.close()

        except TypeError as e:
            print("wavefile : ", e)

    def __loadsoundClass(self):
        if self.sound is not None:
            del(self.sound)
        language = self.ui.comboBox_language.currentText()
        self.sound = chronoQSound(os.path.normpath(self.pathname + '/../'), language, True)

    def quit(self):
        self.sound.stop_all()
        exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = testSound()
    sys.exit(app.exec_())



