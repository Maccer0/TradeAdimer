from os.path import exists

from PySide6.QtWidgets import *

from BaseWidget import BaseWidget


class ChooseFileDialog(BaseWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = ""
        self.setFixedSize(300, 150)
        self.editInput = QLineEdit()
        self.editInput.setReadOnly(True)
        self.editInput.setPlaceholderText("Open csv file")
        if exists("lastfile.txt"):
            with open("lastfile.txt", "r") as f:
                self.editInput.setText(f.readline())
        self.buttonOpen = QPushButton("Open file")
        self.buttonNext = QPushButton("Next")
        self.layouth = QHBoxLayout()
        self.mainLabel.setText("Welcome!")

        self.layouth.addWidget(self.editInput)
        self.layouth.addWidget(self.buttonOpen)
        self.mainLayout.addLayout(self.barLayout)
        self.mainLayout.addLayout(self.layouth)
        self.mainLayout.addWidget(self.buttonNext)
        self.setLayout(self.mainLayout)
