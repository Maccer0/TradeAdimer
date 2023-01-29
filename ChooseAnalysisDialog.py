from PySide6.QtCore import *
from PySide6.QtWidgets import *

from BaseWidget import BaseWidget


class ChooseAnalysisDialog(BaseWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 400)
        self.mainLabel.setText("ANALYSIS CHOICE")
        self.buttonBack = QPushButton("Back")
        self.buttonNext = QPushButton("Next")
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.buttonBack)
        self.buttonLayout.addWidget(self.buttonNext)
        self.titles = ["Plot chart", "VAR", "CVAR", "VIX", "Beta", "Mean", "Standard Deviation"]
        self.checkboxes = {}
        self.infoLabel = QLabel("Choose analysis methods: ")
        self.infoLabel.setFixedHeight(20)
        self.infoLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addLayout(self.barLayout)
        self.mainLayout.addWidget(self.infoLabel)
        for i in self.titles:
            x = QCheckBox(i, self)
            x.setStyleSheet("color:#c1c1c1")
            self.checkboxes[i] = x
            self.mainLayout.addWidget(x)
        self.mainLayout.addLayout(self.buttonLayout)
        self.setLayout(self.mainLayout)
