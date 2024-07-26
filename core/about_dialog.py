import pywinstyles
import webbrowser

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = parent

        self.load_ui()
        self.setup_connect()
        self.setup_content()

    def setup_content(self):
        self.BodyLabel_2.setText(f"Version: {self.window.version}")

    def setup_connect(self):
        self.PrimaryPushButton.clicked.connect(self.close)
        self.PushButton.clicked.connect(self.go_to_github)

    def go_to_github(self):
        webbrowser.open("https://github.com/deeffest/Youtube-Music-Desktop-Player")

    def load_ui(self):
        loadUi(f'{self.window.current_dir}/core/ui/about_dialog.ui', self)
        pywinstyles.apply_style(self, "dark")
        self.setWindowTitle("About app")
        self.setFixedSize(self.size())
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/about-red.png"))

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.window.show()
        event.accept()