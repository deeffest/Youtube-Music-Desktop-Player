import pywinstyles
import webbrowser
import sys
import subprocess
import subprocess
import os

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QShortcut, \
    QFileDialog, QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineSettings, \
    QWebEngineScript
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QSettings, QUrl, Qt, QSize, pyqtSlot, QRect, \
    QProcess
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton
from PyQt5.uic import loadUi
from qfluentwidgets import setTheme, setThemeColor, Theme, \
    RoundMenu, Action, SplashScreen, MessageBox
from core.web_engine_view import WebEngineView
from core.web_engine_page import WebEnginePage
from core.settings_dialog import SettingsDialog
from core.about_dialog import AboutDialog
from core.mini_player_dialog import MiniPlayerDialog
from pypresence import Presence
from core.system_tray_icon import SystemTrayIcon
from core.update_checker import UpdateChecker
from packaging import version as pkg_version

class MainWindow(QMainWindow):
    def __init__(self, app_info, parent=None):
        super().__init__(parent)
        self.name = app_info[0]
        self.version = app_info[1]
        self.current_dir = app_info[2]
        self.icon_folder = f"{self.current_dir}/resources/icons"
    
        self.load_settings()
        self.load_ui()
        self.show_splash_screen()
        self.create_webengine()
        self.setup_webchannel()
        self.create_menu()
        self.create_toolbar()
        self.setup_shortcuts()
        self.activate_plugins()
        self.check_updates()
        
        self.mini_player_dialog = MiniPlayerDialog(self)

    def previous_youtube_video(self):
        self.webview.page().runJavaScript(self.read_script("previous_youtube_video.js"))

    def play_pause_youtube_video(self):
        self.webview.page().runJavaScript(self.read_script("play_pause_youtube_video.js"))

    def next_youtube_video(self):
        self.webview.page().runJavaScript(self.read_script("next_youtube_video.js"))

    def setup_webchannel(self):
        self.webchannel = QWebChannel()
        self.webview.page().setWebChannel(self.webchannel)
        self.webchannel.registerObject("backend", self)

    @pyqtSlot(str, str, str)
    def track_info_changed(self, title, author, thumbnail_url):
        if title == '' or author == '' or thumbnail_url == '':
            print("No track is currently playing.")
            self.setWindowTitle("Youtube Music Desktop Player")

            if self.tray_icon is not None:
                self.tray_icon.setToolTip("Youtube Music Desktop Player")

            if self.discord_rpc:
                self.discord_rpc.clear()
        else:
            print(f"Track info changed: Title='{title}', Author='{author}', Thumbnail URL='{thumbnail_url}'")
            self.mini_player_dialog.update_track_info(title, author, thumbnail_url)
            self.update_discord_rpc(title, author, thumbnail_url)
            self.setWindowTitle(f"{title} - Youtube Music Desktop Player")
            if self.tray_icon:
                self.tray_icon.setToolTip(f"{title} - Youtube Music Desktop Player")

    def update_discord_rpc(self, title, author, thumbnail_url):
        if self.discord_rpc:
            try:
                self.discord_rpc.update(
                    details=title,
                    state=author,
                    large_image=thumbnail_url, 
                    small_image="https://music.youtube.com/img/favicon_32.png",
                )
                print("Discord RPC updated.")
            except Exception as e:
                print(f"Error updating Discord RPC: {e}")
        
    @pyqtSlot(str)
    def video_state_changed(self, state):
        print(f"Video state changed: {state}")

        if state == "VideoPlaying":
            self.mini_player_dialog.previous_button.setEnabled(True)
            self.mini_player_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/pause-filled.png"))
            self.mini_player_dialog.play_pause_button.setEnabled(True)
            self.mini_player_dialog.next_button.setEnabled(True)
            
            if self.win_thumbmail_buttons_setting == 1:
                if self.win_thumbnail_toolbar is not None:
                    self.tool_btn_previous.setIcon(
                        QIcon(f"{self.icon_folder}/previous-border.png"))
                    self.tool_btn_play_pause.setIcon(
                        QIcon(f"{self.icon_folder}/pause-border.png"))            
                    self.tool_btn_next.setIcon(
                        QIcon(f"{self.icon_folder}/next-border.png"))
                    self.tool_btn_previous.setEnabled(True)
                    self.tool_btn_play_pause.setEnabled(True)
                    self.tool_btn_next.setEnabled(True)

            if self.tray_icon_setting == 1:
                if self.tray_icon is not None:
                    self.tray_icon.previous_action.setEnabled(True)
                    self.tray_icon.play_pause_action.setIcon(
                            QIcon(f"{self.icon_folder}/pause.png"))
                    self.tray_icon.play_pause_action.setEnabled(True)
                    self.tray_icon.next_action.setEnabled(True)

        elif state == "VideoPaused":
            self.mini_player_dialog.previous_button.setEnabled(True)
            self.mini_player_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled.png"))
            self.mini_player_dialog.play_pause_button.setEnabled(True)
            self.mini_player_dialog.next_button.setEnabled(True)
                
            if self.win_thumbmail_buttons_setting == 1:
                if self.win_thumbnail_toolbar is not None:
                    self.tool_btn_previous.setIcon(
                        QIcon(f"{self.icon_folder}/previous-border.png"))
                    self.tool_btn_play_pause.setIcon(
                        QIcon(f"{self.icon_folder}/play-border.png"))            
                    self.tool_btn_next.setIcon(
                        QIcon(f"{self.icon_folder}/next-border.png"))
                    self.tool_btn_previous.setEnabled(True)
                    self.tool_btn_play_pause.setEnabled(True)
                    self.tool_btn_next.setEnabled(True)

            if self.tray_icon_setting == 1:
                if self.tray_icon is not None:
                    self.tray_icon.previous_action.setEnabled(True)
                    self.tray_icon.play_pause_action.setIcon(
                            QIcon(f"{self.icon_folder}/play.png"))
                    self.tray_icon.play_pause_action.setEnabled(True)
                    self.tray_icon.next_action.setEnabled(True)

        elif state == "NoVideo":
            self.mini_player_dialog.previous_button.setEnabled(False)
            self.mini_player_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled.png"))
            self.mini_player_dialog.play_pause_button.setEnabled(False)
            self.mini_player_dialog.next_button.setEnabled(False)
            
            if self.win_thumbmail_buttons_setting == 1:
                if self.win_thumbnail_toolbar is not None:
                    self.tool_btn_previous.setIcon(
                        QIcon(f"{self.icon_folder}/previous-border-disabled.png"))
                    self.tool_btn_play_pause.setIcon(
                        QIcon(f"{self.icon_folder}/play-border-disabled.png"))            
                    self.tool_btn_next.setIcon(
                        QIcon(f"{self.icon_folder}/next-border-disabled.png"))
                    self.tool_btn_previous.setEnabled(False)
                    self.tool_btn_play_pause.setEnabled(False)
                    self.tool_btn_next.setEnabled(False)

            if self.tray_icon_setting == 1:
                if self.tray_icon is not None:
                    self.tray_icon.previous_action.setEnabled(False)
                    self.tray_icon.play_pause_action.setIcon(
                            QIcon(f"{self.icon_folder}/play.png"))
                    self.tray_icon.play_pause_action.setEnabled(False)
                    self.tray_icon.next_action.setEnabled(False)

    def show_splash_screen(self):
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(102, 102))
        self.splash_screen.titleBar.hide()

        self.show()

    def activate_plugins(self):
        if self.youtube_ad_blocker_setting == 1:
            self.youtube_ad_blocker_plugin = QWebEngineScript()
            self.youtube_ad_blocker_plugin.setName("YoutubeAdBlocker")
            self.youtube_ad_blocker_plugin.setSourceCode(self.read_script("youtube_ad_blocker.js"))
            self.youtube_ad_blocker_plugin.setInjectionPoint(QWebEngineScript.DocumentReady)
            self.youtube_ad_blocker_plugin.setWorldId(QWebEngineScript.ApplicationWorld)
            self.youtube_ad_blocker_plugin.setRunsOnSubFrames(True)
            self.webpage.profile().scripts().insert(self.youtube_ad_blocker_plugin)

        scrollbar_stylizer_plugin = QWebEngineScript()
        scrollbar_stylizer_plugin.setName("ScrollbarStylizer")
        scrollbar_stylizer_plugin.setSourceCode(self.read_script("scrollbar_stylizer.js"))
        scrollbar_stylizer_plugin.setInjectionPoint(QWebEngineScript.DocumentReady)
        scrollbar_stylizer_plugin.setWorldId(QWebEngineScript.ApplicationWorld)
        scrollbar_stylizer_plugin.setRunsOnSubFrames(True)
        self.webpage.profile().scripts().insert(scrollbar_stylizer_plugin)

        if self.discord_rpc_setting == 1:
            self.discord_rpc = Presence("1254202610781655050")
            try:
                self.discord_rpc.connect()
            except Exception as e:
                self.discord_rpc = None
        else:
            self.discord_rpc = None

        youtube_music_player_observer_plugin = QWebEngineScript()
        youtube_music_player_observer_plugin.setName("YoutubeMusicPlayerObserver")
        youtube_music_player_observer_plugin.setSourceCode(
            self.read_script("youtube_music_player_observer.js"))
        youtube_music_player_observer_plugin.setInjectionPoint(QWebEngineScript.Deferred)
        youtube_music_player_observer_plugin.setWorldId(QWebEngineScript.MainWorld)
        youtube_music_player_observer_plugin.setRunsOnSubFrames(True)
        self.webpage.profile().scripts().insert(youtube_music_player_observer_plugin)

        if self.win_thumbmail_buttons_setting == 1:
            self.win_thumbnail_toolbar = QWinThumbnailToolBar(self)
            
            self.tool_btn_previous = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
            self.tool_btn_previous.setToolTip('Previous')
            self.tool_btn_previous.setEnabled(False)
            self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-border-disabled.png"))
            self.tool_btn_previous.clicked.connect(self.previous_youtube_video)
            self.win_thumbnail_toolbar.addButton(self.tool_btn_previous)

            self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
            self.tool_btn_play_pause.setToolTip('Play/Pause')
            self.tool_btn_play_pause.setEnabled(False)
            self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/pause-border-disabled.png"))  
            self.tool_btn_play_pause.clicked.connect(self.play_pause_youtube_video)                   
            self.win_thumbnail_toolbar.addButton(self.tool_btn_play_pause)

            self.tool_btn_next = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
            self.tool_btn_next.setToolTip('Next')
            self.tool_btn_next.setEnabled(False)
            self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-border-disabled.png"))
            self.tool_btn_next.clicked.connect(self.next_youtube_video)
            self.win_thumbnail_toolbar.addButton(self.tool_btn_next)

            self.win_thumbnail_toolbar.setWindow(self.windowHandle())
        else:
            self.win_thumbnail_toolbar = None

        if self.tray_icon_setting == 1:
            self.tray_icon = SystemTrayIcon(self.windowIcon(), self)
            self.tray_icon.show()
        else:
            self.tray_icon = None

    def read_script(self, filename):
        with open(f"{self.current_dir}/core/js/{filename}", "r", encoding='utf-8') as f:
            return f.read()

    def load_settings(self):
        self.settings = QSettings("deeffest", self.name)

        self.youtube_ad_blocker_setting = int(self.settings.value("ad_blocker", 0))
        self.save_last_win_size_setting = int(self.settings.value("save_last_win_size", 1))
        self.open_last_url_at_startup_setting = int(self.settings.value("open_last_url_at_startup", 1))
        self.last_url_setting = self.settings.value("last_url", "https://music.youtube.com/")
        self.fullscreen_mode_support_setting = int(self.settings.value("fullscreen_mode_support", 1))
        self.support_animated_scrolling_setting = int(self.settings.value("support_animated_scrolling", 0))
        self.save_last_pos_of_mp_setting = int(self.settings.value("save_last_pos_of_mp", 1))
        self.last_win_size_setting = self.settings.value("last_win_size", QSize(1080, 600))
        self.save_last_zoom_factor_setting = int(self.settings.value("save_last_zoom_factor", 1))
        self.last_zoom_factor_setting = float(self.settings.value("last_zoom_factor", 1.0))
        self.last_download_folder_setting = self.settings.value("last_download_folder", self.current_dir)
        self.discord_rpc_setting = int(self.settings.value("discord_rpc", 0))
        self.save_geometry_of_mp_setting = int(self.settings.value("save_geometry_of_mp", 1))
        self.geometry_of_mp_setting = self.settings.value("geometry_of_mp", QRect(30, 60, 360, 150))
        self.win_thumbmail_buttons_setting = int(self.settings.value("win_thumbmail_buttons", 1))
        self.tray_icon_setting = int(self.settings.value("tray_icon", 0))

    def setup_shortcuts(self):
        shortcuts = {
            Qt.ALT + Qt.Key_Left: self.back,
            Qt.ALT + Qt.Key_Right: self.forward,
            Qt.CTRL + Qt.Key_H: self.home,
            Qt.CTRL + Qt.Key_R: self.reload,
            Qt.CTRL + Qt.Key_D: self.download_mp3,
            Qt.CTRL + Qt.SHIFT + Qt.Key_D: self.download_mp4,
            Qt.CTRL + Qt.Key_A: self.download_with_custom_args,
            Qt.CTRL + Qt.Key_M: self.open_mini_player,
            Qt.CTRL + Qt.Key_S: self.open_settings,
        }
        for key, value in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(value)

    def back(self):
        self.webview.back()

    def forward(self):
        self.webview.forward()

    def home(self):
        self.webview.load(QUrl("https://music.youtube.com/"))

    def reload(self):
        self.webview.reload()

    def download_mp3(self):
        if "watch" in self.webview.url().toString():
            try:
                self.download_mp3_track()
            except Exception as e:
                print(e)
        elif "playlist" in self.webview.url().toString():
            try:
                self.download_mp3_playlist()
            except Exception as e:
                print(e)

    def download_mp4(self):
        if "watch" in self.webview.url().toString():
            try:
                self.download_mp4_track()
            except Exception as e:
                print(e)
        elif "playlist" in self.webview.url().toString():
            try:
                self.download_mp4_playlist()
            except Exception as e:
                print(e)

    def select_download_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", 
                                                  self.last_download_folder_setting)
        return folder if folder else None

    def download_mp3_track(self):
        url = self.webview.url().toString()
        clean_url = url.split('&list')[0]

        download_folder = self.select_download_folder()
        if download_folder is None:
            return
        self.last_download_folder_setting = download_folder
        self.settings.setValue("last_download_folder", download_folder)

        yt_dlp_path = os.path.join(self.current_dir, "bin/yt-dlp.exe")
        CREATE_NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE

        subprocess.Popen(
            [yt_dlp_path,
            "-U",
            "-x", 
            "--audio-format", "mp3", 
            "--audio-quality","0",
            "-o", f"{download_folder}/%(title)s.%(ext)s", 
            clean_url],
            creationflags=CREATE_NEW_CONSOLE
        )

    def download_mp3_playlist(self):
        url = self.webview.url().toString()
        playlist_id = url.split('list=')[-1]

        download_folder = self.select_download_folder()
        if download_folder is None:
            return
        self.last_download_folder = download_folder
        self.settings.setValue("last_download_folder", download_folder)        
        
        playlist_folder = os.path.join(download_folder, f"Playlist_{playlist_id}")
        os.makedirs(playlist_folder, exist_ok=True)

        yt_dlp_path = os.path.join(self.current_dir, "bin/yt-dlp.exe")
        CREATE_NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE

        subprocess.Popen(
            [yt_dlp_path,
            "-U",
            "-x",
            "--audio-format", "mp3", 
            "--audio-quality", "0",
            "-o", f"{playlist_folder}/%(title)s.%(ext)s", 
            url],
            creationflags=CREATE_NEW_CONSOLE
        )

    def download_mp4_track(self):
        url = self.webview.url().toString()
        clean_url = url.split('&list')[0]

        download_folder = self.select_download_folder()
        if download_folder is None:
            return
        self.last_download_folder = download_folder
        self.settings.setValue("last_download_folder", download_folder)

        yt_dlp_path = os.path.join(self.current_dir, "bin/yt-dlp.exe")
        CREATE_NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE

        subprocess.Popen(
            [yt_dlp_path,
            "-U",
            "-f", "best[ext=mp4]",
            "--merge-output-format", "mp4",
            "-o", f"{download_folder}/%(title)s.%(ext)s", 
            clean_url],
            creationflags=CREATE_NEW_CONSOLE
        )

    def download_mp4_playlist(self):
        url = self.webview.url().toString()
        playlist_id = url.split('list=')[-1]

        download_folder = self.select_download_folder()
        if download_folder is None:
            return
        self.last_download_folder = download_folder
        self.settings.setValue("last_download_folder", download_folder)        

        playlist_folder = os.path.join(download_folder, f"Playlist_{playlist_id}")
        os.makedirs(playlist_folder, exist_ok=True)

        yt_dlp_path = os.path.join(self.current_dir, "bin/yt-dlp.exe")
        CREATE_NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE

        subprocess.Popen(
            [yt_dlp_path,
            "-U",
            "-f", "best[ext=mp4]",
            "--merge-output-format", "mp4",
            "-o", f"{playlist_folder}/%(title)s.%(ext)s", 
            url],
            creationflags=CREATE_NEW_CONSOLE
        )

    def download_with_custom_args(self):
        CREATE_NEW_CONSOLE = subprocess.CREATE_NEW_CONSOLE
        try:
            subprocess.Popen(
                ["cmd.exe", "/K", "yt-dlp.exe --help"],
                creationflags=CREATE_NEW_CONSOLE,
                cwd=self.current_dir + "/bin"
            )
        except Exception as e:
            print(e)

    def open_mini_player(self):
        if "watch" in self.webview.url().toString():
            pywinstyles.apply_style(self.mini_player_dialog, "dark")
            self.mini_player_dialog.show()
            self.hide()
            if self.tray_icon is not None:
                self.tray_icon.hide()

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()
        
    def create_toolbar(self):
        self.back_tbutton.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_tbutton.clicked.connect(self.webview.back)

        self.forward_tbutton.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_tbutton.clicked.connect(self.webview.forward)

        self.home_tbutton.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_tbutton.clicked.connect(self.home)

        self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_tbutton.clicked.connect(self.webview.reload)

        self.download_stbutton.setIcon(QIcon(f"{self.icon_folder}/download.png"))
        self.download_stbutton.setFlyout(self.download_menu)
        self.download_stbutton.clicked.connect(self.download_mp3)

        self.mini_player_tbutton.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_tbutton.clicked.connect(self.open_mini_player)

        self.settings_tbutton.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_tbutton.clicked.connect(self.open_settings)

    def create_menu(self):
        self.back_action = Action("Back", shortcut="Alt+Left")
        self.back_action.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_action.triggered.connect(self.webview.back)

        self.forward_action = Action("Forward", shortcut="Alt+Right")
        self.forward_action.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_action.triggered.connect(self.webview.forward)

        self.home_action = Action("Home", shortcut="Ctrl+H")
        self.home_action.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_action.triggered.connect(self.home)

        self.reload_action = Action("Reload", shortcut="Ctrl+R")
        self.reload_action.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_action.triggered.connect(self.webview.reload)

        self.download_menu = RoundMenu("Download...")
        self.download_menu.setIcon(QIcon(f"{self.icon_folder}/download.png"))

        self.mp3_track_playlist_action = Action("MP3 Track/Playlist", shortcut="Ctrl+D")
        self.mp3_track_playlist_action.setIcon(QIcon(f"{self.icon_folder}/track.png"))
        self.mp3_track_playlist_action.triggered.connect(self.download_mp3)

        self.mp4_track_playlist_action = Action("MP4 Track/Playlist", shortcut="Ctrl+Shift+D")
        self.mp4_track_playlist_action.setIcon(QIcon(f"{self.icon_folder}/video.png"))
        self.mp4_track_playlist_action.triggered.connect(self.download_mp4)

        self.custom_args_action = Action("Custom args...", shortcut="Ctrl+A")
        self.custom_args_action.setIcon(QIcon(f"{self.icon_folder}/cmd.png"))
        self.custom_args_action.triggered.connect(self.download_with_custom_args)

        self.mini_player_action = Action("Mini-Player", shortcut="Ctrl+M")
        self.mini_player_action.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_action.triggered.connect(self.open_mini_player)

        self.settings_action = Action("Settings", shortcut="Ctrl+S")
        self.settings_action.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_action.triggered.connect(self.open_settings)

        self.bug_report_action = Action("Bug Report")
        self.bug_report_action.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_action.triggered.connect(self.bug_report)

        self.about_app_action = Action("About...")
        self.about_app_action.setIcon(QIcon(f"{self.icon_folder}/about.png"))
        self.about_app_action.triggered.connect(self.about_app)

        self.copy_action = Action("Copy", shortcut="Ctrl+C")
        self.copy_action.setIcon(QIcon(f"{self.icon_folder}/copy.png"))
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = Action("Paste", shortcut="Ctrl+V")
        self.paste_action.setIcon(QIcon(f"{self.icon_folder}/paste.png"))
        self.paste_action.triggered.connect(self.paste)

        self.main_menu = RoundMenu(self)
        self.edit_menu = RoundMenu(self)

        self.main_menu.addAction(self.back_action)
        self.main_menu.addAction(self.forward_action)
        self.main_menu.addAction(self.home_action)
        self.main_menu.addAction(self.reload_action)
        self.main_menu.addSeparator()
        self.main_menu.addMenu(self.download_menu)

        self.main_menu.addAction(self.mini_player_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.settings_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.bug_report_action)
        self.main_menu.addAction(self.about_app_action)        
        
        self.download_menu.addAction(self.mp3_track_playlist_action)
        self.download_menu.addAction(self.mp4_track_playlist_action)
        self.download_menu.addSeparator()
        self.download_menu.addAction(self.custom_args_action)

        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)

    def about_app(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def bug_report(self):
        webbrowser.open_new_tab(
            "https://github.com/deeffest/Youtube-Music-Desktop-Player/issues/new/choose")

    def copy(self):
        self.webpage.triggerAction(QWebEnginePage.Copy)

    def paste(self):
        self.webpage.triggerAction(QWebEnginePage.Paste)

    def create_webengine(self):
        self.webview = WebEngineView(self)
        self.webpage = WebEnginePage(self)
        self.websettings = QWebEngineSettings.globalSettings()
        self.webview.setPage(self.webpage)
        if self.open_last_url_at_startup_setting == 1:
            self.webview.load(QUrl(self.last_url_setting))
        else:
            self.home()
        self.webview.urlChanged.connect(self.url_changed)
        self.webview.loadProgress.connect(self.load_progress)
        self.websettings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, 
                                      self.fullscreen_mode_support_setting)
        self.websettings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled,
                                      self.support_animated_scrolling_setting)
        if self.save_last_zoom_factor_setting == 1:
            self.webview.setZoomFactor(self.last_zoom_factor_setting)
        self.webpage.fullScreenRequested.connect(self.handle_fullscreen)
        self.main_layout.addWidget(self.webview)

    def load_progress(self, progress):
        if progress > 80:
            if self.splash_screen:
                self.splash_screen.hide()
                self.splash_screen = None

    def handle_fullscreen(self, request):
        request.accept()
        if not self.isFullScreen():
            self.toolbar_frame.hide()
            self.showFullScreen()
        else:
            self.toolbar_frame.show()
            self.showNormal()

    def url_changed(self, url):
        self.LineEdit.setText(url.toString())

        if url.toString() == "https://music.youtube.com/":
            self.home_tbutton.setIcon(QIcon(f"{self.icon_folder}/home-filled.png"))
        else:
            self.home_tbutton.setIcon(QIcon(f"{self.icon_folder}/home.png"))

        self.back_action.setEnabled(self.webview.history().canGoBack())
        self.back_tbutton.setEnabled(self.webview.history().canGoBack())
        self.forward_action.setEnabled(self.webview.history().canGoForward())
        self.forward_tbutton.setEnabled(self.webview.history().canGoForward())

        self.mp3_track_playlist_action.setEnabled(
            "watch" in url.toString() or "playlist" in url.toString())
        self.mp4_track_playlist_action.setEnabled(
            "watch" in url.toString() or "playlist" in url.toString())
        self.download_stbutton.setEnabled("watch" in url.toString() or "playlist" in url.toString())
        self.mini_player_action.setEnabled("watch" in url.toString())
        self.mini_player_tbutton.setEnabled("watch" in url.toString())

        self.last_url_setting = self.webview.url().toString()
        self.settings.setValue("last_url", self.last_url_setting)

    def check_updates(self):
        self.update_checker = UpdateChecker()
        self.update_checker.update_checked.connect(self.handle_update_checked)
        self.update_checker.start()
        
    def handle_update_checked(self, version, download, notes):
        if pkg_version.parse(self.version) < pkg_version.parse(version):
            w = MessageBox(f"A new update {version} is available!", notes, self)
            w.yesButton.setText("Download")
            w.cancelButton.setText("Later")
            if w.exec_():
                webbrowser.open_new_tab(download)
                self.exit_app()

    def load_ui(self):
        pywinstyles.apply_style(self, "dark")
        setTheme(Theme.DARK)
        setThemeColor("red")
        loadUi(f"{self.current_dir}/core/ui/main_window.ui", self)
        self.setWindowTitle("Youtube Music Desktop Player")
        self.setWindowIcon(QIcon(f"{self.icon_folder}/icon.ico"))
        if self.save_last_win_size_setting == 1:
            self.resize(self.last_win_size_setting)
        else:
            self.resize(1080, 600)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def restart_app(self):
        self.save_settings()
        QApplication.quit()
        QProcess.startDetached(sys.executable, sys.argv)

    def save_settings(self):
        self.last_win_size_setting = self.size()
        self.settings.setValue("last_win_size", self.last_win_size_setting)
        
        self.last_zoom_factor_setting = self.webview.zoomFactor()
        self.settings.setValue("last_zoom_factor", self.last_zoom_factor_setting)

    def exit_app(self):
        self.save_settings()
        sys.exit(0)

    def hide_show_window(self):
        if self.isMinimized():
            self.showNormal()
            self.activateWindow()
        else:
            if self.isMinimized():
                self.showNormal()
                self.activateWindow()
            elif self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.activateWindow()

    def closeEvent(self, event):
        if self.tray_icon_setting == 1 and self.tray_icon is not None:
            event.ignore()
            self.hide()
        else:
            if "watch" in self.webview.url().toString():
                self.showNormal()
                self.activateWindow()
                w = MessageBox(f"Exit confirmation ✕", 
                            "Do you really want to stop the current playback and exit the app?", self)
                w.yesButton.setText("Yes")
                w.cancelButton.setText("No")
                if w.exec_() == True:
                    self.save_settings()
                    event.accept()
                else:
                    event.ignore()
            else:
                self.save_settings()
                event.accept()