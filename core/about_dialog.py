from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

class AboutDlg(QDialog):
    def __init__(
        self,
        current_dir,
        name,
        settings,
        version,
        parent=None
    ):
        super().__init__(parent)

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings
        self.version = version

        loadUi(
            f'{self.current_dir}/core/ui/about_dialog.ui', self
        )

        self._init_window()
        self._init_content()
        self._init_connect()

    def _init_content(self):
        self.BodyLabel_2.setText(self.version)
    
    def _init_connect(self):
        self.PushButton.clicked.connect(self.close)
        self.PushButton_2.clicked.connect(self.open_changelog)

    def open_changelog(self):
        self.close()
        self.window.open_changelog()

    def _init_window(self):
        self.setWindowTitle("About")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(
            QIcon(f"{self.current_dir}/resources/icons/info_white_24dp.svg"
        ))