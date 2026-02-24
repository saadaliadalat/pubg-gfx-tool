import ctypes
import sys
from datetime import datetime
from pathlib import Path
from src.ui_functions import Window, QtWidgets
from PyQt5 import QtCore
from os import environ

APP_NAME = "EX Tool"
APP_VERSION = "v0.1"
FULL_APP_NAME = f"{APP_NAME} {APP_VERSION}"
ctypes.windll.kernel32.SetConsoleTitleW(FULL_APP_NAME)


def run_application():
    """
    Run the main GUI application.
    """
    ui = Window(APP_NAME, APP_VERSION)
    ui.show()
    app.exec_()


if __name__ == "__main__":
    print("[#] Starting the GUI app")

    def suppress_qt_warnings():
        DS = "1.5"

        scaleFactor = str(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
        if float(scaleFactor) > float(DS):
            scaleFactor = DS

        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
        environ["QT_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = scaleFactor


    suppress_qt_warnings()

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    try:
        app = QtWidgets.QApplication(sys.argv)
        run_application()
    except Exception as e:
        with open(f"{Path.cwd()}/error.log", "a") as f:
            f.write(f"-------------------{datetime.now()}-------------------\n")
            f.write(f"CRASH_ERR: {e}\n")
