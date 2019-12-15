#!/bin/bash
echo "compile qt5 ui file to python"
python3 -m PyQt5.uic.pyuic -x MainUi.ui -o MainUi_UI.py
python3 -m PyQt5.uic.pyuic -x WPilot.ui -o WPilot_UI.py
python3 -m PyQt5.uic.pyuic -x WWind.ui -o WWind_UI.py
python3 -m PyQt5.uic.pyuic -x WConfig.ui -o WConfig_ui.py
python3 -m PyQt5.uic.pyuic -x WChrono.ui -o WChrono_ui.py
python3 -m PyQt5.uic.pyuic -x WChronoBtn.ui -o WChronoBtn_ui.py