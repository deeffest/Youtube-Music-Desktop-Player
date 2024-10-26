import re
import os
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from pytubefix import YouTube, Playlist

class DownloadThread(QThread):
    download_finished = pyqtSignal(str, str)
    download_failed = pyqtSignal(str, str, str)

    def __init__(self, url, download_folder, parent=None):
        super().__init__(parent)
        self.url = url
        self.download_folder = download_folder
        self.title = "Unknown"
        self.window = parent

    def run(self):
        try:
            if "watch" in self.url:
                self.download_youtube()
            elif "playlist" in self.url:
                self.download_playlist()
        except Exception as e:
            logging.error("DownloadThread UnexpectedError: " + str(e))
            self.download_failed.emit(self.url, self.download_folder, self.title)
        else:
            self.download_finished.emit(self.download_folder, self.title)

    def download_youtube(self):
        yt = YouTube(self.url, client="MWEB", proxies=self.get_proxies())
        self.title = yt.title
        sanitized_title = self.sanitize_filename(yt.title)
        stream = yt.streams.get_audio_only()
        stream.download(output_path=self.download_folder, filename=f"{sanitized_title}.mp3", 
                        timeout=5, skip_existing=False, max_retries=2)

    def download_playlist(self):
        pl = Playlist(self.url, client="MWEB", proxies=self.get_proxies())
        self.title = self.sanitize_filename(pl.title)
        playlist_folder = os.path.join(self.download_folder, self.title)
        os.makedirs(playlist_folder, exist_ok=True)

        for video in pl.videos:
            sanitized_title = self.sanitize_filename(video.title)
            stream = video.streams.get_audio_only()
            stream.download(output_path=playlist_folder, filename=f"{sanitized_title}.mp3", 
                            timeout=5, skip_existing=False, max_retries=2)

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

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