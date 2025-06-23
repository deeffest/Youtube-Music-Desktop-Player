import os
import requests
import subprocess
import sqlite3
import tempfile
import uuid
from typing import TYPE_CHECKING
from PyQt5.QtCore import QThread

from core.helpers import get_proxies

if TYPE_CHECKING:
    from core.main_window import MainWindow


class DownloadThread(QThread):
    def __init__(self, url, download_folder, parent=None, use_cookies=False):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.url = url
        self.download_folder = download_folder
        self.use_cookies = use_cookies

        base_path = os.path.join(os.path.expanduser("~"), self.window.name)
        self.bin_folder = os.path.join(base_path, "bin")
        self.ytdlp_path = os.path.join(self.bin_folder, "yt-dlp.exe")
        self.ffmpeg_path = os.path.join(self.bin_folder, "ffmpeg.exe")
        self.cookies_txt = os.path.join(base_path, "__cache__", "cookies.txt")
        self.cookies_sqlite = os.path.join(
            self.window.webview.page().profile().persistentStoragePath(), "Cookies"
        )

    def run(self):
        self.ensure_tools()
        if self.use_cookies:
            self.export_cookies()
        self.spawn_ytdlp()

    def ensure_tools(self):
        os.makedirs(self.bin_folder, exist_ok=True)

        if not os.path.exists(self.ffmpeg_path):
            url = (
                "https://github.com/deeffest/pytubefix/"
                "releases/download/v8.12.3/FFmpeg-Win32.exe"
            )
            tmp_path = self.ffmpeg_path + ".tmp"
            r = requests.get(url, stream=True)
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            os.rename(tmp_path, self.ffmpeg_path)
            os.chmod(self.ffmpeg_path, 0o755)

        if not os.path.exists(self.ytdlp_path):
            url = (
                "https://github.com/yt-dlp/yt-dlp/"
                "releases/latest/download/yt-dlp.exe"
            )
            tmp_path = self.ytdlp_path + ".tmp"
            r = requests.get(url, stream=True)
            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            os.rename(tmp_path, self.ytdlp_path)
            os.chmod(self.ytdlp_path, 0o755)

    def export_cookies(self):
        if not os.path.exists(self.cookies_sqlite):
            return

        os.makedirs(os.path.dirname(self.cookies_txt), exist_ok=True)
        conn = sqlite3.connect(self.cookies_sqlite)
        cursor = conn.cursor()

        def chrome_time_to_unix(chrome_time):
            if not chrome_time:
                return 0
            return int(chrome_time / 1_000_000 - 11644473600)

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

    def spawn_ytdlp(self):
        url = self.url.replace("music.youtube.com", "www.youtube.com")

        if "list=" in url and "watch" not in url:
            output_template = "%(playlist_title)s/%(title)s.%(ext)s"
        else:
            output_template = "%(title)s.%(ext)s"

        output_template_escaped = output_template.replace("%", "%%")

        command = [
            self.ytdlp_path,
            "--update",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--ffmpeg-location",
            os.path.join(self.bin_folder, "ffmpeg.exe"),
            "-o",
            output_template_escaped,
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

        cmd_line = " ".join(
            (
                f'"{arg}"'
                if (" " in arg or "&" in arg or "(" in arg or ")" in arg)
                else arg
            )
            for arg in command
        )

        temp_dir = tempfile.gettempdir()
        ytmdp_temp_folder = os.path.join(temp_dir, "ytmdp_temp")
        os.makedirs(ytmdp_temp_folder, exist_ok=True)

        batch_file_name = f"ytmdp_{uuid.uuid4().hex}.bat"
        batch_file_path = os.path.join(ytmdp_temp_folder, batch_file_name)

        batch_content = f"""
            @echo off
            title yt-dlp Download
            echo Starting download...
            {cmd_line}
            if %errorlevel% == 0 (
                echo Download completed successfully.
            ) else (
                echo Download failed with error code %errorlevel%.
            )
            pause
        """

        with open(batch_file_path, "w", encoding="utf-8") as batch_file:
            batch_file.write(batch_content)

        subprocess.Popen(
            ["cmd.exe", "/c", batch_file_path],
            cwd=self.download_folder,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

    def stop(self):
        self.terminate()
        self.wait()
