#!/bin/bash
echo "compile qt5 ui file to python"
python3 -m PyQt5.uic.pyuic -x MainUi.ui -o MainUi_UI.py
python3 -m PyQt5.uic.pyuic -x WPilot.ui -o WPilot_ui.py
python3 -m PyQt5.uic.pyuic -x WWind.ui -o WWind_ui.py
python3 -m PyQt5.uic.pyuic -x WConfig.ui -o WConfig_ui.py
python3 -m PyQt5.uic.pyuic -x WChrono.ui -o WChrono_ui.py
python3 -m PyQt5.uic.pyuic -x WChronoTraining.ui -o WChronoTraining_ui.py
python3 -m PyQt5.uic.pyuic -x WChronoBtn.ui -o WChronoBtn_ui.py
python3 -m PyQt5.uic.pyuic -x WTrainingBtn.ui -o WTrainingBtn_ui.py
python3 -m PyQt5.uic.pyuic -x simulate_base.ui -o simulate_base_ui.py
python3 -m PyQt5.uic.pyuic -x WSettings.ui -o WSettings_ui.py
python3 -m PyQt5.uic.pyuic -x WSettingsSound.ui -o WSettingsSound_ui.py
python3 -m PyQt5.uic.pyuic -x WSettingsBase.ui -o WSettingsBase_ui.py
python3 -m PyQt5.uic.pyuic -x WSettingsBase_item.ui -o WSettingsBase_item_ui.py
python3 -m PyQt5.uic.pyuic -x WSettingsAdvanced.ui -o WSettingsAdvanced_ui.py
python3 -m PyQt5.uic.pyuic -x WPicamPair.ui -o WPicamPair_ui.py
