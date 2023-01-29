import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mplfinance.original_flavor import candlestick_ohlc

plt.style.use("dark_background")


class CandlestickWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.plot_layout = QVBoxLayout(self)
        self.chart = CandlestickCanvas(self, data)
        self.navi_toolbar = NavigationToolbar(self.chart, self)
        self.plot_layout.addWidget(self.chart)
        self.plot_layout.addWidget(self.navi_toolbar)


class CandlestickCanvas(FigureCanvas):
    def __init__(self, parent, data):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=120)
        self.fig.set_facecolor("#2d2e3d")
        self.fig.tight_layout()
        super().__init__(self.fig)
        self.setParent(parent)
        ohlc = data.loc[:, ['<DATE>', "<OPEN>", '<HIGH>', '<LOW>', '<CLOSE>']]
        ohlc['<DATE>'] = pd.to_datetime(ohlc["<DATE>"], format='%Y%m%d')
        ohlc['<DATE>'] = ohlc['<DATE>'].apply(mpl_dates.date2num)
        ohlc = ohlc.astype(float)

        candlestick_ohlc(self.ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price')
        date_format = mpl_dates.DateFormatter('%Y-%m-%d')
        self.ax.xaxis.set_major_formatter(date_format)
        self.fig.autofmt_xdate()
        ohlc['SMA5'] = ohlc['<CLOSE>'].rolling(5).mean()
        self.ax.plot(ohlc['<DATE>'], ohlc['SMA5'], color='blue', label='SMA5')
        self.fig.suptitle(f'Candlestick Chart of {data["<TICKER>"].values[0]} with SMA5')

    def saveplot(self, folderpath):
        self.fig.savefig(folderpath + "\\candlestick.png", dpi=1500)


class PriceChartWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.plot_layout = QVBoxLayout(self)
        self.chart = PriceChartCanvas(self, data)
        self.navi_toolbar = NavigationToolbar(self.chart, self)
        self.plot_layout.addWidget(self.chart)
        self.plot_layout.addWidget(self.navi_toolbar)


class PriceChartCanvas(FigureCanvas):
    def __init__(self, parent, data):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=120)
        self.fig.set_facecolor("#2d2e3d")
        self.fig.tight_layout()
        super().__init__(self.fig)
        self.setParent(parent)
        self.fig.suptitle(f'Open Price Chart of {data["<TICKER>"].values[0]}')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price')
        plt.plot(data["<DATE>"], data["<OPEN>"])
        date_format = mpl_dates.DateFormatter('%Y-%m-%d')
        self.ax.xaxis.set_major_formatter(date_format)
        self.fig.autofmt_xdate()

    def saveplot(self, folderpath):
        self.fig.savefig(folderpath + "\\openprice.png", dpi=1500)


class ClosePriceChartWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.plot_layout = QVBoxLayout(self)
        self.chart = ClosePriceChartCanvas(self, data)
        self.navi_toolbar = NavigationToolbar(self.chart, self)
        self.plot_layout.addWidget(self.chart)
        self.plot_layout.addWidget(self.navi_toolbar)


class ClosePriceChartCanvas(FigureCanvas):
    def __init__(self, parent, data):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=120)
        self.fig.set_facecolor("#2d2e3d")
        self.fig.tight_layout()
        super().__init__(self.fig)
        self.setParent(parent)
        self.fig.suptitle(f'Close Price Chart of {data["<TICKER>"].values[0]}')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price')
        plt.plot(data["<DATE>"], data["<CLOSE>"])
        date_format = mpl_dates.DateFormatter('%Y-%m-%d')
        self.ax.xaxis.set_major_formatter(date_format)
        self.fig.autofmt_xdate()

    def saveplot(self, folderpath):
        self.fig.savefig(folderpath + "\\closeprice.png", dpi=1500)


class VolatilityChartWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.plot_layout = QVBoxLayout(self)
        self.chart = VolatilityCanvas(self, data)
        self.navi_toolbar = NavigationToolbar(self.chart, self)
        self.plot_layout.addWidget(self.chart)
        self.plot_layout.addWidget(self.navi_toolbar)


class VolatilityCanvas(FigureCanvas):
    def __init__(self, parent, data):
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=120)
        self.fig.set_facecolor("#2d2e3d")
        self.fig.tight_layout()
        super().__init__(self.fig)
        self.setParent(parent)
        self.fig.suptitle(f'Volatility Chart of {data["<TICKER>"].values[0]}')
        self.ax.set_xlabel('Date')
        plt.plot(data["<DATE>"], data["<VOL>"])
        date_format = mpl_dates.DateFormatter('%Y-%m-%d')
        self.ax.xaxis.set_major_formatter(date_format)
        self.fig.autofmt_xdate()

    def saveplot(self, folderpath):
        self.fig.savefig(folderpath + "\\volatility.png", dpi=1500)
