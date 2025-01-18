import logging
import requests
from typing import TYPE_CHECKING

from PyQt5.QtCore import QThread, pyqtSignal
if TYPE_CHECKING:
    from main_window import MainWindow


class UpdateChecker(QThread):
    update_checked = pyqtSignal(str, str, str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window:"MainWindow" = parent

    def run(self):
        try:
            response = requests.get("https://api.github.com/repos/deeffest/Youtube-Music-Desktop-Player/releases/latest")
            response.raise_for_status()
            
            data = response.json()
            last_version = data["tag_name"]
            title = data.get("name")
            whats_new = data.get("body")
            last_release_url = data.get("html_url")
        except Exception as e:
            logging.error(f"Failed to check for updates: {str(e)}")
            return
            
        if response.status_code == 200:
            self.update_checked.emit(last_version, title, whats_new, last_release_url)
