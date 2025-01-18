import logging
import webbrowser
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog
from pywinstyles import apply_style
if TYPE_CHECKING:
    from core.main_window import MainWindow

from core.ui.ui_about_dialog import Ui_AboutDialog

class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.window:"MainWindow" = parent

        try:
            apply_style(self, "dark")
        except Exception as e:
            logging.error("Failed to apply dark style: " + str(e))

        self.setWindowTitle("About")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/about.png"))
        self.setFixedSize(self.size())

        self.BodyLabel_2.setText(self.window.version)

        self.PrimaryPushButton.clicked.connect(self.close)
        self.PushButton.clicked.connect(self.github)

        self.label.setPixmap(QPixmap(f"{self.window.icon_folder}/logo@128x128.png"))
        self.PushButton.setIcon(QIcon(f"{self.window.icon_folder}/github.png"))

    def github(self):
        webbrowser.open("https://github.com/deeffest/Youtube-Music-Desktop-Player")

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.window.show()
        event.accept()
