import os
import logging
import requests
import subprocess
from typing import TYPE_CHECKING

from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop
from pytubefix import YouTube, Playlist

from core.helpers import get_proxies, sanitize_filename

if TYPE_CHECKING:
    from core.main_window import MainWindow


class DownloadThread(QThread):
    download_finished = pyqtSignal(str, str)
    download_failed = pyqtSignal(str, str, str, bool)
    oauth_required = pyqtSignal(str, str)

    def __init__(self, url, download_folder, parent=None, use_oauth=False):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.url = url
        self.download_folder = download_folder
        self.title = "Unknown"
        self.use_oauth = use_oauth

        base_path = os.path.join(os.path.expanduser("~"), self.window.name)
        self.oauth_cache_path = os.path.join(base_path, "__cache__", "tokens.json")
        self.ffmpeg_path = os.path.join(base_path, "bin", "ffmpeg.exe")

    def run(self):
        try:
            self.ensure_ffmpeg()
            if "watch" in self.url:
                self.download_youtube()
            elif "playlist" in self.url:
                self.download_playlist()
        except Exception as e:
            logging.error(f"Failed to download track/playlist: {str(e)}")
            self.download_failed.emit(
                self.url, self.download_folder, self.title, self.use_oauth
            )
        else:
            self.download_finished.emit(self.download_folder, self.title)

    def is_ffmpeg_valid(self):
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            return b"ffmpeg version" in result.stdout
        except Exception as e:
            logging.error(f"Failed to validate ffmpeg: {str(e)}")
            return False

    def ensure_ffmpeg(self):
        if not os.path.exists(self.ffmpeg_path) or not self.is_ffmpeg_valid():
            os.makedirs(os.path.dirname(self.ffmpeg_path), exist_ok=True)
            ffmpeg_url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/FFmpeg-Win32.exe"
            )
            temp_ffmpeg_path = self.ffmpeg_path + ".tmp"

            response = requests.get(ffmpeg_url, stream=True)
            with open(temp_ffmpeg_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            if os.path.exists(self.ffmpeg_path):
                os.remove(self.ffmpeg_path)

            os.rename(temp_ffmpeg_path, self.ffmpeg_path)
            os.chmod(self.ffmpeg_path, 0o755)

    def download_video(self, yt, output_folder):
        original_filename = sanitize_filename(f"{yt.title}.m4a")
        temp_file = yt.streams.get_audio_only().download(
            output_path=output_folder,
            filename=original_filename,
            timeout=10,
            max_retries=3,
        )
        final_filename = sanitize_filename(f"{yt.title}.mp3")
        output_file = os.path.join(output_folder, final_filename)
        self.convert_to_mp3(temp_file, output_file)

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
                self.window.proxy_password_setting,
            ),
        )
        return yt_object

    def download_youtube(self):
        yt = self.setup_yt_object(self.url, is_playlist=False)
        self.title = sanitize_filename(yt.title)
        self.download_video(yt, self.download_folder)

    def download_playlist(self):
        pl = self.setup_yt_object(self.url, is_playlist=True)
        self.title = sanitize_filename(pl.title)
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
        subprocess.run(
            [
                self.ffmpeg_path,
                "-y",
                "-i",
                input_file,
                "-vn",
                "-ar",
                "44100",
                "-ac",
                "2",
                "-b:a",
                "192k",
                output_file,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        os.remove(input_file)

    def stop(self):
        self.terminate()
        self.wait()
