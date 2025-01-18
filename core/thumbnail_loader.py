import logging

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from core.helpers import get_proxies

class ThumbnailLoader(QThread):
    thumbnail_loaded = pyqtSignal(QPixmap)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url
        self.window = parent

    def run(self):
        try:
            response = requests.get(
                self.url,
                proxies=get_proxies(
                    self.window.proxy_type_setting,
                    self.window.proxy_host_name_setting,
                    self.window.proxy_port_setting,
                    self.window.proxy_login_setting,
                    self.window.proxy_password_setting
                ),
                timeout=10
            )
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception(f"Failed to load thumbnail: {response.status_code}")

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            resized_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.thumbnail_loaded.emit(resized_pixmap)
        except Exception as e:
            logging.error(f"Error loading thumbnail: {str(e)}")
            self.thumbnail_loaded.emit(QPixmap())