import os
import re
import logging

import requests
from PySide6.QtCore import QThread, Signal
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed

LRC_LINE_PATTERN = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)")
DURATION_TOLERANCE = 2
MAX_CACHED_FILES = 100


class LoadLyricsThread(QThread):
    load_lyrics_error = Signal(str)
    load_lyrics_failed = Signal()
    load_lyrics_success = Signal(list)

    def __init__(self, title, artist, duration, cache_dir, video_id, parent=None):
        super().__init__(parent)
        self.title = title
        self.artist = artist
        self.duration = duration
        self.cache_dir = cache_dir
        self.video_id = video_id

    @staticmethod
    def parse(lrc: str) -> list[tuple[float, str]]:
        lines = []
        for raw in lrc.splitlines():
            match = LRC_LINE_PATTERN.match(raw.strip())
            if match:
                minutes, seconds, text = match.groups()
                lines.append((int(minutes) * 60 + float(seconds), text.strip()))
        return lines

    @staticmethod
    def _request(session: requests.Session, url: str, params: dict):
        try:
            resp = session.get(url, params=params, timeout=15)
        except Exception as e:
            return None, "error", str(e)

        if resp.status_code == 200:
            return resp.json(), "ok", None
        if resp.status_code == 404:
            return None, "not_found", None

        status, body = resp.status_code, resp.text[:200]
        return None, "error", f"HTTP {status}: {body}"

    @classmethod
    def fetch_get(cls, session: requests.Session, title, artist, duration):
        data, status, error = cls._request(
            session,
            "https://lrclib.net/api/get",
            {"track_name": title, "artist_name": artist, "duration": duration},
        )
        if status != "ok":
            return None, status, error

        lyrics = data.get("syncedLyrics") or None
        return lyrics, ("found" if lyrics else "not_found"), None

    @classmethod
    def fetch_search(cls, session: requests.Session, title, duration):
        data, status, error = cls._request(
            session, "https://lrclib.net/api/search", {"track_name": title}
        )
        if status != "ok":
            return None, status, error

        candidates = [
            r
            for r in (data or [])
            if r.get("syncedLyrics")
            and r.get("duration") is not None
            and abs(r["duration"] - duration) <= DURATION_TOLERANCE
        ]
        if not candidates:
            return None, "not_found", None

        best = min(candidates, key=lambda r: abs(r["duration"] - duration))
        return best["syncedLyrics"], "found", None

    def fetch_lyrics(self, session: requests.Session):
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {
                pool.submit(
                    self.fetch_get, session, self.title, self.artist, self.duration
                ): "get",
                pool.submit(
                    self.fetch_search, session, self.title, self.duration
                ): "search",
            }
            results = {futures[fut]: fut.result() for fut in as_completed(futures)}

        for source in ("get", "search"):
            lrc, status, error = results[source]
            if lrc:
                return lrc, source, None

        if all(status == "not_found" for _, status, _ in results.values()):
            return None, None, None

        errors = [
            f"/{source}: {error}"
            for source, (_, status, error) in results.items()
            if status == "error"
        ]
        return None, None, "; ".join(errors)

    def load_from_cache(self, cache_path):
        if not os.path.exists(cache_path):
            return None
        with open(cache_path, encoding="utf-8") as f:
            lines = self.parse(f.read())
        return lines or None

    def trim_cache(self, lyrics_dir):
        files = sorted(
            (
                os.path.join(lyrics_dir, f)
                for f in os.listdir(lyrics_dir)
                if f.endswith(".lrc")
            ),
            key=os.path.getmtime,
        )
        while len(files) >= MAX_CACHED_FILES:
            os.remove(files.pop(0))

    def run(self):
        lyrics_dir = os.path.join(self.cache_dir, "lyrics")
        os.makedirs(lyrics_dir, exist_ok=True)
        cache_path = os.path.join(lyrics_dir, f"{self.video_id}.lrc")

        self.trim_cache(lyrics_dir)

        cached_lines = self.load_from_cache(cache_path)
        if cached_lines:
            self.load_lyrics_success.emit(cached_lines)
            return

        session = requests.Session()
        retry = Retry(total=2, backoff_factor=0.3)
        session.mount("https://", HTTPAdapter(max_retries=retry))

        try:
            lrc, source, error_msg = self.fetch_lyrics(session)
            lines = self.parse(lrc) if lrc else []

            if lines:
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(lrc)
                self.load_lyrics_success.emit(lines)
            elif error_msg:
                self.load_lyrics_error.emit(error_msg)
            else:
                self.load_lyrics_failed.emit()
        except Exception as e:
            logging.error(f"Failed to load lyrics: {str(e)}")
            self.load_lyrics_error.emit(str(e))

    def stop(self):
        self.terminate()
        self.wait()
