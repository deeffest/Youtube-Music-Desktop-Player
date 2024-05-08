import sys
from pytube import YouTube, Playlist, cipher
from typing import List
from pytube.exceptions import RegexMatchError
import subprocess
import os

def fix(self, js: str):
    import re
    self.transform_plan: List[str] = cipher.get_transform_plan(js)
    var_regex = re.compile(r"^[\w\$_]+\W")
    var_match = var_regex.search(self.transform_plan[0])
    if not var_match:
        raise RegexMatchError(
            caller="__init__", pattern=var_regex.pattern
        )
    var = var_match.group(0)[:-1]
    self.transform_map = cipher.get_transform_map(js, var)
    self.js_func_patterns = [
        r"\w+\.(\w+)\(\w,(\d+)\)",
        r"\w+\[(\"\w+\")\]\(\w,(\d+)\)"
    ]

    self.throttling_plan = cipher.get_throttling_plan(js)
    self.throttling_array = cipher.get_throttling_function_array(js)

    self.calculated_n = None

cipher.Cipher.__init__=fix

def download_track(url, download_path, download_type):
    if download_type == "track":
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download(output_path=download_path)

        name, ext = os.path.splitext(filename)
        existing_file = os.path.join(download_path, f"{name}.mp3")
        input_file = filename
        output_file = f"{name}.mp3" 

        subprocess.run(["ffmpeg", "-i", input_file, "-y", output_file], creationflags=subprocess.CREATE_NO_WINDOW)
        os.remove(input_file)

        sys.exit(0)

    elif download_type == "playlist":
        playlist = Playlist(url)
        playlist_name = playlist.title.replace("/", "_")
        folder_path = os.path.join(download_path, playlist_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for video in playlist.videos:
            stream = video.streams.filter(type='video', progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            filename = stream.download(output_path=folder_path)

            name, ext = os.path.splitext(filename)
            existing_file = os.path.join(folder_path, f"{name}.mp3")
            input_file = filename
            output_file = f"{name}.mp3"

            subprocess.run(["ffmpeg", "-i", input_file, "-y", output_file], creationflags=subprocess.CREATE_NO_WINDOW)
            os.remove(input_file)

        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)

    url = sys.argv[1]
    download_path = sys.argv[2]
    download_type = sys.argv[3]

    download_track(url, download_path, download_type)