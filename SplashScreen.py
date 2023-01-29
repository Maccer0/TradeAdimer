from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap("styles/TradeAdimer_splash.png")
        self.splash = QSplashScreen(self.pixmap)
