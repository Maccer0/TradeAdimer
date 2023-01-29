from PySide6.QtWidgets import *
from PySide6.QtSvgWidgets import *
from BaseWidget import BaseWidget
from ChartsCanvas import *
from CustomBoxMsg import *
from scipy.stats import norm


class ResultsDialog(BaseWidget):
    df = None
    window_h = 800
    window_w = 1200
    checkbox_arr = None

    def __init__(self, data, checkbox_arr, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.window_w, self.window_h)
        self.df = data
        self.checkbox_arr = checkbox_arr
        self.mainLabel.setText("RESULTS:")
        self.buttonSave = QPushButton("Save all")
        self.buttonSave.setMinimumWidth(50)
        self.buttonBack = QPushButton("Back")
        self.buttonBack.setMinimumWidth(50)
        self.buttonNextWidget = QPushButton(">")
        self.buttonNextWidget.setMinimumWidth(50)
        self.buttonPreviousWidget = QPushButton("<")
        self.buttonPreviousWidget.setMinimumWidth(50)
        self.layout_nav_btns = QHBoxLayout()
        self.stackedwidget = QStackedLayout()
        self.stackedwidget.setAlignment(Qt.AlignHCenter)
        if checkbox_arr["Plot chart"].checkState():
            self.candlestickchart = CandlestickWidget(self.df)
            self.pricechart = PriceChartWidget(self.df)
            self.closepricechart = ClosePriceChartWidget(self.df)
            self.stackedwidget.addWidget(self.candlestickchart)
            self.stackedwidget.addWidget(self.pricechart)
            self.stackedwidget.addWidget(self.closepricechart)
        if checkbox_arr["VIX"].checkState():
            self.volatilitychart = VolatilityChartWidget(self.df)
            self.stackedwidget.addWidget(self.volatilitychart)
        if not (not checkbox_arr["VAR"].checkState() and not checkbox_arr["CVAR"].checkState() and not checkbox_arr[
            "Beta"].checkState() and not checkbox_arr["Mean"].checkState()) \
                or checkbox_arr["Standard Deviation"].checkState():  # VAR CVAR VIX BETA
            self.labelwidget = QWidget()
            self.labelwidget.setWindowFlag(Qt.FramelessWindowHint)
            self.labellayout = QHBoxLayout()
            self.labelwidget.setLayout(self.labellayout)
            self.coeflabel = QLabel("")
            self.coeflabel.setStyleSheet("font-size:20px;color:#fce595")
            if checkbox_arr["VAR"].checkState():
                self.coeflabel.setText(self.coeflabel.text() + self.calculateVAR())
            if checkbox_arr["Beta"].checkState():
                self.coeflabel.setText(self.coeflabel.text() + self.calculateBeta())
            if checkbox_arr["Mean"].checkState():
                self.coeflabel.setText(self.coeflabel.text() + self.calculateMean())
            if checkbox_arr["Standard Deviation"].checkState():
                self.coeflabel.setText(self.coeflabel.text() + self.calculateDeviation())
            self.labellayout.addWidget(self.coeflabel, alignment=Qt.AlignCenter)
            self.stonkswidget = QSvgWidget("styles/Stonks_emoji.svg")
            self.stonkswidget.setFixedSize(self.window_w / 2 - 100, self.window_h / 2)
            self.labellayout.addWidget(self.stonkswidget, alignment=Qt.AlignCenter)
            self.stackedwidget.addWidget(self.labelwidget)
        self.layout_nav_btns.addStretch()
        self.layout_nav_btns.addWidget(self.buttonPreviousWidget)
        self.layout_nav_btns.addWidget(self.buttonNextWidget)
        self.layout_nav_btns.addStretch()
        self.layout_nav_btns.addWidget(self.buttonBack)
        self.layout_nav_btns.addWidget(self.buttonSave)
        self.mainLayout.addLayout(self.stackedwidget)
        self.mainLayout.addLayout(self.layout_nav_btns)
        self.buttonSave.clicked.connect(self.saveOutputToFile)
        self.buttonNextWidget.clicked.connect(self.setNextWidget)
        self.buttonPreviousWidget.clicked.connect(self.setPrevWidget)
        self.setLayout(self.mainLayout)

    def calculateVAR(self):
        # VAR/CVAR
        close_mean = self.df["<CLOSE>"].mean()
        standard_deviation_close = self.df["<CLOSE>"].std()
        var_90 = float(norm.ppf(1 - 0.9, close_mean, standard_deviation_close))
        var_96 = float(norm.ppf(1 - 0.95, close_mean, standard_deviation_close))
        var_99 = float(norm.ppf(1 - 0.99, close_mean, standard_deviation_close))
        if self.checkbox_arr["CVAR"].checkState():
            x = norm.expect(lambda x: x, loc=close_mean, scale=standard_deviation_close, lb=var_90)
            cvar_90 = (1 / (1 - 0.90)) * x
            y = norm.expect(lambda y: y, loc=close_mean, scale=standard_deviation_close, lb=var_96)
            cvar_95 = (1 / (1 - 0.95)) * y
            z = norm.expect(lambda z: z, loc=close_mean, scale=standard_deviation_close, lb=var_99)
            cvar_99 = (1 / (1 - 0.99)) * z
            return f"\nVaR 90%:\t{var_90:.3f}" \
                   f"\nVaR 95%:\t{var_96:.3f}" \
                   f"\nVaR 99%:\t{var_99:.3f}" \
                   f"\n\nCVaR 90%:\t{cvar_90:.3f}" \
                   f"\nCVaR 95%:\t{cvar_95:.3f}" \
                   f"\nCVaR 99%:\t{cvar_99:.3f}\n"
        return f"\nVaR 90%:\t{var_90:.3f}" \
               f"\nVaR 95%:\t{var_96:.3f}" \
               f"\nVaR 99%:\t{var_99:.3f}\n"
        # VAR/CVAR

    def calculateBeta(self):
        # BETA
        covariance = self.df["<HIGH>"].iloc[0] / self.df["<HIGH>"].iloc[-1]
        variance = 10
        beta = covariance / variance
        return f"\nBeta (calculated with 10% benchmark):" \
               f"\n{beta:.3f}\n"
        # BETA

    def calculateMean(self):
        return f"\nMean of close price:" \
               f"\n{self.df['<CLOSE>'].mean():.3f}\n"

    def calculateDeviation(self):
        return f"\nStandard deviation of close price:" \
               f"\n{self.df['<CLOSE>'].std():.3f}\n"

    def saveOutputToFile(self):
        folderpath = QFileDialog.getExistingDirectory()
        if folderpath != "":
            if self.checkbox_arr["Plot chart"].checkState():
                self.candlestickchart.chart.saveplot(folderpath)
                self.pricechart.chart.saveplot(folderpath)
                self.closepricechart.chart.saveplot(folderpath)
            if self.checkbox_arr["VIX"].checkState():
                self.volatilitychart.chart.saveplot(folderpath)
            if self.checkbox_arr["VAR"].checkState() or self.checkbox_arr["CVAR"].checkState() or self.checkbox_arr[
                "Beta"].checkState() or self.checkbox_arr["Mean"].checkState() or self.checkbox_arr[
                "Standard Deviation"].checkState():
                with open(folderpath + "\\coef.txt", "w") as f:
                    f.write(f"Results for {self.df['<TICKER>'].values[0]}\n")
                    if self.checkbox_arr["VAR"].checkState():
                        f.write(self.calculateVAR())
                    if self.checkbox_arr["Beta"].checkState():
                        f.write(self.calculateBeta())
                    if self.checkbox_arr["Mean"].checkState():
                        f.write(self.calculateMean())
                    if self.checkbox_arr["Standard Deviation"].checkState():
                        f.write(self.calculateDeviation())
                    f.close()
            self.openFolder(folderpath)
            y = folderpath.split('/')

            # MessageBox("Data saved to:\n" + y[-1])  # last folder in folderpath
            self.showMessage("Data saved to:\n" + y[-1], 0.9)

    def setNextWidget(self):  # switch between output data
        i = self.stackedwidget.currentIndex()
        if i < self.stackedwidget.count():
            self.stackedwidget.setCurrentIndex(i + 1)
        if i == self.stackedwidget.count() - 1:
            self.stackedwidget.setCurrentIndex(0)

    def setPrevWidget(self):  # switch between output data
        i = self.stackedwidget.currentIndex()
        if i > 0:
            self.stackedwidget.setCurrentIndex(i - 1)
        if i == 0:
            self.stackedwidget.setCurrentIndex(self.stackedwidget.count() - 1)

    def closeFigure(self):
        plt.close('all')
