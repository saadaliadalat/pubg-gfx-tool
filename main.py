import ctypes
import sys
from datetime import datetime
from pathlib import Path
from os import environ

from PyQt5 import QtCore, QtWidgets
from src.constants import APP_NAME, APP_VERSION, FULL_APP_NAME
from src.ui.main_window import MainWindow

def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def suppress_qt_warnings():
    try:
        scale_factor = str(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
        if float(scale_factor) > 1.5:
            scale_factor = "1.5"
    except Exception:
        scale_factor = "1"

    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
    environ["QT_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = scale_factor

def main():
    if not is_admin():
        args = " ".join(f'"{arg}"' for arg in sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 1)
        sys.exit()

    ctypes.windll.kernel32.SetConsoleTitleW(FULL_APP_NAME)
    suppress_qt_warnings()

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open(Path.cwd() / "error.log", "a") as f:
            f.write(f"-------------------{datetime.now()}-------------------\n")
            f.write(f"CRASH_ERR: {e}\n")
