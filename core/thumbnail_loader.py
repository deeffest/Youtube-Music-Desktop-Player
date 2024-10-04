import requests
import logging

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

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
            proxies = self.get_proxies()
            response = requests.get(self.url, proxies=proxies)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            resized_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.thumbnail_loaded.emit(resized_pixmap)
        except requests.exceptions.RequestException as e:
            logging.error("ThumbnailLoader RequestException: " + str(e))
            self.thumbnail_loaded.emit(QPixmap())
        except Exception as e:
            logging.error("ThumbnailLoader UnexpectedError: " + str(e))
        finally:
            self._is_running = False
            
    def is_running(self):
        return self._is_running

    def get_proxies(self):
        if self.window.proxy_type_setting in ["HttpProxy", "Socks5Proxy"]:
            proxy_address = f"{self.window.proxy_host_name_setting}:{self.window.proxy_port_setting}"

            if self.window.proxy_login_setting and self.window.proxy_password_setting:
                proxy_address = f"{self.window.proxy_login_setting}:{self.window.proxy_password_setting}@{proxy_address}"
                
            proxy_type = "http" if self.window.proxy_type_setting == "HttpProxy" else "socks5"
            return {
                "http": f"{proxy_type}://{proxy_address}",
                "https": f"{proxy_type}://{proxy_address}"
            }
        else:
            return None