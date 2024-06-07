import sys
from pytube import YouTube, Playlist
import subprocess
import os

def sanitize_filename(filename):
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename

def download_track(url, download_path, download_type):
    os.chdir(download_path)
    if download_type == "track":
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download()

        name, ext = os.path.splitext(os.path.basename(filename))
        name = sanitize_filename(name)
        output_file = f"{name}.mp3"

        try:
            subprocess.run(["ffmpeg", "-i", filename, "-y", output_file], creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            print("FFmpeg is not found. Conversion will be skipped.")
            return

        os.remove(filename)

    elif download_type == "playlist":
        playlist = Playlist(url)
        playlist_name = sanitize_filename(playlist.title)
        folder_path = os.path.join(download_path, playlist_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        os.chdir(folder_path)
        for video in playlist.videos:
            stream = video.streams.filter(type='video', progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            filename = stream.download()

            name, ext = os.path.splitext(os.path.basename(filename))
            name = sanitize_filename(name)
            output_file = f"{name}.mp3"

            try:
                subprocess.run(["ffmpeg", "-i", filename, "-y", output_file], creationflags=subprocess.CREATE_NO_WINDOW)
            except FileNotFoundError:
                print("FFmpeg is not found. Conversion for this file will be skipped.")
                continue

            os.remove(filename)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)

    url = sys.argv[1]
    download_path = sys.argv[2]
    download_type = sys.argv[3]

    download_track(url, download_path, download_type)