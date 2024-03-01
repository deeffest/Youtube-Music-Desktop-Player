from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import os

class ConfirmDlg(QDialog):
    def __init__(
        self,
        name,
        current_dir,
        parent=None
    ):
        super().__init__(parent)

        self.window = parent
        self.name = name
        self.current_dir = current_dir

        loadUi(
            f'{self.current_dir}/core/ui/confirm_dialog.ui', self
        )

        self._init_window()

    def setText(self, text):
        self.BodyLabel.setText(text)
        self._init_connect()
    
    def _init_connect(self):
        self.PushButton.clicked.connect(self.accept)
        self.PushButton_2.clicked.connect(self.close)

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(400, 138)
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )