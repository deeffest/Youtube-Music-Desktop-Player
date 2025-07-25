import logging
import platform
import webbrowser
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog

from core.ui.ui_about_dialog import Ui_AboutDialog

if TYPE_CHECKING:
    from core.main_window import MainWindow


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.configure_window()
        self.configure_ui_elements()

    def configure_window(self):
        if platform.system() == "Windows":
            from pywinstyles import apply_style

            try:
                apply_style(self, "dark")
            except Exception as e:
                logging.error(f"Failed to apply dark style: + {str(e)}")

        self.setupUi(self)
        self.setWindowTitle("About")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/about.png"))
        self.setFixedSize(self.size())

    def configure_ui_elements(self):
        self.PrimaryPushButton.clicked.connect(self.close)
        self.PushButton.clicked.connect(self.github)

        self.BodyLabel_2.setText(self.window.version)
        self.label.setPixmap(QPixmap(f"{self.window.icon_folder}/logo.png"))
        self.PushButton.setIcon(QIcon(f"{self.window.icon_folder}/github.png"))

    def github(self):
        webbrowser.open(
            f"https://github.com/{self.window.app_author}/{self.window.name}"
        )

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Escape:
            self.close()
        key_event.accept()

    def closeEvent(self, event):
        self.window.show()
        event.accept()
