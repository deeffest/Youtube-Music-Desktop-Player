import os
import time
import wave
import audioop
import logging
import platform
import subprocess
from typing import TYPE_CHECKING

import requests
from PySide6.QtCore import QThread, Signal

if TYPE_CHECKING:
    from core.main_window import MainWindow


RATE = 44100
CHANNELS = 1
WIDTH = 2
CHUNK_FRAMES = 1024


def _record_win32(duration):
    import pyaudiowpatch as pyaudio

    pa = pyaudio.PyAudio()
    stream = None
    try:
        wasapi_info = pa.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_out = pa.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        device = default_out
        for loopback in pa.get_loopback_device_info_generator():
            if default_out["name"] in loopback["name"]:
                device = loopback
                break

        rate = int(device["defaultSampleRate"])
        channels = device["maxInputChannels"]
        frames_needed = int(rate * duration)
        chunks, collected = [], 0

        def _callback(in_data, frame_count, time_info, status):
            nonlocal collected
            chunks.append(in_data)
            collected += frame_count
            done = collected >= frames_needed
            return (None, pyaudio.paComplete if done else pyaudio.paContinue)

        stream = pa.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=device["index"],
            frames_per_buffer=CHUNK_FRAMES,
            stream_callback=_callback,
        )
        stream.start_stream()

        deadline = time.monotonic() + duration + 5
        while stream.is_active() and time.monotonic() < deadline:
            time.sleep(0.05)
    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        pa.terminate()

    return b"".join(chunks), rate, channels


def _record_linux(duration):
    cmd = [
        "parec",
        "--device=@DEFAULT_SINK@.monitor",
        f"--rate={RATE}",
        f"--channels={CHANNELS}",
        "--format=s16le",
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        raw = process.stdout.read(int(RATE * duration) * WIDTH)
    finally:
        process.terminate()
        process.wait()

    return raw, RATE, CHANNELS


class MusicRecognizerThread(QThread):
    recording_audio_from_pc = Signal()
    recording_audio_from_pc_success = Signal()

    recognizing_via_audd_api = Signal()
    recognizing_via_audd_api_error = Signal(int, str)
    recognizing_via_audd_api_success = Signal(str, str)

    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.service = service

        self.temp_wav = os.path.join(self.window.cache_dir, "temp.wav")

    def run(self):
        self.recording_audio_from_pc.emit()
        duration = self.window.audd_recording_lenght_setting

        if platform.system() == "Windows":
            raw, rate, channels = _record_win32(duration)
        else:
            raw, rate, channels = _record_linux(duration)

        if channels > 1:
            raw = audioop.tomono(raw, WIDTH, 0.5, 0.5)
        if rate != RATE:
            raw, _ = audioop.ratecv(raw, WIDTH, 1, rate, RATE, None)

        with wave.open(self.temp_wav, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(WIDTH)
            wf.setframerate(RATE)
            wf.writeframes(raw)

        self.recording_audio_from_pc_success.emit()

        if self.service == "AudD":
            self.recognizing_via_audd_api.emit()

            with open(self.temp_wav, "rb") as f:
                resp = requests.post(
                    "https://api.audd.io/",
                    data={"api_token": self.window.audd_api_token_setting},
                    files={"file": f},
                    timeout=10,
                )

            resp_json = resp.json()

            if resp_json["status"] == "success":
                r = resp_json.get("result")
                if r:
                    self.recognizing_via_audd_api_success.emit(r["title"], r["artist"])
                else:
                    self.recognizing_via_audd_api_error.emit(
                        0,
                        "Music not recognized; try a different"
                        " time range or increase the recording length in the settings.",
                    )
            else:
                e = resp_json.get("error", {})
                code = e.get("error_code", "Unknown code")
                msg = e.get("error_message", "Unknown error")
                logging.error(resp_json)
                self.recognizing_via_audd_api_error.emit(code, msg)

    def stop(self):
        self.terminate()
        self.wait()
