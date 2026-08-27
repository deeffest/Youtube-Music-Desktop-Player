from typing import TYPE_CHECKING

from PySide6.QtWebEngineCore import (
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.blocked_domains = []

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        first_party = info.firstPartyUrl().toString()
        res_type = info.resourceType()

        if (
            "music.youtube.com" in first_party
            and self.window.block_google_trackers_setting == 1
        ):
            if self.blocked_domains:
                if any(d in url for d in self.blocked_domains):
                    return info.block(True)

            blocked_paths = (
                "/pagead/",
                "/ptracking",
                "/youtube/ads",
                "/api/stats/qoe",
                "/api/stats/atr",
                "/pcs/activeview",
                "/ads/ga-audiences",
                "/youtubei/v1/log_event",
            )
            if any(p in url for p in blocked_paths):
                return info.block(True)

        elif "m.youtube.com" in first_party:
            info.setHttpHeader(
                b"User-Agent",
                b"Mozilla/5.0 (Mobile; Nokia 8110 4G; rv:48.0) "
                b"Gecko/48.0 Firefox/48.0 KAIOS/2.5",
            )

            blocked_types = (
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypePing,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeMedia,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeWorker,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeFontResource,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeSharedWorker,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeServiceWorker,
            )
            if res_type in blocked_types:
                return info.block(True)

            if res_type == QWebEngineUrlRequestInfo.ResourceType.ResourceTypeXhr:
                if "/youtubei/v1/" in url:
                    essential_api = ("next", "comment", "get_panel", "flow")
                    if not any(a in url for a in essential_api):
                        return info.block(True)
                else:
                    return info.block(True)

            blocked_substrings = (
                "lottie",
                "log_event",
                "googleads",
                "doubleclick",
                "google.com/js",
            )
            if any(p in url for p in blocked_substrings):
                return info.block(True)

            if res_type == QWebEngineUrlRequestInfo.ResourceType.ResourceTypeImage:
                if "yt3.ggpht.com" not in url and "fonts.gstatic.com" not in url:
                    info.block(True)
