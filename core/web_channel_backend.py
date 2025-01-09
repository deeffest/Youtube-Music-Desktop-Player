from PyQt5.QtCore import QObject, pyqtSlot

class WebChannelBackend(QObject):
    def __init__(self, parent):
        super().__init__()
        self.window = parent

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
        window_title = "Youtube Music Desktop Player" if is_empty else f"{self.window.title} - Youtube Music Desktop Player"
        self.window.setWindowTitle(window_title)
        
        if self.window.tray_icon:
            self.window.tray_icon.setToolTip(window_title)

        if not is_empty and self.window.track_change_notificator_setting and self.window.track_notifier is not None:
            self.window.track_notifier.show_toast(
                self.window.title,
                self.window.author,
                duration=5,
                icon_path=f"{self.window.icon_folder}/music-notify.ico",
                threaded=True
            )
        
        if is_empty:
            self.window.clear_discord_rpc()
        else:
            self.window.update_mini_player_track_info()
            self.window.update_discord_rpc()

    @pyqtSlot(str, str)
    def track_progress_changed(self, current_time, total_time):
        self.window.current_time = current_time
        self.window.total_time = total_time

        self.window.update_mini_player_track_progress()

    def update_mini_player_track_progress(self):
        if self.window.mini_player_dialog:
            self.window.mini_player_dialog.BodyLabel.setText(self.window.current_time)
            self.window.mini_player_dialog.BodyLabel_2.setText(self.window.total_time)

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