import sys
from pytube import YouTube, Playlist
import subprocess
import os
import requests

def download_track(url, download_path, download_type, script_dir):
    if not check_ffmpeg_available():
        download_ffmpeg(script_dir)

    if download_type == "track":
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download(output_path=download_path)

        name, ext = os.path.splitext(filename)
        existing_file = os.path.join(download_path, f"{name}.mp3")
        input_file = filename
        output_file = f"{name}.mp3" 

        subprocess.run(
            ["ffmpeg", "-i", input_file, "-y", output_file], 
            creationflags=subprocess.CREATE_NO_WINDOW
            )
        os.remove(input_file)

        sys.exit(0)

    elif download_type == "playlist":
        playlist = Playlist(url)
        playlist_name = playlist.title.replace("/", "_")
        folder_path = os.path.join(download_path, playlist_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for video in playlist.videos:
            stream = video.streams.filter(
                type='video', 
                progressive=True, 
                file_extension='mp4'
                ).order_by('resolution').desc().first()
            filename = stream.download(output_path=folder_path)

            name, ext = os.path.splitext(filename)
            existing_file = os.path.join(folder_path, f"{name}.mp3")
            input_file = filename
            output_file = f"{name}.mp3"

            subprocess.run(
                ["ffmpeg", "-i", input_file, "-y", output_file], 
                creationflags=subprocess.CREATE_NO_WINDOW
                )
            os.remove(input_file)

        sys.exit(0)

def download_ffmpeg(script_dir):
    ffmpeg_url = "https://github.com/deeffest/Youtube-Music-Desktop-Player/releases/download/1.0/ffmpeg.exe" 
    ffmpeg_filename = os.path.join(f"{script_dir}/core", "ffmpeg.exe")

    try:
        response = requests.get(ffmpeg_url, stream=True)
        with open(ffmpeg_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        if not os.path.isfile(ffmpeg_filename):
            raise Exception("Error downloading FFmpeg.")

    except Exception as e:
        sys.exit(1)

def check_ffmpeg_available():
    try:
        subprocess.run(
            ["ffmpeg", "-version"], 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, 
            creationflags=subprocess.CREATE_NO_WINDOW
            )
        return True
    except:
        return False

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(1)

    url = sys.argv[1]
    download_path = sys.argv[2]
    download_type = sys.argv[3]
    script_dir = sys.argv[4]

    download_track(url, download_path, download_type, script_dir)