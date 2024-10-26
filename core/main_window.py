import pywinstyles
import webbrowser
import pypresence
import os
import logging

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QShortcut, \
    QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineSettings, \
    QWebEngineScript
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QSettings, QUrl, Qt, QSize, pyqtSlot, QRect
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.uic import loadUi
from qfluentwidgets import setTheme, setThemeColor, Theme, \
    RoundMenu, Action, SplashScreen, MessageBox, InfoBar, InfoBarPosition, \
    PushButton
from core.web_engine_view import WebEngineView
from core.web_engine_page import WebEnginePage
from core.settings_dialog import SettingsDialog
from core.about_dialog import AboutDialog
from core.mini_player_dialog import MiniPlayerDialog
from core.system_tray_icon import SystemTrayIcon
from core.update_checker import UpdateChecker
from packaging import version as pkg_version
from core.ytmusic_downloader import DownloadThread

class MainWindow(QMainWindow):
    def __init__(self, custom_url, app_info, parent=None):
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
        self.custom_url = custom_url
        self.current_time = "NaN"
        self.total_time = "NaN"
    
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
        self.settings_ = QSettings()

        if self.settings_.value("ad_blocker") is None:
            self.settings_.setValue("ad_blocker", 1)
        if self.settings_.value("save_last_win_size") is None:
            self.settings_.setValue("save_last_win_size", 1)
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
        if self.settings_.value("last_win_size") is None:
            self.settings_.setValue("last_win_size", QSize(1080, 600))
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
            self.settings_.setValue("geometry_of_mp", QRect(30, 60, 360, 150))
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

        self.ad_blocker_setting = int(self.settings_.value("ad_blocker"))
        self.save_last_win_size_setting = int(self.settings_.value("save_last_win_size"))
        self.open_last_url_at_startup_setting = int(self.settings_.value("open_last_url_at_startup"))
        self.last_url_setting = self.settings_.value("last_url")
        self.fullscreen_mode_support_setting = int(self.settings_.value("fullscreen_mode_support"))
        self.support_animated_scrolling_setting = int(self.settings_.value("support_animated_scrolling"))
        self.save_last_pos_of_mp_setting = int(self.settings_.value("save_last_pos_of_mp"))
        self.last_win_size_setting = self.settings_.value("last_win_size")
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
        
        if self.custom_url is not None:
            self.webview.load(QUrl(self.custom_url))
        elif self.open_last_url_at_startup_setting == 1:
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
            logging.error(f"QNetworkProxy An error occurred: {e}")

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
        
    def handle_update_checked(self, version, download):
        if pkg_version.parse(self.version) < pkg_version.parse(version):
            msg_box = MessageBox(
                f"A new update {version} is available",
                (
                    "New features, bug fixes and application optimization are waiting for you!\n"
                    "Do you want to update now?"
                ),
                self
            )
            msg_box.yesButton.setText("Update now!")
            msg_box.cancelButton.setText("Later")
            if msg_box.exec_():
                webbrowser.open_new_tab(download)
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

        self.download_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), self)
        self.download_shortcut.activated.connect(self.download)

        self.mini_player_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), self)
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
            self.download_action.setEnabled(self.is_video_or_playlist)
            self.download_tbutton.setEnabled(self.is_video_or_playlist)
            self.download_shortcut.setEnabled(self.is_video_or_playlist)

        if self.current_url is not None:
            self.last_url_setting = self.current_url
            self.settings_.setValue("last_url", self.last_url_setting)

    def setup_webchannel(self):
        self.webchannel = QWebChannel()
        self.webview.page().setWebChannel(self.webchannel)
        self.webchannel.registerObject("backend", self)

    @pyqtSlot(str)
    def like_status_changed(self, status):
        if status != "":
            self.like_status = status
        else:
            self.like_status = None

        self.update_mini_player_like_dislike_controls()
        self.update_win_thumbnail_buttons_like_dislike_controls()
        self.update_tray_icon_like_dislike_controls()

    def update_tray_icon_like_dislike_controls(self):
        if self.tray_icon_setting == 1 and self.tray_icon:
            if self.like_status == "Like":
                self.tray_icon.like_action.setIcon(QIcon(f"{self.icon_folder}/like-checked.png"))
                self.tray_icon.dislike_action.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))
                self.tray_icon.like_action.setEnabled(True)
                self.tray_icon.dislike_action.setEnabled(True)
            elif self.like_status == "Dislike":
                self.tray_icon.like_action.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.tray_icon.dislike_action.setIcon(QIcon(f"{self.icon_folder}/dislike-checked.png"))
                self.tray_icon.like_action.setEnabled(True)
                self.tray_icon.dislike_action.setEnabled(True)
            elif self.like_status == "Indifferent":
                self.tray_icon.like_action.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.tray_icon.dislike_action.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))
                self.tray_icon.like_action.setEnabled(True)
                self.tray_icon.dislike_action.setEnabled(True)
            else:
                self.tray_icon.like_action.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.tray_icon.dislike_action.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))
                self.tray_icon.like_action.setEnabled(False)
                self.tray_icon.dislike_action.setEnabled(False)

    def update_win_thumbnail_buttons_like_dislike_controls(self):
        if self.win_thumbmail_buttons_setting == 1 and self.win_thumbnail_toolbar:
            if self.like_status == "Like":
                self.tool_btn_like.setIcon(QIcon(f"{self.icon_folder}/like-border-checked.png"))
                self.tool_btn_dislike.setIcon(QIcon(f"{self.icon_folder}/dislike-border.png"))
                self.tool_btn_like.setEnabled(True)
                self.tool_btn_dislike.setEnabled(True)
            elif self.like_status == "Dislike":
                self.tool_btn_like.setIcon(QIcon(f"{self.icon_folder}/like-border.png"))
                self.tool_btn_dislike.setIcon(QIcon(f"{self.icon_folder}/dislike-border-checked.png"))
                self.tool_btn_like.setEnabled(True)
                self.tool_btn_dislike.setEnabled(True)
            elif self.like_status == "Indifferent":
                self.tool_btn_like.setIcon(QIcon(f"{self.icon_folder}/like-border.png"))
                self.tool_btn_dislike.setIcon(QIcon(f"{self.icon_folder}/dislike-border.png"))
                self.tool_btn_like.setEnabled(True)
                self.tool_btn_dislike.setEnabled(True)
            else:
                self.tool_btn_like.setIcon(QIcon(f"{self.icon_folder}/like-border-disabled.png"))
                self.tool_btn_dislike.setIcon(QIcon(f"{self.icon_folder}/dislike-border-disabled.png"))
                self.tool_btn_like.setEnabled(False)
                self.tool_btn_dislike.setEnabled(False)
    
    def update_mini_player_like_dislike_controls(self):
        if self.mini_player_dialog:
            if self.like_status == "Like":
                self.mini_player_dialog.like_button.setIcon(QIcon(f"{self.icon_folder}/like-filled-checked.png"))
                self.mini_player_dialog.dislike_button.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))
                self.mini_player_dialog.like_button.setEnabled(True)
                self.mini_player_dialog.dislike_button.setEnabled(True)
            elif self.like_status == "Dislike":
                self.mini_player_dialog.like_button.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.mini_player_dialog.dislike_button.setIcon(QIcon(f"{self.icon_folder}/dislike-filled-checked.png"))
                self.mini_player_dialog.like_button.setEnabled(True)
                self.mini_player_dialog.dislike_button.setEnabled(True)
            elif self.like_status == "Indifferent":
                self.mini_player_dialog.like_button.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.mini_player_dialog.dislike_button.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))
                self.mini_player_dialog.like_button.setEnabled(True)
                self.mini_player_dialog.dislike_button.setEnabled(True)
            else:
                self.mini_player_dialog.like_button.setIcon(QIcon(f"{self.icon_folder}/like.png"))
                self.mini_player_dialog.dislike_button.setIcon(QIcon(f"{self.icon_folder}/dislike.png"))
                self.mini_player_dialog.like_button.setEnabled(False)
                self.mini_player_dialog.dislike_button.setEnabled(False)

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
                logging.error("An error occurred while updating Discord RPC: " + str(e))
                self.reconnect_discord_rpc(retry_update=True)

    def reconnect_discord_rpc(self, retry_update=False):
        if self.discord_rpc:
            try:
                self.discord_rpc.connect()
                if retry_update:
                    self.update_discord_rpc()
            except Exception as e:
                logging.error("An error occurred while reconnecting Discord RPC: " + str(e))

    def clear_discord_rpc(self):
        if self.discord_rpc:
            try:
                self.discord_rpc.clear()
            except Exception as e:
                logging.error("An error occurred while clearing Discord RPC: " + str(e))

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
                self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-border.png"))
                self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/pause-border.png"))            
                self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-border.png"))
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
            elif self.video_state == "VideoPaused":
                self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-border.png"))
                self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/play-border.png"))
                self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-border.png"))
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
            else:
                self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-border-disabled.png"))
                self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/play-border-disabled.png"))
                self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-border-disabled.png"))
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
            elif self.video_state == "VideoPaused":
                self.mini_player_dialog.previous_button.setEnabled(True)
                self.mini_player_dialog.play_pause_button.setIcon(QIcon(f"{self.icon_folder}/play-filled.png"))
                self.mini_player_dialog.play_pause_button.setEnabled(True)
                self.mini_player_dialog.next_button.setEnabled(True)
            else:
                self.mini_player_dialog.previous_button.setEnabled(False)
                self.mini_player_dialog.play_pause_button.setIcon(QIcon(f"{self.icon_folder}/play-filled.png"))
                self.mini_player_dialog.play_pause_button.setEnabled(False)
                self.mini_player_dialog.next_button.setEnabled(False)

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

        self.download_action = Action("Download", shortcut="Ctrl+D")
        self.download_action.setIcon(QIcon(f"{self.icon_folder}/download.png"))
        self.download_action.triggered.connect(self.download)

        self.mini_player_action = Action("Mini-Player", shortcut="Ctrl+M")
        self.mini_player_action.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_action.triggered.connect(self.mini_player)

        self.settings_action = Action("Settings", shortcut="Ctrl+S")
        self.settings_action.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_action.triggered.connect(self.settings)

        self.bug_report_action = Action("Bug Report")
        self.bug_report_action.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_action.triggered.connect(self.bug_report)

        self.about_action = Action("About...")
        self.about_action.setIcon(QIcon(f"{self.icon_folder}/about.png"))
        self.about_action.triggered.connect(self.about)

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
        self.main_menu.addAction(self.download_action)

        self.main_menu.addAction(self.mini_player_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.settings_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.bug_report_action)
        self.main_menu.addAction(self.about_action)

        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)

    def create_toolbar(self):
        self.back_tbutton.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_tbutton.clicked.connect(self.webview.back)

        self.forward_tbutton.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_tbutton.clicked.connect(self.webview.forward)

        self.home_tbutton.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_tbutton.clicked.connect(self.home)

        self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_tbutton.clicked.connect(self.webview.reload)

        self.LineEdit.textChanged.connect(self.on_line_edit_text_changed)

        self.download_tbutton.setIcon(QIcon(f"{self.icon_folder}/download.png"))
        self.download_tbutton.clicked.connect(self.download)

        self.mini_player_tbutton.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_tbutton.clicked.connect(self.mini_player)

        self.settings_tbutton.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_tbutton.clicked.connect(self.settings)

    def activate_plugins(self):
        self.activate_ad_blocker()
        self.activate_scrollbar_styles()
        self.activate_discord_rpc()
        self.activate_ytmusic_observer()
        self.activate_win_thumbnail_toolbar()
        self.activate_tray_icon()

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
                logging.error("An error occurred while connecting to Discord RPC: " + str(e))
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
            self.create_dislike_button()
            self.create_previous_button()
            self.create_play_pause_button()
            self.create_next_button()
            self.create_like_button()
            self.win_thumbnail_toolbar.setWindow(self.windowHandle())
        else:
            self.win_thumbnail_toolbar = None

    def create_dislike_button(self):
        self.tool_btn_dislike = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_dislike.setToolTip('Dislike')
        self.tool_btn_dislike.setEnabled(False)
        self.tool_btn_dislike.setIcon(QIcon(f"{self.icon_folder}/dislike-border-disabled.png"))
        self.tool_btn_dislike.clicked.connect(self.dislike)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_dislike)

    def create_previous_button(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_previous.setToolTip('Previous')
        self.tool_btn_previous.setEnabled(False)
        self.tool_btn_previous.setIcon(QIcon(f"{self.icon_folder}/previous-border-disabled.png"))
        self.tool_btn_previous.clicked.connect(self.skip_previous)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_previous)

    def create_play_pause_button(self):
        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_play_pause.setToolTip('Play/Pause')
        self.tool_btn_play_pause.setEnabled(False)
        self.tool_btn_play_pause.setIcon(QIcon(f"{self.icon_folder}/play-border-disabled.png"))  
        self.tool_btn_play_pause.clicked.connect(self.play_pause)                   
        self.win_thumbnail_toolbar.addButton(self.tool_btn_play_pause)

    def create_next_button(self):
        self.tool_btn_next = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_next.setToolTip('Next')
        self.tool_btn_next.setEnabled(False)
        self.tool_btn_next.setIcon(QIcon(f"{self.icon_folder}/next-border-disabled.png"))
        self.tool_btn_next.clicked.connect(self.skip_next)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_next)

    def create_like_button(self):
        self.tool_btn_like = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_like.setToolTip('Like')
        self.tool_btn_like.setEnabled(False)
        self.tool_btn_like.setIcon(QIcon(f"{self.icon_folder}/like-border-disabled.png"))
        self.tool_btn_like.clicked.connect(self.like)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_like)

    def activate_tray_icon(self):
        if self.tray_icon_setting == 1:
            self.tray_icon = SystemTrayIcon(self.windowIcon(), self)
            self.tray_icon.show()
        else:
            self.tray_icon = None

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
        self.webview.page().runJavaScript(self.read_script(script_name))    
        
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

    def select_download_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", self.last_download_folder_setting)
        return folder if folder else None

    def download(self, custom_url=None, download_folder=None, info_bar=None):
        if self.is_downloading:
            return

        if info_bar:
            info_bar.close()

        download_folder = download_folder or self.select_download_folder()
        if not download_folder:
            return

        self.last_download_folder_setting = download_folder
        self.settings_.setValue("last_download_folder", download_folder)

        self.is_downloading = True
        self.update_download_buttons("Wait...")

        url = custom_url or self.current_url

        self.download_thread = DownloadThread(url, download_folder, self)
        self.download_thread.download_finished.connect(self.on_download_finished)
        self.download_thread.download_failed.connect(self.on_download_failed)
        self.download_thread.start()

    def on_download_finished(self, download_folder, title):
        self.is_downloading = False
        self.update_download_buttons("Download")

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

    def on_download_failed(self, url, download_folder, title):
        self.is_downloading = False
        self.update_download_buttons("Download")

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
        retry_download_btn.clicked.connect(lambda: self.download(url, download_folder, info_bar))
        info_bar.addWidget(retry_download_btn)
        info_bar.show()

    def update_download_buttons(self, text):
        self.download_action.setText(text)
        self.download_action.setEnabled(not self.is_downloading)
        self.download_tbutton.setToolTip(text)
        self.download_tbutton.setEnabled(not self.is_downloading)

    def open_download_folder(self, download_folder, info_bar):
        info_bar.close()
        os.startfile(download_folder)

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

    def on_line_edit_text_changed(self):
        self.LineEdit.setCursorPosition(0)

    def settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def bug_report(self):
        webbrowser.open_new_tab("https://github.com/deeffest/Youtube-Music-Desktop-Player/issues/new/choose")

    def copy(self):
        self.webpage.triggerAction(QWebEnginePage.Copy)

    def paste(self):
        self.webpage.triggerAction(QWebEnginePage.Paste)

    def save_settings(self):
        self.last_zoom_factor_setting = self.webview.zoomFactor()
        self.settings_.setValue("last_zoom_factor", self.last_zoom_factor_setting)

    def show_window(self):
        if self.isMinimized() or self.isHidden():
            if self.isMinimized():
                self.showNormal()
            else:
                self.show()
        self.activateWindow()

    def resizeEvent(self, event):
        self.last_win_size_setting = self.size()
        self.settings_.setValue("last_win_size", self.last_win_size_setting)
        event.accept()
        
    def closeEvent(self, event):
        accept_event = True

        if self.tray_icon_setting == 1 and self.tray_icon is not None:
            if not self.force_exit:
                event.ignore()
                self.hide()
                return

        if self.video_state == "VideoPlaying":
            self.show_window()
            
            msg_box = MessageBox(
                "Exit Confirmation",
                (
                    "Exiting now will stop the current playback and close the application.\n"
                    "Do you want to exit now?"
                ),
                self
            )
            msg_box.yesButton.setText("Exit")
            msg_box.cancelButton.setText("Cancel")
            
            if msg_box.exec_():
                accept_event = True
            else:
                self.force_exit = False
                accept_event = False

        if accept_event:
            self.save_settings()
            event.accept()
        else:
            event.ignore()