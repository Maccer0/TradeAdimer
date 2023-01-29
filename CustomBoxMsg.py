from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QLabel, QDialogButtonBox


class MessageBox(QMessageBox):
    def __init__(self, msg, parent=None, ):
        super().__init__(parent)

        grid_layout = self.layout()
        self.setWindowFlag(Qt.FramelessWindowHint)
        qt_msgboxex_icon_label = self.findChild(QLabel, "qt_msgboxex_icon_label")
        qt_msgboxex_icon_label.deleteLater()
        qt_msgbox_label = self.findChild(QLabel, "qt_msgbox_label")
        self.setStyleSheet("QLabel{min-width: 200px;min-height: 60px} QMessageBox{border: 1px groove #ff9900;}");
        qt_msgbox_label.setAlignment(Qt.AlignCenter)
        grid_layout.removeWidget(qt_msgbox_label)

        qt_msgbox_buttonbox = self.findChild(QDialogButtonBox, "qt_msgbox_buttonbox")
        grid_layout.removeWidget(qt_msgbox_buttonbox)

        grid_layout.addWidget(qt_msgbox_label, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(qt_msgbox_buttonbox, 1, 0, alignment=Qt.AlignCenter)

        self.setText(msg)

        self.exec()

        # if (self==qt_msgbox_buttonbox):
        #     self.setOpacity(1)
