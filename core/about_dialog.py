import logging
import platform
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt, PYQT_VERSION_STR
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog
from core.ui.ui_about_dialog import Ui_AboutDialog
from core.helpers import open_url

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
            from pywinstyles import apply_style  # type: ignore

            try:
                apply_style(self, "dark")
            except Exception as e:
                logging.error(f"Failed to apply dark style: + {str(e)}")

        self.setupUi(self)
        self.setWindowTitle("About")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/about-filled-border.png"))
        self.setFixedSize(self.size())

    def configure_ui_elements(self):
        self.PrimaryPushButton.clicked.connect(self.close)
        self.PushButton.clicked.connect(
            lambda: open_url(
                f"https://github.com/{self.window.app_author}/{self.window.name}"
            )
        )
        self.HyperlinkLabel.clicked.connect(lambda: open_url("https://icons8.com"))

        self.BodyLabel_2.setText(self.window.version)
        self.label_3.setText(f"PyQt5: {PYQT_VERSION_STR}")
        self.label_5.setText(f"Python: {platform.python_version()}")
        os_info = (
            platform.freedesktop_os_release() if platform.system() == "Linux" else {}
        )
        os_name = (
            f"{os_info.get('NAME')} {os_info.get('VERSION_ID')}"
            if os_info
            else f"{platform.system()} {platform.release()}"
        )
        self.label_7.setText(f"OS: {os_name}")
        self.label.setPixmap(QPixmap(f"{self.window.icon_folder}/logo.png"))
        self.PushButton.setIcon(QIcon(f"{self.window.icon_folder}/github.png"))

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Escape:
            self.close()
        key_event.accept()

    def closeEvent(self, event):
        self.window.show()
        event.accept()
