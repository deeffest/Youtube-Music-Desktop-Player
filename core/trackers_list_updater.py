import os
import time
import json
import logging
from typing import TYPE_CHECKING

import requests
from PySide6.QtCore import QThread, Signal

if TYPE_CHECKING:
    from core.main_window import MainWindow


class TrackersListUpdater(QThread):
    trackers_list_updated = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

    def run(self):
        cache_path = os.path.join(self.window.cache_dir, "trackers.json")

        try:
            if os.path.exists(cache_path):
                with open(cache_path, "r") as f:
                    cached = json.load(f)
                diff = time.time() - cached["fetched_at"]
                if 0 <= diff < 7 * 24 * 3600:
                    self.trackers_list_updated.emit(cached["domains"])
                    return
        except Exception as e:
            logging.error(f"Failed to load cached trackers: {e}")

        try:
            response = requests.get(
                "https://raw.githubusercontent.com/disconnectme/"
                "disconnect-tracking-protection/master/services.json",
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            domains = set()
            for category in ("Analytics", "Advertising"):
                for entry in data["categories"].get(category, []):
                    google_urls = entry.get("Google")
                    if google_urls:
                        for url_domains in google_urls.values():
                            domains.update(url_domains)
            domains = sorted(domains)

            with open(cache_path, "w") as f:
                json.dump({"fetched_at": time.time(), "domains": domains}, f)

            self.trackers_list_updated.emit(domains)
        except Exception as e:
            logging.error(f"Failed to fetch trackers: {e}")
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "r") as f:
                        self.trackers_list_updated.emit(json.load(f)["domains"])
                        return
                except Exception as e:
                    logging.error(f"Failed to load cached trackers: {e}")
            self.trackers_list_updated.emit([])

    def stop(self):
        self.terminate()
        self.wait()
