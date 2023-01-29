import pandas as pd
from PySide6.QtWidgets import *

from ChooseAnalysisDialog import ChooseAnalysisDialog
from ChooseFileDialog import ChooseFileDialog
from ResultsDialog import ResultsDialog


class MainDialog(QMainWindow):
    filename = ""
    df = None

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.testLayout = None
        self.choicedialog = None
        self.filedialog = None
        self.stackedLayout = None
        self.resultsdialog = None

    def run(self):
        self.stackedLayout = QStackedLayout()
        self.filedialog = ChooseFileDialog()
        self.choicedialog = ChooseAnalysisDialog()
        self.testLayout = QVBoxLayout()
        self.stackedLayout.addWidget(self.filedialog)
        self.stackedLayout.addWidget(self.choicedialog)
        self.testLayout.addLayout(self.stackedLayout)
        self.setLayout(self.testLayout)
        self.filedialog.buttonNext.clicked.connect(self.loadfile)
        self.choicedialog.buttonBack.clicked.connect(self.setPrevWindow)
        self.choicedialog.buttonNext.clicked.connect(self.showResultsWindow)
        self.filedialog.buttonOpen.clicked.connect(self.openfile)
        self.filename = self.filedialog.editInput.text()

    def loadfile(self):
        if self.validateFile():
            self.setNextWindow()
        else:
            self.filedialog.showMessage("Invalid file!\nTry again.", 0.6)

    def openfile(self):
        self.filename, _filter = QFileDialog.getOpenFileName(self, "Open file", "C://", "(*.csv *.txt *.cpp)")
        with open("lastfile.txt", "w") as f:
            f.write(self.filename)
        self.filedialog.editInput.setText(self.filename)

    def showResultsWindow(self):
        for x in self.choicedialog.checkboxes.values():
            if x.checkState():
                self.resultsdialog = ResultsDialog(self.df, self.choicedialog.checkboxes)
                self.stackedLayout.addWidget(self.resultsdialog)
                self.resultsdialog.buttonBack.clicked.connect(self.setPrevWindowResults)
                self.setNextWindow()

                return
        self.choicedialog.showMessage("Check AT LEAST one\n checkbox!", 0.6)

    def setPrevWindowResults(self):         # method to go back from results dialog
        self.resultsdialog.closeFigure()
        self.stackedLayout.removeWidget(self.resultsdialog)
        self.resultsdialog = None

    def setNextWindow(self):
        i = self.stackedLayout.currentIndex()
        if i < self.stackedLayout.count():
            self.stackedLayout.setCurrentIndex(i + 1)

    def setPrevWindow(self):
        i = self.stackedLayout.currentIndex()
        if i > 0:
            self.stackedLayout.setCurrentIndex(i - 1)

    def validateFile(self):
        if self.filename:
            try:
                self.df = pd.read_csv(self.filename)
                self.df['<DATE>'] = pd.to_datetime(self.df["<DATE>"], format='%Y%m%d')
                return True
            except:
                return False
