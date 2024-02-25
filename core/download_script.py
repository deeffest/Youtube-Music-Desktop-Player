import sys
from pytube import YouTube, Playlist
import subprocess
import os
import requests

def download_track(url, download_path, download_type):
    if download_type == "track":
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download(output_path=download_path)

        name, ext = os.path.splitext(filename)
        input_file = filename
        output_file = f"{name}.mp3"

        try:
            subprocess.run(["ffmpeg", "-i", input_file, output_file], creationflags=subprocess.CREATE_NO_WINDOW)
            os.remove(input_file)
        except subprocess.CalledProcessError:
            print("FFmpeg not found. Downloading...")
            download_ffmpeg(download_path)
            subprocess.run(["ffmpeg", "-i", input_file, output_file], creationflags=subprocess.CREATE_NO_WINDOW)
            os.remove(input_file)

    elif download_type == "playlist":
        playlist = Playlist(url)
        for video in playlist.videos:
            stream = video.streams.filter(type='video', progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            filename = stream.download(output_path=download_path)

            name, ext = os.path.splitext(filename)
            input_file = filename
            output_file = f"{name}.mp3"

            subprocess.run(["ffmpeg", "-i", input_file, output_file], creationflags=subprocess.CREATE_NO_WINDOW)
            os.remove(input_file)

def download_ffmpeg(download_path, script_dir):
    ffmpeg_url = "https://github.com/deeffest/Youtube-Music-Desktop-Player/releases/download/1.0/ffmpeg.exe" 
    ffmpeg_filename = os.path.join(script_dir, "ffmpeg.exe")

    try:
        response = requests.get(ffmpeg_url, stream=True)
        with open(ffmpeg_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        if not os.path.isfile(ffmpeg_filename):
            raise Exception("Error downloading FFmpeg.")

        print("FFmpeg downloaded successfully.")
    except Exception as e:
        print(f"Error downloading FFmpeg: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(1)

    url = sys.argv[1]
    download_path = sys.argv[2]
    download_type = sys.argv[3]
    script_dir = sys.argv[4]

    try:
        download_track(url, download_path, download_type)
    except:
        print("FFmpeg not found.")
        download_ffmpeg(download_path, script_dir)
        download_track(url, download_path, download_type)