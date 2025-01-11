import logging
import requests

from PyQt5.QtCore import QThread, pyqtSignal

class UpdateChecker(QThread):
    update_checked = pyqtSignal(str, str, str, str)
    def __init__(self):
        super().__init__()

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