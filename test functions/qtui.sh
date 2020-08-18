#!/bin/bash
echo "compile qt5 ui file to python"
python3 -m PyQt5.uic.pyuic -x test.ui -o test_UI.py
