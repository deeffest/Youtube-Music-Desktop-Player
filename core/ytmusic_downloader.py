import os
import re
import logging
import requests
import subprocess
from pytubefix import YouTube, Playlist
from core.get_proxies import get_proxies
from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop

class DownloadThread(QThread):
    download_finished = pyqtSignal(str, str)
    download_failed = pyqtSignal(str, str, str, bool)
    oauth_required = pyqtSignal(str, str)

    def __init__(self, url, download_folder, parent=None, use_oauth=False):
        super().__init__(parent)
        self.url = url
        self.download_folder = download_folder
        self.title = "Unknown"
        self.window = parent
        self.use_oauth = use_oauth
        self.ffmpeg_path = os.path.join(os.path.expanduser("~"), self.window.name, "bin", "ffmpeg.exe")
        self.oauth_cache_path = os.path.join(os.path.expanduser("~"), self.window.name, "__cache__", "tokens.json")

    def run(self):
        try:
            self.ensure_ffmpeg()
            if "watch" in self.url:
                self.download_youtube()
            elif "playlist" in self.url:
                self.download_playlist()
        except Exception as e:
            logging.error("DownloadThread UnexpectedError: " + str(e))
            self.download_failed.emit(self.url, self.download_folder, self.title, self.use_oauth)
        else:
            self.download_finished.emit(self.download_folder, self.title)

    def ensure_ffmpeg(self):
        if not os.path.exists(self.ffmpeg_path):
            os.makedirs(os.path.dirname(self.ffmpeg_path), exist_ok=True)
            ffmpeg_url = "https://github.com/deeffest/Youtube-Music-Desktop-Player/releases/download/1.0/ffmpeg.exe"
            response = requests.get(ffmpeg_url, stream=True)
            with open(self.ffmpeg_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            os.chmod(self.ffmpeg_path, 0o755)

    def download_video(self, yt, output_folder):
        title = self.sanitize_filename(f"{yt.title}.mp3")
        stream = yt.streams.get_audio_only()
        temp_file = stream.download(output_path=output_folder, filename=title)
        self.convert_to_mp3(temp_file, os.path.join(output_folder, title))

    def setup_yt_object(self, url, is_playlist=False):
        yt_object = (Playlist if is_playlist else YouTube)(
            url,
            client="MWEB",
            use_oauth=self.use_oauth,
            allow_oauth_cache=self.use_oauth,
            oauth_verifier=self.oauth_verifier,
            token_file=self.oauth_cache_path,
            proxies=get_proxies(
                self.window.proxy_type_setting,
                self.window.proxy_host_name_setting,
                self.window.proxy_port_setting,
                self.window.proxy_login_setting,
                self.window.proxy_password_setting
            )
        )
        return yt_object

    def download_youtube(self):
        yt = self.setup_yt_object(self.url, is_playlist=False)
        self.title = self.sanitize_filename(yt.title)
        self.download_video(yt, self.download_folder)

    def download_playlist(self):
        pl = self.setup_yt_object(self.url, is_playlist=True)
        self.title = self.sanitize_filename(pl.title)
        playlist_folder = os.path.join(self.download_folder, self.title)
        os.makedirs(playlist_folder, exist_ok=True)

        for yt in pl.videos:
            self.download_video(yt, playlist_folder)

    def oauth_verifier(self, verification_url, user_code):
        self.oauth_required.emit(verification_url, user_code)
        loop = QEventLoop()
        self.window.oauth_completed.connect(loop.quit)
        loop.exec_()    

    def convert_to_mp3(self, input_file, output_file):
        output_dir = os.path.dirname(output_file)
        base_filename = os.path.basename(output_file)
        
        sanitized_filename = self.sanitize_filename(base_filename)
        sanitized_output_file = os.path.join(output_dir, sanitized_filename)

        subprocess.run(
            [self.ffmpeg_path, "-y", "-i", input_file, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", sanitized_output_file],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        os.remove(input_file)

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)