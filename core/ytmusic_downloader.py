import os
import json
import sqlite3
import logging
import requests
import platform
import subprocess

from typing import TYPE_CHECKING
from PyQt5.QtCore import QThread, pyqtSignal

from core.helpers import get_proxies

if TYPE_CHECKING:
    from core.main_window import MainWindow


class DownloadThread(QThread):
    downloading_ffmpeg = pyqtSignal()
    downloading_ffmpeg_success = pyqtSignal()

    downloading_ytdlp = pyqtSignal()
    downloading_ytdlp_success = pyqtSignal()

    downloading_audio = pyqtSignal()
    downloading_audio_error = pyqtSignal(str, str)
    downloading_audio_success = pyqtSignal(str, str)

    def __init__(self, url, download_folder, parent=None, use_cookies=False):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.url = url
        self.download_folder = download_folder
        self.use_cookies = use_cookies

        base_path = os.path.join(os.path.expanduser("~"), self.window.name)
        self.bin_folder = os.path.join(base_path, "bin")

        if platform.system() == "Windows":
            self.ffmpeg_url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/FFmpeg-Win32.exe"
            )
            self.ytdlp_url = (
                "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            )
            self.ffmpeg_path = os.path.join(self.bin_folder, "ffmpeg.exe")
            self.ytdlp_path = os.path.join(self.bin_folder, "yt-dlp.exe")
        else:
            self.ffmpeg_url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/FFmpeg-Linux"
            )
            self.ytdlp_url = (
                "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
            )
            self.ffmpeg_path = os.path.join(self.bin_folder, "ffmpeg")
            self.ytdlp_path = os.path.join(self.bin_folder, "yt-dlp")

        self.cookies_txt = os.path.join(base_path, "__cache__", "cookies.txt")
        self.cookies_sqlite = os.path.join(
            self.window.webview.page().profile().persistentStoragePath(), "Cookies"
        )

    def run(self):
        self.ensure_tools()
        if self.use_cookies:
            self.export_cookies()
        self.emit_command()

    def ensure_tools(self):
        def download_binary(url, dst_path):
            tmp_path = dst_path + ".tmp"
            r = requests.get(
                url,
                proxies=get_proxies(
                    self.window.proxy_type_setting,
                    self.window.proxy_host_name_setting,
                    self.window.proxy_port_setting,
                    self.window.proxy_login_setting,
                    self.window.proxy_password_setting,
                ),
                stream=True,
                timeout=10,
            )
            r.raise_for_status()
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            os.rename(tmp_path, dst_path)
            if platform.system() != "Windows":
                os.chmod(dst_path, 0o755)

        os.makedirs(self.bin_folder, exist_ok=True)
        if not os.path.exists(self.ffmpeg_path):
            self.downloading_ffmpeg.emit()
            download_binary(self.ffmpeg_url, self.ffmpeg_path)
            self.downloading_ffmpeg_success.emit()
        if not os.path.exists(self.ytdlp_path):
            self.downloading_ytdlp.emit()
            download_binary(self.ytdlp_url, self.ytdlp_path)
            self.downloading_ytdlp_success.emit()

    def export_cookies(self):
        if not os.path.exists(self.cookies_sqlite):
            return
        os.makedirs(os.path.dirname(self.cookies_txt), exist_ok=True)
        conn = sqlite3.connect(self.cookies_sqlite)
        cursor = conn.cursor()

        def chrome_time_to_unix(chrome_time):
            return int(chrome_time / 1_000_000 - 11644473600) if chrome_time else 0

        with open(self.cookies_txt, "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for row in cursor.execute(
                "SELECT host_key, path, is_secure, expires_utc, name, value "
                "FROM cookies"
            ):
                domain, path, is_secure, expires_utc, name, value = row
                include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
                expires = chrome_time_to_unix(expires_utc)
                secure_flag = "TRUE" if is_secure else "FALSE"
                f.write(
                    f"{domain}\t{include_subdomains}\t{path}\t{secure_flag}\t"
                    f"{expires}\t{name}\t{value}\n"
                )
        conn.close()

    def emit_command(self):
        url = self.url.replace("music.youtube.com", "www.youtube.com")

        output_template = (
            "%(playlist_title).80B/%(title).150B.%(ext)s"
            if "list=" in url and "watch" not in url
            else "%(title).150B.%(ext)s"
        )

        command = [
            self.ytdlp_path,
            "--update",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--ffmpeg-location",
            self.ffmpeg_path,
            "-o",
            output_template,
            "--print-json",
            "--socket-timeout",
            "10",
        ]

        if "watch" in url and "list=" in url:
            command.append("--no-playlist")

        if self.use_cookies and os.path.exists(self.cookies_txt):
            command += ["--cookies", self.cookies_txt]

        proxy_config = {
            "proxy_type": self.window.proxy_type_setting,
            "host_name": self.window.proxy_host_name_setting,
            "port": self.window.proxy_port_setting,
            "login": self.window.proxy_login_setting,
            "password": self.window.proxy_password_setting,
        }

        proxies = {}
        if proxy_config["proxy_type"] == "DefaultProxy":
            proxies = get_proxies(proxy_type="DefaultProxy")
        elif proxy_config["proxy_type"] in ["HttpProxy", "Socks5Proxy"]:
            if proxy_config["host_name"] and proxy_config["port"]:
                proxies = get_proxies(**proxy_config)

        if "https" in proxies:
            command += ["--proxy", proxies["https"]]

        command.append(url)
        self.start_ytdlp(command)

    def start_ytdlp(self, command):
        self.downloading_audio.emit()

        kwargs = dict(
            cwd=self.download_folder,
            capture_output=True,
            text=False,
        )

        if platform.system() == "Windows":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(command, **kwargs)

        stdout_decoded = (
            result.stdout.decode("utf-8", errors="ignore") if result.stdout else ""
        )
        stderr_decoded = (
            result.stderr.decode("utf-8", errors="ignore") if result.stderr else ""
        )

        lines = stdout_decoded.strip().splitlines()
        titles = []
        playlist_title = None
        for line in lines:
            try:
                data = json.loads(line)
                titles.append(data.get("title", "Unknown"))
                if not playlist_title and "playlist_title" in data:
                    playlist_title = data["playlist_title"]
            except Exception:
                titles.append("Unknown")

        title = (
            playlist_title if playlist_title else (titles[0] if titles else "Unknown")
        )

        if result.returncode == 0:
            self.downloading_audio_success.emit(self.download_folder, title)
        else:
            e = stderr_decoded.strip()
            logging.error(e)
            self.downloading_audio_error.emit(e, title)

    def stop(self):
        self.terminate()
        self.wait()
