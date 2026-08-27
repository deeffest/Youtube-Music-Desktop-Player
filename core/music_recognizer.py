import os
import uuid
import random
import asyncio
import logging
from typing import TYPE_CHECKING

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from shazamio_core import Recognizer

from core.audio_recorder import record_to_wav

if TYPE_CHECKING:
    from core.main_window import MainWindow


NOT_RECOGNIZED_MESSAGE = (
    "Music not recognized; try a different"
    " time range or increase the recording length in the settings."
)

SHAZAM_SEARCH_URL = (
    "https://amp.shazam.com/discovery/v5/{language}/{endpoint_country}/{device}/-/tag"
    "/{uuid_1}/{uuid_2}?sync=true&webv3=true&sampling=true&connected="
    "&shazamapiversion=v3&sharehub=true&hubv5minorversion=v5.1&hidelb=true&video=v3"
)


class RecognitionError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def _recognize_via_audd_api(wav_path, api_token):
    with open(wav_path, "rb") as f:
        resp = requests.post(
            "https://api.audd.io/",
            data={"api_token": api_token},
            files={"file": f},
            timeout=10,
        )

    resp_json = resp.json()

    if resp_json["status"] != "success":
        e = resp_json.get("error", {})
        logging.error(resp_json)
        raise RecognitionError(
            e.get("error_code", "Unknown code"), e.get("error_message", "Unknown error")
        )

    result = resp_json.get("result")
    if not result:
        raise RecognitionError(0, NOT_RECOGNIZED_MESSAGE)

    return result["artist"], result["title"]


def _recognize_via_shazam_api(wav_path):
    async def _get_signature():
        return await Recognizer().recognize_path(wav_path)

    signature = asyncio.run(_get_signature())

    url = SHAZAM_SEARCH_URL.format(
        language="en-US",
        endpoint_country="GB",
        device=random.choice(("iphone", "android", "web")),
        uuid_1=str(uuid.uuid4()).upper(),
        uuid_2=str(uuid.uuid4()).upper(),
    )
    body = {
        "timezone": "Europe/Moscow",
        "signature": {
            "uri": signature.signature.uri,
            "samplems": signature.signature.samples,
        },
        "timestamp": signature.timestamp,
        "context": {},
        "geolocation": {},
    }
    headers = {
        "X-Shazam-Platform": "IPHONE",
        "X-Shazam-AppVersion": "14.1.0",
        "Accept": "*/*",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) Apple"
        "WebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    }

    resp = requests.post(url, headers=headers, json=body, timeout=10)
    resp_json = resp.json()

    track = resp_json.get("track")
    if not track:
        raise RecognitionError(0, NOT_RECOGNIZED_MESSAGE)

    return track["subtitle"], track["title"]


class MusicRecognizerThread(QThread):
    recording_audio_from_pc = pyqtSignal()
    recording_audio_from_pc_success = pyqtSignal()

    recognizing_via_audd_api = pyqtSignal()
    recognizing_via_audd_api_error = pyqtSignal(int, str, str)
    recognizing_via_audd_api_success = pyqtSignal(str, str)

    recognizing_via_shazam_api = pyqtSignal()
    recognizing_via_shazam_api_error = pyqtSignal(int, str, str)
    recognizing_via_shazam_api_success = pyqtSignal(str, str)

    def __init__(self, service, duration, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.service = service
        self.duration = duration

        self.temp_wav = os.path.join(self.window.cache_dir, "temp.wav")

    def run(self):
        self.recording_audio_from_pc.emit()
        record_to_wav(self.duration, self.temp_wav)
        self.recording_audio_from_pc_success.emit()

        if self.service == "AudD":
            self.recognizing_via_audd_api.emit()
            try:
                artist, title = _recognize_via_audd_api(
                    self.temp_wav, self.window.audd_api_token_setting
                )
            except RecognitionError as e:
                self.recognizing_via_audd_api_error.emit(
                    e.code, e.message, self.service
                )
            else:
                self.recognizing_via_audd_api_success.emit(artist, title)
        elif self.service == "Shazam":
            self.recognizing_via_shazam_api.emit()
            try:
                artist, title = _recognize_via_shazam_api(self.temp_wav)
            except RecognitionError as e:
                self.recognizing_via_shazam_api_error.emit(
                    e.code, e.message, self.service
                )
            else:
                self.recognizing_via_shazam_api_success.emit(artist, title)

    def stop(self):
        self.terminate()
        self.wait()
