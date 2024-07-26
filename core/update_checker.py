import requests

from PyQt5.QtCore import QThread, pyqtSignal

class UpdateChecker(QThread):
    update_checked = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/Youtube-Music-Desktop-Player/releases/latest")
            item_version = response.json()["name"]
            item_download = response.json().get("html_url")
            data = response.json()
            item_notes = data.get("body")
        except Exception as e:
            return
        if response.status_code == 200:
            self.update_checked.emit(item_version, item_download, item_notes)