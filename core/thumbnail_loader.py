import requests
import logging

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

class ThumbnailLoader(QThread):
    thumbnail_loaded = pyqtSignal(QPixmap)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self._is_running = False

    def run(self):
        self._is_running = True
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.thumbnail_loaded.emit(pixmap)
        except requests.exceptions.RequestException as e:
            logging.error("ThumbnailLoader RequestException: " + str(e))
            self.thumbnail_loaded.emit(QPixmap())
        except Exception as e:
            logging.error("ThumbnailLoader UnexpectedError: " + str(e))
        finally:
            self._is_running = False
            
    def is_running(self):
        return self._is_running