import logging
import requests

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from core.get_proxies import get_proxies

class ThumbnailLoader(QThread):
    thumbnail_loaded = pyqtSignal(QPixmap)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url
        self.window = parent
        self._is_running = False

    def run(self):
        self._is_running = True
        try:
            response = requests.get(
                self.url,
                proxies=get_proxies(
                    self.window.proxy_type_setting,
                    self.window.proxy_host_name_setting,
                    self.window.proxy_port_setting,
                    self.window.proxy_login_setting,
                    self.window.proxy_password_setting
                )
            )
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            resized_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.thumbnail_loaded.emit(resized_pixmap)
        except Exception as e:
            logging.error(f"Error loading thumbnail: {str(e)}")
            self.thumbnail_loaded.emit(QPixmap())
        finally:
            self._is_running = False
            
    def is_running(self):
        return self._is_running