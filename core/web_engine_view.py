from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, \
    QWebEnginePage
from qfluentwidgets import RoundMenu, Action, \
    MenuAnimationType

import webbrowser

class WebEngineView(QWebEngineView):
    def contextMenuEvent(self, event):
        url = self.window().webview.url().toString()

        menu = RoundMenu(parent=self.window())
        edit_menu = RoundMenu(parent=self.window())

        go_back_action = Action("Back", shortcut="Left")
        go_back_action.setIcon(QIcon(f"{self.window().icon_path}/left.svg"))
        go_back_action.triggered.connect(self.window().go_back)
        menu.addAction(go_back_action)

        go_forward_action = Action("Forward", shortcut="Right")
        go_forward_action.setIcon(QIcon(f"{self.window().icon_path}/right.svg"))
        go_forward_action.triggered.connect(self.window().go_forward)
        menu.addAction(go_forward_action)

        go_home_action = Action("Home", shortcut="Ctrl+H")
        go_home_action.setIcon(QIcon(f"{self.window().icon_path}/home.svg"))
        go_home_action.triggered.connect(self.window().go_home)
        menu.addAction(go_home_action)

        go_reload_action = Action("Reload", shortcut="Ctrl+R")
        go_reload_action.setIcon(QIcon(f"{self.window().icon_path}/sync.svg"))
        go_reload_action.triggered.connect(self.window().go_reload)
        menu.addAction(go_reload_action)

        menu.addSeparator()

        download_menu = RoundMenu("Download...", self)
        download_menu.setIcon(QIcon(f"{self.window().icon_path}/download.svg"))
        menu.addMenu(download_menu)

        download_track_action = Action('Track', shortcut="Ctrl+D")        
        download_track_action.setIcon(QIcon(f"{self.window().icon_path}/music.svg"))
        download_track_action.triggered.connect(self.window().go_download)
        download_menu.addAction(download_track_action)

        download_playlist_action = Action('Playlist', shortcut="Ctrl+P")        
        download_playlist_action.setIcon(QIcon(f"{self.window().icon_path}/playlist.svg"))
        download_playlist_action.triggered.connect(self.window().go_download)
        download_menu.addAction(download_playlist_action)        

        open_mini_player_action = Action("Mini-Player", shortcut="Ctrl+M")
        open_mini_player_action.setIcon(QIcon(f"{self.window().icon_path}/picture_in_picture.svg"))
        open_mini_player_action.triggered.connect(self.window().open_mini_player)
        menu.addAction(open_mini_player_action)

        menu.addSeparator()

        open_settings_action = Action("Settings", shortcut="Ctrl+S")
        open_settings_action.setIcon(QIcon(f"{self.window().icon_path}/settings.svg"))
        open_settings_action.triggered.connect(self.window().open_settings_dialog)
        menu.addAction(open_settings_action)

        menu.addSeparator()        

        bug_report_action = Action("Bug Report")
        bug_report_action.setIcon(QIcon(f"{self.window().icon_path}/bug.svg"))
        bug_report_action.triggered.connect(lambda:
            webbrowser.open_new_tab(
                "https://github.com/deeffest/Youtube-Music-Desktop-Player/issues/new/choose"
                ))
        menu.addAction(bug_report_action)

        open_about_action = Action("About...")
        open_about_action.setIcon(QIcon(f"{self.window().icon_path}/info.svg"))
        open_about_action.triggered.connect(self.window().open_about_dialog)
        menu.addAction(open_about_action)

        context_data = self.page().contextMenuData()
        if self.page().selectedText() or context_data.isContentEditable():
            copy_action = Action('Copy', shortcut="Ctrl+C")
            copy_action.setIcon(QIcon(f"{self.window().icon_path}/copy.svg"))
            copy_action.triggered.connect(self.window().handle_copy)
            copy_action.setEnabled(self.page().action(QWebEnginePage.Copy).isEnabled())
            edit_menu.addAction(copy_action)

            paste_action = Action('Paste', shortcut="Ctrl+V")
            paste_action.setIcon(QIcon(f"{self.window().icon_path}/paste.svg"))
            paste_action.triggered.connect(self.window().handle_paste)
            paste_action.setEnabled(context_data.isContentEditable())
            edit_menu.addAction(paste_action)

            edit_menu.exec(event.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
            return

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