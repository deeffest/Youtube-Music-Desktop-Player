import sys
from pytube import YouTube, Playlist
import subprocess
import os

def download_track(url, download_path, download_type):
    if download_type == "track":
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download(output_path=download_path)

        name, ext = os.path.splitext(filename)
        existing_file = os.path.join(download_path, f"{name}.mp3")
        input_file = filename
        output_file = f"{name}.mp3" 

        try:
            subprocess.run(["ffmpeg", "-i", input_file, "-y", output_file], creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            print("FFmpeg is not found. Conversion will be skipped.")
            return
        
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

            try:
                subprocess.run(["ffmpeg", "-i", input_file, "-y", output_file], creationflags=subprocess.CREATE_NO_WINDOW)
            except FileNotFoundError:
                print("FFmpeg is not found. Conversion for this file will be skipped.")
                continue

            os.remove(input_file)

        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)

    url = sys.argv[1]
    download_path = sys.argv[2]
    download_type = sys.argv[3]

    download_track(url, download_path, download_type)