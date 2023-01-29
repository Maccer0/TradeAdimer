import os
import platform
import subprocess

from PySide6.QtCore import *
from PySide6.QtWidgets import *

from CustomBoxMsg import MessageBox


class BaseWidget(QWidget):

    def __init__(self, parent=None):
        super(BaseWidget, self).__init__(parent)
        self.currSystem = platform.system()
        self.dragPos = None
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.buttonClose = QPushButton("X")
        self.buttonClose.setFixedSize(25, 25)
        self.buttonClose.setStyleSheet("QPushButton::hover{background-color : red;}")
        self.buttonMinimize = QPushButton("_")
        self.buttonMinimize.setFixedSize(25, 25)
        self.buttonHelp = QPushButton("?")
        self.buttonHelp.setFixedSize(25, 25)
        self.mainLabel = QLabel("")
        self.barLayout = QHBoxLayout()
        self.barLayout.addWidget(self.mainLabel, 0, alignment=Qt.AlignCenter)
        self.mainLayout = QVBoxLayout()
        self.barLayout.addWidget(self.buttonHelp)
        self.barLayout.addWidget(self.buttonMinimize)
        self.barLayout.addWidget(self.buttonClose)
        self.mainLayout.addLayout(self.barLayout)
        self.buttonMinimize.clicked.connect(self.showMinimized)
        self.buttonClose.clicked.connect(self.close)
        self.buttonHelp.clicked.connect(self.showHelp)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()
        event.accept()

    def showHelp(self):
        helppath = "Docs/FAQ.pdf"
        apppath = os.path.dirname(__file__)
        abspath = os.path.join(apppath, helppath)

        if self.currSystem == 'Windows':  # Windows
            os.startfile(abspath)

        elif self.currSystem == 'Darwin':  # macOS
            subprocess.call(('open', abspath))
        else:  # linux
            subprocess.call(('xdg-open', abspath))

    def openFolder(self, folder_path: str):
        if self.currSystem == 'Windows':  # Windows
            os.startfile(os.path.realpath(folder_path))

        elif self.currSystem == 'Darwin':  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # linux
            subprocess.Popen(["xdg-open", folder_path])

    def showMessage(self, msg, val: float):
        self.setWindowOpacity(val)  # background opacity effect
        MessageBox(msg)
        self.setWindowOpacity(1.0)
