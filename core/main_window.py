import logging
import os
import webbrowser

import pypresence
import pywinstyles
from PyQt5.QtCore import QUrl, Qt, QSize, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineSettings, QWebEngineScript
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QFileDialog, QMainWindow, QShortcut
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton
from PyQt5.uic import loadUi
from qfluentwidgets import (
    Action, InfoBar, InfoBarPosition, MessageBox, PushButton, RoundMenu, 
    SplashScreen, ToolTipFilter, ToolTipPosition, Theme, setTheme, setThemeColor
)
from packaging import version as pkg_version
from win10toast import ToastNotifier

from core.about_dialog import AboutDialog
from core.mini_player_dialog import MiniPlayerDialog
from core.settings_dialog import SettingsDialog
from core.system_tray_icon import SystemTrayIcon
from core.update_checker import UpdateChecker
from core.web_channel_backend import WebChannelBackend
from core.web_engine_page import WebEnginePage
from core.web_engine_view import WebEngineView
from core.ytmusic_downloader import DownloadThread

class MainWindow(QMainWindow):
    oauth_completed = pyqtSignal()
    def __init__(self, app_settings, opengl_enviroment_setting, app_info, parent=None):
        super().__init__(parent)
        self.name = app_info[0]
        self.version = app_info[1]
        self.current_dir = app_info[2]
        self.icon_folder = f"{self.current_dir}/resources/icons"
        self.title = "Unknown"
        self.author = "Unknown"
        self.thumbnail_url = None
        self.video_state = None
        self.mini_player_dialog = None
        self.force_exit = False
        self.is_downloading = False
        self.is_video_or_playlist = False
        self.current_url = None
        self.like_status = None
        self.current_time = "NaN"
        self.total_time = "NaN"
        self.settings_ = app_settings
        self.opengl_enviroment_setting = opengl_enviroment_setting
    
        self.load_settings()
        self.load_ui()
        self.setup_shortcuts()
        self.show_splash_screen()
        self.create_webengine()
        self.setup_webchannel()
        self.create_menu()
        self.create_toolbar()
        self.activate_plugins()

    def load_settings(self):
        if self.settings_.value("ad_blocker") is None:
            self.settings_.setValue("ad_blocker", 1)
        if self.settings_.value("save_last_win_geometry") is None:
            self.settings_.setValue("save_last_win_geometry", 1)
        if self.settings_.value("open_last_url_at_startup") is None:
            self.settings_.setValue("open_last_url_at_startup", 1)
        if self.settings_.value("last_url") is None:
            self.settings_.setValue("last_url", "https://music.youtube.com/")
        if self.settings_.value("fullscreen_mode_support") is None:
            self.settings_.setValue("fullscreen_mode_support", 1)
        if self.settings_.value("support_animated_scrolling") is None:
            self.settings_.setValue("support_animated_scrolling", 0)
        if self.settings_.value("save_last_pos_of_mp") is None:
            self.settings_.setValue("save_last_pos_of_mp", 1)
        if self.settings_.value("last_win_geometry") is None:
            self.settings_.setValue("last_win_geometry", QRect(self.get_centered_geometry(1000, 580)))
        if self.settings_.value("save_last_zoom_factor") is None:
            self.settings_.setValue("save_last_zoom_factor", 1)
        if self.settings_.value("last_zoom_factor") is None:
            self.settings_.setValue("last_zoom_factor", 1.0)
        if self.settings_.value("last_download_folder") is None:
            self.settings_.setValue("last_download_folder", self.current_dir)
        if self.settings_.value("discord_rpc") is None:
            self.settings_.setValue("discord_rpc", 0)
        if self.settings_.value("save_geometry_of_mp") is None:
            self.settings_.setValue("save_geometry_of_mp", 1)
        if self.settings_.value("geometry_of_mp") is None:
            self.settings_.setValue("geometry_of_mp", QRect(self.get_centered_geometry(360, 150)))
        if self.settings_.value("win_thumbmail_buttons") is None:
            self.settings_.setValue("win_thumbmail_buttons", 1)
        if self.settings_.value("tray_icon") is None:
            self.settings_.setValue("tray_icon", 1)
        if self.settings_.value("proxy_type") is None:
            self.settings_.setValue("proxy_type", "NoProxy")
        if self.settings_.value("proxy_host_name") is None:
            self.settings_.setValue("proxy_host_name", "")
        if self.settings_.value("proxy_port") is None:
            self.settings_.setValue("proxy_port", "")
        if self.settings_.value("proxy_login") is None:
            self.settings_.setValue("proxy_login", "")
        if self.settings_.value("proxy_password") is None:
            self.settings_.setValue("proxy_password", "")
        if self.settings_.value("track_change_notificator") is None:
            self.settings_.setValue("track_change_notificator", 0)
        if self.settings_.value("hotkey_playback_control") is None:
            self.settings_.setValue("hotkey_playback_control", 1)
        if self.settings_.value("only_audio_mode") is None:
            self.settings_.setValue("only_audio_mode", 0)

        self.ad_blocker_setting = int(self.settings_.value("ad_blocker"))
        self.save_last_win_geometry_setting = int(self.settings_.value("save_last_win_geometry"))
        self.open_last_url_at_startup_setting = int(self.settings_.value("open_last_url_at_startup"))
        self.last_url_setting = self.settings_.value("last_url")
        self.fullscreen_mode_support_setting = int(self.settings_.value("fullscreen_mode_support"))
        self.support_animated_scrolling_setting = int(self.settings_.value("support_animated_scrolling"))
        self.save_last_pos_of_mp_setting = int(self.settings_.value("save_last_pos_of_mp"))
        self.last_win_geometry_setting = self.settings_.value("last_win_geometry")
        self.save_last_zoom_factor_setting = int(self.settings_.value("save_last_zoom_factor"))
        self.last_zoom_factor_setting = float(self.settings_.value("last_zoom_factor"))
        self.last_download_folder_setting = self.settings_.value("last_download_folder")
        self.discord_rpc_setting = int(self.settings_.value("discord_rpc"))
        self.save_geometry_of_mp_setting = int(self.settings_.value("save_geometry_of_mp"))
        self.geometry_of_mp_setting = self.settings_.value("geometry_of_mp")
        self.win_thumbmail_buttons_setting = int(self.settings_.value("win_thumbmail_buttons"))
        self.tray_icon_setting = int(self.settings_.value("tray_icon"))
        self.proxy_type_setting = self.settings_.value("proxy_type")
        self.proxy_host_name_setting = self.settings_.value("proxy_host_name")
        self.proxy_port_setting = self.settings_.value("proxy_port")
        self.proxy_login_setting = self.settings_.value("proxy_login")
        self.proxy_password_setting = self.settings_.value("proxy_password")
        self.track_change_notificator_setting = int(self.settings_.value("track_change_notificator"))
        self.hotkey_playback_control_setting = int(self.settings_.value("hotkey_playback_control"))
        self.only_audio_mode_setting = int(self.settings_.value("only_audio_mode"))

    def load_ui(self):
        try:
            pywinstyles.apply_style(self, "dark")
        except Exception as e:
            logging.error("Failed to apply dark style: " + str(e))
        setTheme(Theme.DARK)
        setThemeColor("red")
        
        loadUi(f"{self.current_dir}/core/ui/main_window.ui", self)
        
        self.setWindowTitle("Youtube Music Desktop Player")
        self.setWindowIcon(QIcon(f"{self.icon_folder}/icon.ico"))
        
        if self.save_last_win_geometry_setting == 1:
            self.setGeometry(self.last_win_geometry_setting)
        else:
            self.setGeometry(self.get_centered_geometry(1000, 560))

    def get_centered_geometry(self, width, height):
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - width) // 2 
        y = (screen_geometry.height() - height) // 2
        return QRect(x, y, width, height)

    def show_splash_screen(self):
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(102, 102))
        self.splash_screen.titleBar.hide()

        self.show()

    def create_webengine(self):
        self.webview = WebEngineView(self)
        self.webpage = WebEnginePage(self)
        self.websettings = QWebEngineSettings.globalSettings()
        self.webview.setPage(self.webpage)

        self.set_application_proxy()
        
        if self.open_last_url_at_startup_setting == 1:
            self.webview.load(QUrl(self.last_url_setting))
        else:
            self.home()
            
        self.webview.urlChanged.connect(self.url_changed)
        self.webview.loadProgress.connect(self.load_progress)
        self.webpage.fullScreenRequested.connect(self.handle_fullscreen)
        
        self.websettings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, self.fullscreen_mode_support_setting)
        self.websettings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, self.support_animated_scrolling_setting)
        
        if self.save_last_zoom_factor_setting == 1:
            self.webview.setZoomFactor(self.last_zoom_factor_setting)
            
        self.MainLayout.addWidget(self.webview)
        self.webview.setFocus()

    def set_application_proxy(self):
        try:
            proxy = QNetworkProxy()
        
            if self.proxy_type_setting == "HttpProxy":
                proxy.setType(QNetworkProxy.HttpProxy)
            elif self.proxy_type_setting == "Socks5Proxy":
                proxy.setType(QNetworkProxy.Socks5Proxy)
            elif self.proxy_type_setting == "DefaultProxy":
                proxy.setType(QNetworkProxy.DefaultProxy)
                return
            else:
                proxy.setType(QNetworkProxy.NoProxy)
                return
            
            if self.proxy_host_name_setting:
                proxy.setHostName(self.proxy_host_name_setting)
            else:
                raise ValueError("Proxy host name is not set.")
            
            if self.proxy_port_setting:
                if not (1 <= self.proxy_port_setting <= 65535):
                    raise ValueError("Proxy port is out of range (1-65535).")
                proxy.setPort(self.proxy_port_setting)
            else:
                raise ValueError("Proxy port is not set.")
            
            if self.proxy_login_setting:
                proxy.setUser(self.proxy_login_setting)
            if self.proxy_password_setting:
                proxy.setPassword(self.proxy_password_setting)

            QNetworkProxy.setApplicationProxy(proxy)
        except Exception as e:
            logging.error(f"Failed to set application proxy: {str(e)}")

    def load_progress(self, progress):
        if progress > 80 and self.splash_screen:
            if self.isHidden():
                self.showNormal()
                self.activateWindow()

            self.splash_screen.finish()
            self.splash_screen = None
            
            self.check_updates()

    def check_updates(self):
        self.update_checker = UpdateChecker()
        self.update_checker.update_checked.connect(self.handle_update_checked)
        self.update_checker.start()
        
    def handle_update_checked(self, last_version, title, whats_new, last_release_url):
        if pkg_version.parse(self.version) < pkg_version.parse(last_version):
            msg_box = MessageBox(
                title, 
                whats_new, 
                self)
            msg_box.yesButton.setText("Download")
            msg_box.cancelButton.setText("Later")
            if msg_box.exec_():
                webbrowser.open_new_tab(last_release_url)
                self.force_exit = True
                self.close()

    def setup_shortcuts(self):
        self.back_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Left), self)
        self.back_shortcut.activated.connect(self.back)

        self.forward_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Right), self)
        self.forward_shortcut.activated.connect(self.forward)

        self.home_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_H), self)
        self.home_shortcut.activated.connect(self.home)

        self.reload_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self)
        self.reload_shortcut.activated.connect(self.reload)

        self.download_with_oauth_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_D), self)
        self.download_with_oauth_shortcut.setEnabled(False)
        self.download_with_oauth_shortcut.activated.connect(lambda: self.download(use_oauth=True))

        self.download_as_unauthorized_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), self)
        self.download_as_unauthorized_shortcut.setEnabled(False)
        self.download_as_unauthorized_shortcut.activated.connect(lambda: self.download(use_oauth=False))

        self.mini_player_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), self)
        self.mini_player_shortcut.setEnabled(False)
        self.mini_player_shortcut.activated.connect(self.mini_player)

        self.settings_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.settings_shortcut.activated.connect(self.settings)

    def handle_fullscreen(self, request):
        if not self.isFullScreen():
            self.ToolBar.hide()
            self.showFullScreen()
        else:
            self.ToolBar.show()
            self.showNormal()
            
        request.accept()

    def url_changed(self, url):
        self.current_url = url.toString()
        self.LineEdit.setText(self.current_url)

        can_go_back = self.webview.history().canGoBack()
        can_go_forward = self.webview.history().canGoForward()
        self.back_action.setEnabled(can_go_back)
        self.back_tbutton.setEnabled(can_go_back)
        self.forward_action.setEnabled(can_go_forward)
        self.forward_tbutton.setEnabled(can_go_forward)

        self.is_video_or_playlist = ("watch" in self.current_url or "playlist" in self.current_url)

        if not self.is_downloading:
            self.download_with_oauth_action.setEnabled(self.is_video_or_playlist)
            self.download_as_unauthorized_action.setEnabled(self.is_video_or_playlist)
            self.download_with_oauth_shortcut.setEnabled(self.is_video_or_playlist)
            self.download_as_unauthorized_shortcut.setEnabled(self.is_video_or_playlist)

    def setup_webchannel(self):
        self.webchannel_backend = WebChannelBackend(self)

        self.webchannel = QWebChannel()
        self.webpage.setWebChannel(self.webchannel)
        self.webchannel.registerObject("backend", self.webchannel_backend)

    @pyqtSlot(str)
    def like_status_changed(self, status):
        if status != "":
            self.like_status = status
        else:
            self.like_status = None

        self.update_mini_player_like_dislike_controls()
    
    def update_mini_player_like_dislike_controls(self):
        if self.mini_player_dialog:
            if self.like_status == "Like":
                self.mini_player_dialog.like_button.setIcon(QIcon(f"{self.icon_folder}/like-filled.png"))
                self.mini_player_dialog.dislike_button.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))
            elif self.like_status == "Dislike":
                self.mini_player_dialog.like_button.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.mini_player_dialog.dislike_button.setIcon(QIcon(f"{self.icon_folder}/dislike-filled.png"))
            else:
                self.mini_player_dialog.like_button.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.mini_player_dialog.dislike_button.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))

    @pyqtSlot(str, str, str)
    def track_info_changed(self, title, author, thumbnail_url):
        self.title = title
        self.author = author
        self.thumbnail_url = thumbnail_url

        is_empty = not self.title or not self.author or not self.thumbnail_url
        window_title = "Youtube Music Desktop Player" if is_empty else f"{self.title} - Youtube Music Desktop Player"
        self.setWindowTitle(window_title)
        
        if self.tray_icon:
            self.tray_icon.setToolTip(window_title)

        if not is_empty and self.track_change_notificator_setting and self.track_notifier is not None:
            self.track_notifier.show_toast(
                self.title,
                self.author,
                duration=5,
                icon_path=f"{self.icon_folder}/music-notify.ico",
                threaded=True
            )
        
        if is_empty:
            self.clear_discord_rpc()
        else:
            self.update_mini_player_track_info()
            self.update_discord_rpc()

    def update_mini_player_track_info(self):
        if self.mini_player_dialog:
            self.mini_player_dialog.title_label.setText(self.title)
            self.mini_player_dialog.title_label.setToolTip(self.title)
            self.mini_player_dialog.author_label.setText(self.author)
            self.mini_player_dialog.author_label.setToolTip(self.author)
            self.mini_player_dialog.load_thumbnail(self.thumbnail_url)

    def update_discord_rpc(self):
        if self.discord_rpc:
            details = self.title[:128]
            state = self.author[:128]
            large_image = self.thumbnail_url
            small_image = "https://music.youtube.com/img/favicon_48.png"

            try:
                self.discord_rpc.update(
                    details=details,
                    state=state,
                    large_image=large_image,
                    small_image=small_image,
                    activity_type=pypresence.ActivityType.LISTENING
                )
            except Exception as e:
                logging.error(f"An error occurred while updating Discord RPC: {str(e)}")
                self.reconnect_discord_rpc(retry_update=True)

    def reconnect_discord_rpc(self, retry_update=False):
        if self.discord_rpc:
            try:
                self.discord_rpc.connect()
                if retry_update:
                    self.update_discord_rpc()
            except Exception as e:
                logging.error(f"An error occurred while reconnecting to Discord RPC: {str(e)}")

    def clear_discord_rpc(self):
        if self.discord_rpc:
            try:
                self.discord_rpc.clear()
            except Exception as e:
                logging.error(f"An error occurred while clearing Discord RPC: {str(e)}")

    @pyqtSlot(str, str)
    def track_progress_changed(self, current_time, total_time):
        self.current_time = current_time
        self.total_time = total_time

        self.update_mini_player_track_progress()

    def update_mini_player_track_progress(self):
        if self.mini_player_dialog:
            self.mini_player_dialog.BodyLabel.setText(self.current_time)
            self.mini_player_dialog.BodyLabel_2.setText(self.total_time)

    @pyqtSlot(str)
    def video_state_changed(self, state):
        self.video_state = state

        if self.video_state == "VideoPlaying" or self.video_state == "VideoPaused":
            self.mini_player_action.setEnabled(True)
            self.mini_player_tbutton.setEnabled(True)
            self.mini_player_shortcut.setEnabled(True)
        else:
            self.mini_player_action.setEnabled(False)
            self.mini_player_tbutton.setEnabled(False)
            self.mini_player_shortcut.setEnabled(False)

        self.update_mini_player_track_controls()
        self.update_win_thumbnail_buttons_track_controls()
        self.update_tray_icon_track_controls()

    def update_tray_icon_track_controls(self):
        if self.tray_icon_setting == 1 and self.tray_icon:
            if self.video_state == "VideoPlaying":
                self.tray_icon.previous_action.setEnabled(True)
                self.tray_icon.play_pause_action.setIcon(QIcon(f"{self.icon_folder}/pause.png"))
                self.tray_icon.play_pause_action.setEnabled(True)
                self.tray_icon.next_action.setEnabled(True)
            elif self.video_state == "VideoPaused":
                self.tray_icon.previous_action.setEnabled(True)
                self.tray_icon.play_pause_action.setIcon(QIcon(f"{self.icon_folder}/play.png"))
                self.tray_icon.play_pause_action.setEnabled(True)
                self.tray_icon.next_action.setEnabled(True)
            else:
                self.tray_icon.previous_action.setEnabled(False)
                self.tray_icon.play_pause_action.setIcon(QIcon(f"{self.icon_folder}/play.png"))
                self.tray_icon.play_pause_action.setEnabled(False)
                self.tray_icon.next_action.setEnabled(False)
    
    def update_win_thumbnail_buttons_track_controls(self):
        if self.win_thumbmail_buttons_setting == 1 and self.win_thumbnail_toolbar:
            if self.video_state == "VideoPlaying":
                self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-filled-border.png"))
                self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/pause-filled-border.png"))            
                self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-filled-border.png"))
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
            elif self.video_state == "VideoPaused":
                self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-filled-border.png"))
                self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/play-filled-border.png"))
                self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-filled-border.png"))
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
            else:
                self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-filled-border-disabled.png"))
                self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/play-filled-border-disabled.png"))
                self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-filled-border-disabled.png"))
                self.tool_btn_previous.setEnabled(False)
                self.tool_btn_play_pause.setEnabled(False)
                self.tool_btn_next.setEnabled(False)

    def update_mini_player_track_controls(self):
        if self.mini_player_dialog:
            if self.video_state == "VideoPlaying":
                self.mini_player_dialog.previous_button.setEnabled(True)
                self.mini_player_dialog.play_pause_button.setIcon(QIcon(f"{self.icon_folder}/pause-filled.png"))
                self.mini_player_dialog.play_pause_button.setEnabled(True)
                self.mini_player_dialog.next_button.setEnabled(True)
                self.mini_player_dialog.like_button.setEnabled(True)
                self.mini_player_dialog.dislike_button.setEnabled(True)
            elif self.video_state == "VideoPaused":
                self.mini_player_dialog.previous_button.setEnabled(True)
                self.mini_player_dialog.play_pause_button.setIcon(QIcon(f"{self.icon_folder}/play-filled.png"))
                self.mini_player_dialog.play_pause_button.setEnabled(True)
                self.mini_player_dialog.next_button.setEnabled(True)
                self.mini_player_dialog.like_button.setEnabled(True)
                self.mini_player_dialog.dislike_button.setEnabled(True)
            else:
                self.mini_player_dialog.previous_button.setEnabled(False)
                self.mini_player_dialog.play_pause_button.setIcon(QIcon(f"{self.icon_folder}/play-filled.png"))
                self.mini_player_dialog.play_pause_button.setEnabled(False)
                self.mini_player_dialog.next_button.setEnabled(False)
                self.mini_player_dialog.like_button.setEnabled(False)
                self.mini_player_dialog.dislike_button.setEnabled(False)

    def create_menu(self):
        self.back_action = Action("Back", shortcut="Alt+Left")
        self.back_action.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_action.setEnabled(False)
        self.back_action.triggered.connect(self.webview.back)

        self.forward_action = Action("Forward", shortcut="Alt+Right")
        self.forward_action.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_action.setEnabled(False)
        self.forward_action.triggered.connect(self.webview.forward)

        self.home_action = Action("Home", shortcut="Ctrl+H")
        self.home_action.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_action.triggered.connect(self.home)

        self.reload_action = Action("Reload", shortcut="Ctrl+R")
        self.reload_action.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_action.triggered.connect(self.webview.reload)

        self.download_with_oauth_action = Action("with OAuth 2.0", shortcut="Ctrl+Shift+D")
        self.download_with_oauth_action.setIcon(QIcon(f"{self.icon_folder}/oauth.png"))
        self.download_with_oauth_action.setEnabled(True)
        self.download_with_oauth_action.triggered.connect(lambda: self.download(use_oauth=True))

        self.download_as_unauthorized_action = Action("as Unauthorized", shortcut="Ctrl+D")
        self.download_as_unauthorized_action.setIcon(QIcon(f"{self.icon_folder}/unauthorized.png"))
        self.download_as_unauthorized_action.setEnabled(False)
        self.download_as_unauthorized_action.triggered.connect(lambda: self.download(use_oauth=False))

        self.mini_player_action = Action("Mini-Player", shortcut="Ctrl+M")
        self.mini_player_action.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_action.setEnabled(False)
        self.mini_player_action.triggered.connect(self.mini_player)

        self.settings_action = Action("Settings", shortcut="Ctrl+S")
        self.settings_action.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_action.triggered.connect(self.settings)

        self.bug_report_action = Action("Bug Report")
        self.bug_report_action.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_action.triggered.connect(self.bug_report)

        self.about_action = Action("About")
        self.about_action.setIcon(QIcon(f"{self.icon_folder}/about.png"))
        self.about_action.triggered.connect(self.about)

        self.cut_action = Action("Cut", shortcut="Ctrl+X")
        self.cut_action.setIcon(QIcon(f"{self.icon_folder}/cut.png"))
        self.cut_action.triggered.connect(self.cut)

        self.copy_action = Action("Copy", shortcut="Ctrl+C")
        self.copy_action.setIcon(QIcon(f"{self.icon_folder}/copy.png"))
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = Action("Paste", shortcut="Ctrl+V")
        self.paste_action.setIcon(QIcon(f"{self.icon_folder}/paste.png"))
        self.paste_action.triggered.connect(self.paste)

        self.main_menu = RoundMenu(self)

        self.download_menu = RoundMenu("Download...", self)
        self.download_menu.setIcon(QIcon(f"{self.icon_folder}/download.png"))
        
        self.edit_menu = RoundMenu(self)

        self.copy_menu = RoundMenu(self)

        self.paste_menu = RoundMenu(self)

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
        self.main_menu.addAction(self.about_action)

        self.download_menu.addAction(self.download_with_oauth_action)
        self.download_menu.addAction(self.download_as_unauthorized_action)

        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)

        self.copy_menu.addAction(self.copy_action)

        self.paste_menu.addAction(self.paste_action)

    def create_toolbar(self):
        self.back_tbutton.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_tbutton.setEnabled(False)
        self.back_tbutton.installEventFilter(ToolTipFilter(self.back_tbutton, 300, ToolTipPosition.TOP))
        self.back_tbutton.clicked.connect(self.webview.back)

        self.forward_tbutton.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_tbutton.setEnabled(False)
        self.forward_tbutton.installEventFilter(ToolTipFilter(self.forward_tbutton, 300, ToolTipPosition.TOP))
        self.forward_tbutton.clicked.connect(self.webview.forward)

        self.home_tbutton.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_tbutton.installEventFilter(ToolTipFilter(self.home_tbutton, 300, ToolTipPosition.TOP))
        self.home_tbutton.clicked.connect(self.home)

        self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_tbutton.installEventFilter(ToolTipFilter(self.reload_tbutton, 300, ToolTipPosition.TOP))
        self.reload_tbutton.clicked.connect(self.webview.reload)

        self.LineEdit.returnPressed.connect(self.on_line_edit_return_pressed)

        self.download_ddtbutton.setIcon(QIcon(f"{self.icon_folder}/download.png"))
        self.download_ddtbutton.setMenu(self.download_menu)
        self.download_ddtbutton.installEventFilter(ToolTipFilter(self.download_ddtbutton, 300, ToolTipPosition.TOP))

        self.mini_player_tbutton.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_tbutton.setEnabled(False)
        self.mini_player_tbutton.installEventFilter(ToolTipFilter(self.mini_player_tbutton, 300, ToolTipPosition.TOP))
        self.mini_player_tbutton.clicked.connect(self.mini_player)

        self.settings_tbutton.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_tbutton.installEventFilter(ToolTipFilter(self.settings_tbutton, 300, ToolTipPosition.TOP))
        self.settings_tbutton.clicked.connect(self.settings)

        self.bug_report_tbutton.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_tbutton.installEventFilter(ToolTipFilter(self.bug_report_tbutton, 300, ToolTipPosition.TOP))
        self.bug_report_tbutton.clicked.connect(self.bug_report)

        self.about_tbutton.setIcon(QIcon(f"{self.icon_folder}/about.png"))
        self.about_tbutton.installEventFilter(ToolTipFilter(self.about_tbutton, 300, ToolTipPosition.TOP))
        self.about_tbutton.clicked.connect(self.about)

    def activate_plugins(self):
        self.activate_ad_blocker()
        self.activate_scrollbar_styles()
        self.activate_discord_rpc()
        self.activate_ytmusic_observer()
        self.activate_win_thumbnail_toolbar()
        self.activate_tray_icon()
        self.activate_track_notifier()
        self.activate_yt_hotkeys()
        self.activate_only_audio()

    def activate_ad_blocker(self):
        if self.ad_blocker_setting == 1:
            ad_blocker_plugin = QWebEngineScript()
            ad_blocker_plugin.setName("AdBlocker")
            ad_blocker_plugin.setSourceCode(self.read_script("ad_blocker.js"))
            ad_blocker_plugin.setInjectionPoint(QWebEngineScript.DocumentReady)
            ad_blocker_plugin.setWorldId(QWebEngineScript.ApplicationWorld)
            ad_blocker_plugin.setRunsOnSubFrames(True)
            self.webpage.profile().scripts().insert(ad_blocker_plugin)

    def activate_scrollbar_styles(self):
        scrollbar_styles_plugin = QWebEngineScript()
        scrollbar_styles_plugin.setName("ScrollbarStyles")
        scrollbar_styles_plugin.setSourceCode(self.read_script("scrollbar_styles.js"))
        scrollbar_styles_plugin.setInjectionPoint(QWebEngineScript.DocumentReady)
        scrollbar_styles_plugin.setWorldId(QWebEngineScript.ApplicationWorld)
        scrollbar_styles_plugin.setRunsOnSubFrames(True)
        self.webpage.profile().scripts().insert(scrollbar_styles_plugin)

    def activate_discord_rpc(self):
        if self.discord_rpc_setting == 1:
            app_id = "1254202610781655050"
            self.discord_rpc = pypresence.Presence(app_id)
            try:
                self.discord_rpc.connect()
            except Exception as e:
                logging.error(f"Discord RPC connection failed: {str(e)}")
        else:
            self.discord_rpc = None

    def activate_ytmusic_observer(self):
        ytmusic_observer_plugin = QWebEngineScript()
        ytmusic_observer_plugin.setName("YtMusicObserver")
        ytmusic_observer_plugin.setSourceCode(self.read_script("ytmusic_observer.js"))
        ytmusic_observer_plugin.setInjectionPoint(QWebEngineScript.Deferred)
        ytmusic_observer_plugin.setWorldId(QWebEngineScript.MainWorld)
        ytmusic_observer_plugin.setRunsOnSubFrames(True)
        self.webpage.profile().scripts().insert(ytmusic_observer_plugin)

    def activate_win_thumbnail_toolbar(self):
        if self.win_thumbmail_buttons_setting == 1:
            self.win_thumbnail_toolbar = QWinThumbnailToolBar(self)
            self.create_previous_button()
            self.create_play_pause_button()
            self.create_next_button()
            self.win_thumbnail_toolbar.setWindow(self.windowHandle())
        else:
            self.win_thumbnail_toolbar = None

    def create_previous_button(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_previous.setToolTip('Previous')
        self.tool_btn_previous.setEnabled(False)
        self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-filled-border-disabled.png"))
        self.tool_btn_previous.clicked.connect(self.skip_previous)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_previous)

    def create_play_pause_button(self):
        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_play_pause.setToolTip('Play/Pause')
        self.tool_btn_play_pause.setEnabled(False)
        self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/play-filled-border-disabled.png"))  
        self.tool_btn_play_pause.clicked.connect(self.play_pause)                   
        self.win_thumbnail_toolbar.addButton(self.tool_btn_play_pause)

    def create_next_button(self):
        self.tool_btn_next = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_next.setToolTip('Next')
        self.tool_btn_next.setEnabled(False)
        self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-filled-border-disabled.png"))
        self.tool_btn_next.clicked.connect(self.skip_next)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_next)

    def activate_tray_icon(self):
        if self.tray_icon_setting == 1:
            self.tray_icon = SystemTrayIcon(self.windowIcon(), self)
            self.tray_icon.show()
        else:
            self.tray_icon = None

    def activate_track_notifier(self):
        if self.track_change_notificator_setting == 1:
            self.track_notifier = ToastNotifier()
        else:
            self.track_notifier = None

    def activate_yt_hotkeys(self):
        if self.hotkey_playback_control_setting == 1:
            yt_hotkeys_script = QWebEngineScript()
            yt_hotkeys_script.setName("YtHotkeys")
            yt_hotkeys_script.setSourceCode(self.read_script("yt_hotkeys.js"))
            yt_hotkeys_script.setInjectionPoint(QWebEngineScript.Deferred)
            yt_hotkeys_script.setWorldId(QWebEngineScript.MainWorld)
            yt_hotkeys_script.setRunsOnSubFrames(True)
            self.webpage.profile().scripts().insert(yt_hotkeys_script)

    def activate_only_audio(self):
        if self.only_audio_mode_setting == 1:
            only_audio_script = QWebEngineScript()
            only_audio_script.setName("OnlyAudio")
            only_audio_script.setSourceCode(self.read_script("only_audio.js"))
            only_audio_script.setInjectionPoint(QWebEngineScript.Deferred)
            only_audio_script.setWorldId(QWebEngineScript.MainWorld)
            only_audio_script.setRunsOnSubFrames(True)
            self.webpage.profile().scripts().insert(only_audio_script)

    def skip_previous(self):
        self.run_js_script("skip_previous.js")

    def play_pause(self):
        self.run_js_script("play_pause.js")

    def skip_next(self):
        self.run_js_script("skip_next.js")

    def like(self):
        self.run_js_script("like.js")
    
    def dislike(self):
        self.run_js_script("dislike.js")
        
    def run_js_script(self, script_name):
        self.webpage.runJavaScript(self.read_script(script_name))    
        
    def read_script(self, filename):
        with open(f"{self.current_dir}/core/js/{filename}", "r", encoding='utf-8') as f:
            return f.read()

    def back(self):
        self.webview.back()

    def forward(self):
        self.webview.forward()

    def home(self):
        self.webview.load(QUrl("https://music.youtube.com/"))

    def reload(self):
        self.webview.reload()

    def select_download_folder(self, title_suffix=""):
        title = f"Select Download Folder {title_suffix}"
        folder = QFileDialog.getExistingDirectory(self, title, self.last_download_folder_setting)
        return folder if folder else None

    def download(self, custom_url=None, download_folder=None, info_bar=None, use_oauth=False):
        if self.is_downloading:
            return

        if info_bar:
            info_bar.close()

        url = custom_url or self.current_url

        title_suffix = "[OAuth 2.0]" if use_oauth else "[Unauthorized]"
        download_folder = download_folder or self.select_download_folder(title_suffix)
        if not download_folder:
            return

        self.last_download_folder_setting = download_folder
        self.settings_.setValue("last_download_folder", download_folder)

        self.is_downloading = True
        self.update_download_buttons_state(self.is_downloading)

        self.download_thread = DownloadThread(url, download_folder, self, use_oauth=use_oauth)
        self.download_thread.download_finished.connect(self.on_download_finished)
        self.download_thread.download_failed.connect(self.on_download_failed)
        self.download_thread.oauth_required.connect(self.oauth_verifier)
        self.download_thread.start()

    def on_download_finished(self, download_folder, title):
        self.is_downloading = False
        self.update_download_buttons_state(self.is_downloading)

        info_bar = InfoBar.success(
            title=title,
            content="successfully downloaded!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self
        )
        open_download_folder_btn = PushButton("Open Folder", icon=f"{self.icon_folder}/open_folder.png")
        open_download_folder_btn.clicked.connect(lambda: self.open_download_folder(download_folder, info_bar))
        info_bar.addWidget(open_download_folder_btn)
        info_bar.show()

    def on_download_failed(self, url, download_folder, title, use_oauth=False):
        self.is_downloading = False
        self.update_download_buttons_state(self.is_downloading)

        info_bar = InfoBar.error(
            title=title,
            content="download failed!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self
        )
        retry_download_btn = PushButton("Re-download", icon=f"{self.icon_folder}/restart.png")
        retry_download_btn.clicked.connect(lambda: self.download(url, download_folder, info_bar, use_oauth))
        info_bar.addWidget(retry_download_btn)
        info_bar.show()

    def update_download_buttons_state(self, is_downloading):
        self.download_with_oauth_action.setEnabled(not is_downloading)
        self.download_as_unauthorized_action.setEnabled(not is_downloading)
        self.download_with_oauth_shortcut.setEnabled(not is_downloading)
        self.download_as_unauthorized_shortcut.setEnabled(not is_downloading)

    def open_download_folder(self, download_folder, info_bar):
        info_bar.close()
        os.startfile(download_folder)

    def oauth_verifier(self, verification_url, user_code):
        previous_url = self.current_url
        self.webview.load(QUrl(verification_url))

        info_bar = InfoBar.info(
            title=f'{user_code}',
            content='Copy the code and paste it into the input field',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self
        )
        info_bar.closeButton.setIcon(QIcon(f"{self.icon_folder}/next_step.png"))
        info_bar.closeButton.setToolTip("Click after all authentication steps have been completed.")
        info_bar.closeButton.installEventFilter(ToolTipFilter(info_bar.closeButton, 300, ToolTipPosition.TOP))
        info_bar.closeButton.clicked.connect(lambda: self.next_oauth_step(previous_url, info_bar))

        copy_btn = PushButton("Copy Code", icon=f"{self.icon_folder}/copy.png")
        copy_btn.clicked.connect(lambda: self.copy_oauth_code(user_code))  
        info_bar.addWidget(copy_btn)

        info_bar.addWidget(copy_btn)
        info_bar.show()

    def copy_oauth_code(self, code):
        clipboard = QApplication.clipboard()
        clipboard.setText(code)

    def next_oauth_step(self, previous_url, info_bar):
        info_bar.close()
        self.oauth_completed.emit()
        if self.current_url != previous_url:
            self.webview.load(QUrl(previous_url))

    def mini_player(self):
        if self.video_state == "VideoPlaying" or "VideoPaused":
            self.show_mini_player()
            self.hide()
            self.hide_tray_icon()

    def show_mini_player(self):
        self.mini_player_dialog = MiniPlayerDialog(self)
        self.update_mini_player_track_controls()
        self.update_mini_player_like_dislike_controls()
        self.update_mini_player_track_info()
        self.update_mini_player_track_progress()
        self.mini_player_dialog.show()

    def show_tray_icon(self):
        if self.tray_icon:
            self.tray_icon.show()

    def hide_tray_icon(self):
        if self.tray_icon:
            self.tray_icon.hide()
    
    def on_line_edit_return_pressed(self):
        url = self.LineEdit.text()
        self.webview.load(QUrl(url))

    def settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def bug_report(self):
        webbrowser.open_new_tab("https://github.com/deeffest/Youtube-Music-Desktop-Player/issues/new/choose")

    def cut(self):  
        self.webpage.triggerAction(QWebEnginePage.Cut)

    def copy(self):
        self.webpage.triggerAction(QWebEnginePage.Copy)

    def paste(self):
        self.webpage.triggerAction(QWebEnginePage.Paste)

    def save_settings(self):
        if self.save_last_zoom_factor_setting == 1:
            self.last_zoom_factor_setting = self.webview.zoomFactor()
            self.settings_.setValue("last_zoom_factor", self.last_zoom_factor_setting)
        if self.save_last_win_geometry_setting == 1:
            if not self.isMaximized() and not self.isFullScreen():
                self.last_win_geometry_setting = self.geometry()
                self.settings_.setValue("last_win_geometry", self.last_win_geometry_setting)
        if self.current_url is not None:
            self.last_url_setting = self.current_url
            self.settings_.setValue("last_url", self.last_url_setting)

    def show_window(self):
        if self.isMinimized() or self.isHidden():
            if self.isMinimized():
                self.showNormal()
            else:
                self.show()
        self.activateWindow()
        
    def closeEvent(self, event):
        if self.tray_icon_setting == 1 and self.tray_icon is not None:
            if not self.force_exit:
                self.hide()
                event.ignore()
                return

        if self.video_state == "VideoPlaying":
            self.show_window()
            
            msg_box = MessageBox(
                "Exit Confirmation",
                "Exiting now will stop the current playback and close the application.\nDo you want to exit now?",
                self
            )
            msg_box.yesButton.setText("Exit")
            msg_box.cancelButton.setText("Cancel")
            
            if not msg_box.exec_():
                self.force_exit = False
                event.ignore()
                return

        self.save_settings()
        event.accept()