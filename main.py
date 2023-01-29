import sys
import time

from PySide6.QtWidgets import *

from MainDialog import MainDialog
from SplashScreen import SplashScreen

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("styles/Obit.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    splashscreen = SplashScreen()
    splashscreen.splash.show()
    time.sleep(0.5)          # how long the splash screen should be displayed

    window = MainDialog()
    splashscreen.splash.finish(window)
    window.run()
    app.exec()
