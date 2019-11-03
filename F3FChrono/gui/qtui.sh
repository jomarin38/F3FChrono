#!/bin/bash
echo "compile qt5 ui file to python"
python3 -m PyQt5.uic.pyuic -x MainUi.ui -o MainUi_UI.py
python3 -m PyQt5.uic.pyuic -x WTop.ui -o WTop_UI.py
python3 -m PyQt5.uic.pyuic -x WBottom.ui -o WBottom_UI.py
python3 -m PyQt5.uic.pyuic -x WHome.ui -o WHome_ui.py
python3 -m PyQt5.uic.pyuic -x WChrono.ui -o WChrono_ui.py
