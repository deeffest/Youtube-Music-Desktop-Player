from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

from qfluentwidgets import (
    RoundMenu, Action, MenuAnimationType
)

import webbrowser

class WebEngineView(QWebEngineView):
    def contextMenuEvent(self, event):
        url = self.window().webview.url().toString()
        menu = RoundMenu(parent=self.window())

        go_back_action = Action("Back", shortcut="Left")
        go_back_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/arrow_back_white_24dp.svg")
        )
        go_back_action.triggered.connect(
            self.window().go_back
        )
        menu.addAction(go_back_action)

        go_forward_action = Action("Forward", shortcut="Right")
        go_forward_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/arrow_forward_white_24dp.svg")
        )
        go_forward_action.triggered.connect(
            self.window().go_forward
        )
        menu.addAction(go_forward_action)

        go_home_action = Action("Home", shortcut="Ctrl+H")
        go_home_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/home_white_24dp.svg")
        )
        go_home_action.triggered.connect(
            self.window().go_home
        )
        menu.addAction(go_home_action)

        go_reload_action = Action("Reload", shortcut="Ctrl+R")
        go_reload_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/refresh_white_24dp.svg")
        )
        go_reload_action.triggered.connect(
            self.window().go_reload
        )
        menu.addAction(go_reload_action)

        menu.addSeparator()

        download_menu = RoundMenu("Download...", self)
        download_menu.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/file_download_white_24dp.svg")
        )
        menu.addMenu(download_menu)

        download_track_action = Action('Track', shortcut="Ctrl+D")
        download_track_action.triggered.connect(
            lambda: self.window().go_download('track')
        )
        download_track_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/audiotrack_white_24dp.svg")
        )
        download_menu.addAction(download_track_action)

        download_playlist_action = Action('Playlist', shortcut="Ctrl+P")
        download_playlist_action.triggered.connect(
            lambda: self.window().go_download('playlist')
        )
        download_playlist_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/playlist_play_white_24dp.svg")
        )
        download_menu.addAction(download_playlist_action)

        open_mini_player_action = Action("Mini-Player", shortcut="Ctrl+M")
        open_mini_player_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/picture_in_picture_white_24dp.svg")
        )
        open_mini_player_action.triggered.connect(
            self.window().open_mini_player
        )
        menu.addAction(open_mini_player_action)

        menu.addSeparator()

        open_settings_action = Action("Settings", shortcut="Ctrl+S")
        open_settings_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/settings_white_24dp.svg")
        )
        open_settings_action.triggered.connect(
            self.window().open_settings_dialog
        )
        menu.addAction(open_settings_action)

        menu.addSeparator()        

        bug_report_action = Action("Bug Report")
        bug_report_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/bug_report_white_24dp.svg")
        )
        bug_report_action.triggered.connect(lambda:
            webbrowser.open_new_tab(
                "https://github.com/deeffest/Youtube-Music-Desktop-Player/issues/new/choose"
            )
        )
        menu.addAction(bug_report_action)

        open_about_action = Action("About...")
        open_about_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/info_white_24dp.svg")
        )
        open_about_action.triggered.connect(
            self.window().open_about_dialog
        )
        menu.addAction(open_about_action)

        if not "watch" in url:
            download_track_action.setEnabled(False)
            open_mini_player_action.setEnabled(False)
        if not "playlist" in url:
            download_playlist_action.setEnabled(False)

        if not self.page().history().canGoForward():
            go_forward_action.setEnabled(False)
        if not self.page().history().canGoBack():
            go_back_action.setEnabled(False)

        menu.exec(event.globalPos(), aniType=MenuAnimationType.DROP_DOWN)