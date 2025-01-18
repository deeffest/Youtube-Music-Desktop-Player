from typing import TYPE_CHECKING

from PyQt5.QtCore import QObject, pyqtSlot
if TYPE_CHECKING:
    from main_window import MainWindow


class WebChannelBackend(QObject):
    def __init__(self, parent):
        super().__init__()
        self.window:"MainWindow" = parent

    @pyqtSlot(str)
    def like_status_changed(self, status):
        if status != "":
            self.window.like_status = status
        else:
            self.window.like_status = None

        self.window.update_mini_player_like_dislike_controls()

    @pyqtSlot(str, str, str)
    def track_info_changed(self, title, author, thumbnail_url):
        self.window.title = title
        self.window.author = author
        self.window.thumbnail_url = thumbnail_url

        is_empty = not self.window.title or not self.window.author or not self.window.thumbnail_url

        if is_empty:
            window_title = "Youtube Music Desktop Player"
            self.window.clear_discord_rpc()
        else:
            window_title = f"{self.window.title} - Youtube Music Desktop Player"
            self.window.update_mini_player_track_info()
            self.window.update_discord_rpc()
            self.window.send_notification()

        self.window.setWindowTitle(window_title)
        if self.window.tray_icon is not None:
            self.window.tray_icon.setToolTip(window_title)

    @pyqtSlot(str, str)
    def track_progress_changed(self, current_time, total_time):
        self.window.current_time = current_time
        self.window.total_time = total_time

        self.window.update_mini_player_track_progress()

    @pyqtSlot(str)
    def video_state_changed(self, state):
        self.window.video_state = state

        if self.window.video_state == "VideoPlaying" or self.window.video_state == "VideoPaused":
            self.window.mini_player_action.setEnabled(True)
            self.window.mini_player_tbutton.setEnabled(True)
            self.window.mini_player_shortcut.setEnabled(True)
        else:
            self.window.mini_player_action.setEnabled(False)
            self.window.mini_player_tbutton.setEnabled(False)
            self.window.mini_player_shortcut.setEnabled(False)

        self.window.update_mini_player_track_controls()
        self.window.update_win_thumbnail_buttons_track_controls()
        self.window.update_tray_icon_track_controls()
