import requests
import logging

from PyQt5.QtCore import QThread, pyqtSignal

class UpdateChecker(QThread):
    update_checked = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/Youtube-Music-Desktop-Player/releases/latest")
            response.raise_for_status()
            
            data = response.json()
            item_version = data["name"]
            item_download = data.get("html_url")
        except requests.exceptions.RequestException as e:
            logging.error("UpdateChecker RequestException: " + str(e))
            return
        except Exception as e:
            logging.error("UpdateChecker UnexpectedError: " + str(e))
            return
        
        if response.status_code == 200:
            self.update_checked.emit(item_version, item_download)