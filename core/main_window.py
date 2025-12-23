import os
import logging
import platform
import traceback

from PyQt5.QtCore import (
    QUrl,
    Qt,
    QSize,
    QRect,
    QFile,
    QTextStream,
    QPoint,
    QTimer,
    QEvent,
)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import (
    QWebEnginePage,
    QWebEngineSettings,
    QWebEngineScript,
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QShortcut,
    QLineEdit,
    QAction,
    QSystemTrayIcon,
)
from qfluentwidgets import (
    Action,
    MessageBox,
    RoundMenu,
    CheckableMenu,
    SplashScreen,
    ToolTipFilter,
    ToolTipPosition,
    Theme,
    InfoBar,
    InfoBarPosition,
    StateToolTip,
    PushButton,
    setTheme,
    setThemeColor,
)
from packaging import version as pkg_version
from discordrpc import RPC, Button, Activity, ProgressBar

from core.about_dialog import AboutDialog
from core.picture_in_picture_dialog import PictureInPictureDialog
from core.settings_dialog import SettingsDialog
from core.system_tray_icon import SystemTrayIcon
from core.update_checker import UpdateChecker
from core.web_channel_backend import WebChannelBackend
from core.web_engine_page import WebEnginePage
from core.web_engine_view import WebEngineView
from core.ytmusic_downloader import DownloadThread
from core.helpers import (
    get_centered_geometry,
    is_valid_ytmusic_url,
    open_url,
)
from core.ui.ui_main_window import Ui_MainWindow
from core.hotkey_controller import HotkeyController
from core.text_view_dialog import TextViewDialog
from core.signal_bus import signal_bus

if platform.system() == "Windows":
    from PyQt5.QtWinExtras import (  # type: ignore
        QWinThumbnailToolBar,
        QWinThumbnailToolButton,
    )
    from pywinstyles import apply_style  # type: ignore


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app_settings, opengl_enviroment_setting, app_info):
        super().__init__()
        self.name = app_info[0]
        self.author = app_info[1]
        self.version = app_info[2]
        self.current_dir = app_info[3]
        self.icon_folder = f"{self.current_dir}/resources/icons"

        self.title = ""
        self.artist = ""
        self.artwork = ""
        self.video_id = ""
        self.duration = 0
        self.current_time = "0:00"
        self.total_time = "0:00"
        self.song_state = "NoSong"
        self.song_status = "Indifferent"

        self.force_exit = False
        self.is_downloading = False

        self.settings_ = app_settings
        self.opengl_enviroment_setting = opengl_enviroment_setting

        self.current_url = None
        self.picture_in_picture_dialog = None
        self.download_thread = None
        self.update_checker_thread = None
        self.hotkey_controller_thread = None
        self.downloading_state_tool_tip = None
        self.discord_rpc = None
        self.proxy_error_message = None

        self.load_settings()
        self.configure_window()
        self.connect_signals()
        self.set_application_proxy()
        self.connect_shortcuts()
        self.show_splash_screen()
        self.setup_web_engine()
        self.create_context_menu()
        self.configure_ui_elements()
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
            self.settings_.setValue("save_last_pos_of_mp", 0)
        if self.settings_.value("last_win_geometry") is None:
            self.settings_.setValue(
                "last_win_geometry", QRect(get_centered_geometry(1000, 799))
            )
        if self.settings_.value("save_last_zoom_factor") is None:
            self.settings_.setValue("save_last_zoom_factor", 1)
        if self.settings_.value("last_zoom_factor") is None:
            self.settings_.setValue("last_zoom_factor", 1.0)
        if self.settings_.value("last_download_folder") is None:
            self.settings_.setValue("last_download_folder", os.path.expanduser("~"))
        if self.settings_.value("discord_rpc") is None:
            self.settings_.setValue("discord_rpc", 0)
        if self.settings_.value("geometry_of_mp") is None:
            self.settings_.setValue(
                "geometry_of_mp", QRect(get_centered_geometry(360, 150))
            )
        if self.settings_.value("tray_icon") is None:
            self.settings_.setValue(
                "tray_icon", 1 if QSystemTrayIcon.isSystemTrayAvailable() else 0
            )
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
        if self.settings_.value("hotkey_playback_control") is None:
            self.settings_.setValue("hotkey_playback_control", 0)
        if self.settings_.value("only_audio_mode") is None:
            self.settings_.setValue("only_audio_mode", 0)
        if self.settings_.value("nonstop_music") is None:
            self.settings_.setValue("nonstop_music", 1)
        if self.settings_.value("hide_toolbar") is None:
            self.settings_.setValue("hide_toolbar", 0)
        if self.settings_.value("use_hd_thumbnails") is None:
            self.settings_.setValue("use_hd_thumbnails", 0)
        if self.settings_.value("hide_mini_player") is None:
            self.settings_.setValue("hide_mini_player", 0)
        if self.settings_.value("use_cookies") is None:
            self.settings_.setValue("use_cookies", "false")
        if self.settings_.value("convert_to_mp3") is None:
            self.settings_.setValue("convert_to_mp3", "false")
        if self.settings_.value("auto_update_ytdlp") is None:
            self.settings_.setValue("auto_update_ytdlp", "true")

        self.ad_blocker_setting = int(self.settings_.value("ad_blocker"))
        self.save_last_win_geometry_setting = int(
            self.settings_.value("save_last_win_geometry")
        )
        self.open_last_url_at_startup_setting = int(
            self.settings_.value("open_last_url_at_startup")
        )
        self.last_url_setting = self.settings_.value("last_url")
        self.fullscreen_mode_support_setting = int(
            self.settings_.value("fullscreen_mode_support")
        )
        self.support_animated_scrolling_setting = int(
            self.settings_.value("support_animated_scrolling")
        )
        self.save_last_pos_of_mp_setting = int(
            self.settings_.value("save_last_pos_of_mp")
        )
        self.last_win_geometry_setting = self.settings_.value("last_win_geometry")
        self.save_last_zoom_factor_setting = int(
            self.settings_.value("save_last_zoom_factor")
        )
        self.last_zoom_factor_setting = float(self.settings_.value("last_zoom_factor"))
        self.last_download_folder_setting = self.settings_.value("last_download_folder")
        self.discord_rpc_setting = int(self.settings_.value("discord_rpc"))
        self.geometry_of_mp_setting = self.settings_.value("geometry_of_mp")
        self.tray_icon_setting = (
            int(self.settings_.value("tray_icon"))
            if QSystemTrayIcon.isSystemTrayAvailable()
            else 0
        )
        self.proxy_type_setting = self.settings_.value("proxy_type")
        self.proxy_host_name_setting = self.settings_.value("proxy_host_name")
        self.proxy_port_setting = self.settings_.value("proxy_port")
        self.proxy_login_setting = self.settings_.value("proxy_login")
        self.proxy_password_setting = self.settings_.value("proxy_password")
        self.hotkey_playback_control_setting = int(
            self.settings_.value("hotkey_playback_control")
        )
        self.only_audio_mode_setting = int(self.settings_.value("only_audio_mode"))
        self.nonstop_music_setting = int(self.settings_.value("nonstop_music"))
        self.hide_toolbar_setting = int(self.settings_.value("hide_toolbar"))
        self.use_hd_thumbnails_setting = int(self.settings_.value("use_hd_thumbnails"))
        self.hide_mini_player_setting = int(self.settings_.value("hide_mini_player"))
        self.use_cookies_setting = str(self.settings_.value("use_cookies"))
        self.convert_to_mp3_setting = str(self.settings_.value("convert_to_mp3"))
        self.auto_update_ytdlp_setting = str(self.settings_.value("auto_update_ytdlp"))

    def configure_window(self):
        if platform.system() == "Windows":
            try:
                apply_style(self, "dark")
            except Exception as e:
                logging.error(f"Failed to apply dark style: + {str(e)}")
        setTheme(Theme.DARK)
        setThemeColor("red")

        self.setupUi(self)
        self.setWindowTitle("Youtube Music Desktop Player")
        self.setWindowIcon(QIcon(f"{self.icon_folder}/icon.ico"))
        if self.save_last_win_geometry_setting == 1:
            self.setGeometry(self.last_win_geometry_setting)
        else:
            self.setGeometry(get_centered_geometry(1000, 799))

    def connect_signals(self):
        signal_bus.show_window_sig.connect(self.show_window_or_picture_in_picture)
        signal_bus.app_error_sig.connect(self.show_error_message)

    def show_error_message(self, msg, title=None):
        text_view_dialog = TextViewDialog(
            f"{title}" if title else "Unexpected Error", msg, self
        )
        text_view_dialog.cancelButton.hide()
        text_view_dialog.exec_()

    def set_application_proxy(self):
        try:
            proxy = QNetworkProxy()

            if self.proxy_type_setting == "HttpProxy":
                proxy.setType(QNetworkProxy.HttpProxy)
            elif self.proxy_type_setting == "Socks5Proxy":
                proxy.setType(QNetworkProxy.Socks5Proxy)
            elif self.proxy_type_setting == "DefaultProxy":
                proxy.setType(QNetworkProxy.DefaultProxy)
                QNetworkProxy.setApplicationProxy(proxy)
                return
            elif self.proxy_type_setting == "NoProxy":
                proxy.setType(QNetworkProxy.NoProxy)
                QNetworkProxy.setApplicationProxy(proxy)
                return

            if self.proxy_host_name_setting:
                proxy.setHostName(self.proxy_host_name_setting)
            if self.proxy_port_setting:
                proxy.setPort(self.proxy_port_setting)

            if self.proxy_login_setting:
                proxy.setUser(self.proxy_login_setting)
            if self.proxy_password_setting:
                proxy.setPassword(self.proxy_password_setting)

            QNetworkProxy.setApplicationProxy(proxy)
        except Exception as e:
            logging.error(f"Failed to set application proxy: {e}")
            self.proxy_error_message = traceback.format_exc()

    def connect_shortcuts(self):
        self.back_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Left), self)
        self.back_shortcut.activated.connect(self.back)

        self.forward_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Right), self)
        self.forward_shortcut.activated.connect(self.forward)

        self.home_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_H), self)
        self.home_shortcut.activated.connect(self.home)

        self.reload_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self)
        self.reload_shortcut.activated.connect(self.reload)

        self.stop_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.stop_shortcut.setEnabled(False)
        self.stop_shortcut.activated.connect(self.stop)

        self.go_to_youtube_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Y), self)
        self.go_to_youtube_shortcut.setEnabled(False)
        self.go_to_youtube_shortcut.activated.connect(self.go_to_youtube)

        self.download_song_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_D), self)
        self.download_song_shortcut.setEnabled(False)
        self.download_song_shortcut.activated.connect(self.download_song)

        self.download_album_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), self)
        self.download_album_shortcut.setEnabled(False)
        self.download_album_shortcut.activated.connect(self.download_album)

        self.watch_in_pip_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), self)
        self.watch_in_pip_shortcut.setEnabled(False)
        self.watch_in_pip_shortcut.activated.connect(self.watch_in_pip)

        self.settings_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.settings_shortcut.activated.connect(self.settings)

        self.hide_toolbar_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), self)
        self.hide_toolbar_shortcut.activated.connect(self.hide_toolbar)

    def show_splash_screen(self):
        self.splash_screen = SplashScreen(self.windowIcon(), self, enableTitleBar=False)
        self.splash_screen.setIconSize(QSize(102, 102))

    def setup_web_engine(self):
        self.webview = WebEngineView(self)
        self.webpage = WebEnginePage(self)
        self.websettings = QWebEngineSettings.globalSettings()
        self.webview.setPage(self.webpage)

        if self.open_last_url_at_startup_setting == 1 and is_valid_ytmusic_url(
            self.last_url_setting
        ):
            self.webview.load(QUrl(self.last_url_setting))
        else:
            self.home()

        self.webview.urlChanged.connect(self.on_url_changed)
        self.webview.loadProgress.connect(self.on_load_progress)
        self.webview.loadStarted.connect(self.on_load_started)
        self.webpage.fullScreenRequested.connect(self.on_fullscreen_requested)

        self.websettings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled,
            self.fullscreen_mode_support_setting,
        )
        self.websettings.setAttribute(
            QWebEngineSettings.ScrollAnimatorEnabled,
            self.support_animated_scrolling_setting,
        )

        if self.save_last_zoom_factor_setting == 1:
            self.webview.setZoomFactor(self.last_zoom_factor_setting)

        self.webchannel_backend = WebChannelBackend(self)

        self.webchannel = QWebChannel()
        self.webpage.setWebChannel(self.webchannel)
        self.webchannel.registerObject("backend", self.webchannel_backend)

        self.MainLayout.addWidget(self.webview)
        self.webview.setFocus()

    def create_context_menu(self):
        self.exit_full_screen_action = Action("Exit full screen", shortcut="Esc")
        self.exit_full_screen_action.setIcon(
            QIcon(f"{self.icon_folder}/exit_full_screen.png")
        )
        self.exit_full_screen_action.triggered.connect(self.exit_full_screen)

        self.back_action = Action("Back", shortcut="Alt+Left")
        self.back_action.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_action.setEnabled(False)
        self.back_action.triggered.connect(self.back)

        self.forward_action = Action("Forward", shortcut="Alt+Right")
        self.forward_action.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_action.setEnabled(False)
        self.forward_action.triggered.connect(self.forward)

        self.home_action = Action("Home", shortcut="Ctrl+H")
        self.home_action.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_action.triggered.connect(self.home)

        self.reload_action = Action("Reload", shortcut="Ctrl+R")
        self.reload_action.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_action.triggered.connect(self.reload)

        self.go_to_youtube_action = Action("Go to YouTube", shortcut="Ctrl+Y")
        self.go_to_youtube_action.setIcon(QIcon(f"{self.icon_folder}/open.png"))
        self.go_to_youtube_action.setEnabled(False)
        self.go_to_youtube_action.triggered.connect(self.go_to_youtube)

        self.download_menu = RoundMenu("Download...", self)
        self.download_menu.setIcon(QIcon(f"{self.icon_folder}/download.png"))

        self.download_song_action = Action("Song", shortcut="Ctrl+D")
        self.download_song_action.setIcon(QIcon(f"{self.icon_folder}/song.png"))
        self.download_song_action.setEnabled(False)
        self.download_song_action.triggered.connect(self.download_song)

        self.download_album_action = Action("Album", shortcut="Ctrl+P")
        self.download_album_action.setIcon(QIcon(f"{self.icon_folder}/album.png"))
        self.download_album_action.setEnabled(False)
        self.download_album_action.triggered.connect(self.download_album)

        self.ytdlp_options_menu = CheckableMenu("yt-dlp Options...", self)
        self.ytdlp_options_menu.setIcon(QIcon(f"{self.icon_folder}/options.png"))

        self.use_cookies_action = Action("Use Cookies")
        self.use_cookies_action.setCheckable(True)
        if self.use_cookies_setting == "true":
            self.use_cookies_action.setChecked(True)
        else:
            self.use_cookies_action.setChecked(False)

        self.convert_to_mp3_action = Action("Convert to MP3")
        self.convert_to_mp3_action.setCheckable(True)
        if self.convert_to_mp3_setting == "true":
            self.convert_to_mp3_action.setChecked(True)
        else:
            self.convert_to_mp3_action.setChecked(False)

        self.auto_update_action = Action("Auto Update")
        self.auto_update_action.setCheckable(True)
        if self.auto_update_ytdlp_setting == "true":
            self.auto_update_action.setChecked(True)
        else:
            self.auto_update_action.setChecked(False)

        self.watch_in_pip_action = Action("Watch in PiP", shortcut="Ctrl+M")
        self.watch_in_pip_action.setIcon(
            QIcon(f"{self.icon_folder}/picture-in-picture.png")
        )
        self.watch_in_pip_action.setEnabled(False)
        self.watch_in_pip_action.triggered.connect(self.watch_in_pip)

        self.settings_action = Action("Settings...", shortcut="Ctrl+S")
        self.settings_action.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_action.triggered.connect(self.settings)

        self.bug_report_action = Action("Bug Report")
        self.bug_report_action.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_action.triggered.connect(self.bug_report)

        self.about_action = Action("About...")
        self.about_action.setIcon(QIcon(f"{self.icon_folder}/about.png"))
        self.about_action.triggered.connect(self.about)

        self.hide_toolbar_action = Action("Hide Toolbar", shortcut="Ctrl+T")
        self.hide_toolbar_action.setIcon(QIcon(f"{self.icon_folder}/hide_toolbar.png"))
        self.hide_toolbar_action.triggered.connect(self.hide_toolbar)

        self.cut_action = Action("Cut", shortcut="Ctrl+X")
        self.cut_action.setIcon(QIcon(f"{self.icon_folder}/cut.png"))
        self.cut_action.triggered.connect(self.cut)

        self.copy_action = Action("Copy", shortcut="Ctrl+C")
        self.copy_action.setIcon(QIcon(f"{self.icon_folder}/copy.png"))
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = Action("Paste", shortcut="Ctrl+V")
        self.paste_action.setIcon(QIcon(f"{self.icon_folder}/paste.png"))
        self.paste_action.triggered.connect(self.paste)

        self.main_menu = RoundMenu()
        self.main_menu.addAction(self.exit_full_screen_action)
        self.main_menu.setActionVisible(self.exit_full_screen_action, False)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.back_action)
        self.main_menu.addAction(self.forward_action)
        self.main_menu.addAction(self.home_action)
        self.main_menu.addAction(self.reload_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.go_to_youtube_action)
        self.main_menu.addMenu(self.download_menu)
        self.main_menu.addAction(self.watch_in_pip_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.settings_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.bug_report_action)
        self.main_menu.addAction(self.about_action)
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.hide_toolbar_action)

        self.download_menu.addAction(self.download_song_action)
        self.download_menu.addAction(self.download_album_action)
        self.download_menu.addSeparator()
        self.download_menu.addMenu(self.ytdlp_options_menu)

        self.ytdlp_options_menu.addAction(self.use_cookies_action)
        self.ytdlp_options_menu.addAction(self.convert_to_mp3_action)
        self.ytdlp_options_menu.addAction(self.auto_update_action)

        self.edit_menu = RoundMenu()
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)

        self.copy_menu = RoundMenu()
        self.copy_menu.addAction(self.copy_action)

        self.paste_menu = RoundMenu()
        self.paste_menu.addAction(self.paste_action)

    def configure_ui_elements(self):
        self.back_tbutton.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_tbutton.setEnabled(False)
        self.back_tbutton.clicked.connect(self.back)

        self.forward_tbutton.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_tbutton.setEnabled(False)
        self.forward_tbutton.clicked.connect(self.forward)

        self.home_tbutton.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_tbutton.clicked.connect(self.home)

        self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_tbutton.clicked.connect(self.reload)

        url_action = QAction(self)
        url_action.setIcon(QIcon(f"{self.icon_folder}/url.png"))
        url_action.triggered.connect(self.url_line_edit.selectAll)
        self.url_line_edit.addAction(url_action, QLineEdit.LeadingPosition)
        for button in self.url_line_edit.leftButtons:
            if button.action() == url_action:
                button.setIconSize(QSize(16, 16))
                break
        self.url_line_edit.returnPressed.connect(
            lambda: self.load_url(self.url_line_edit.text())
        )

        self.download_ddtbutton.setIcon(QIcon(f"{self.icon_folder}/download.png"))
        self.download_ddtbutton.setMenu(self.download_menu)

        self.watch_in_pip_tbutton.setIcon(
            QIcon(f"{self.icon_folder}/picture-in-picture.png")
        )
        self.watch_in_pip_tbutton.setEnabled(False)
        self.watch_in_pip_tbutton.clicked.connect(self.watch_in_pip)

        self.settings_tbutton.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_tbutton.clicked.connect(self.settings)

        self.bug_report_tbutton.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_tbutton.clicked.connect(self.bug_report)

        self.about_tbutton.setIcon(QIcon(f"{self.icon_folder}/about.png"))
        self.about_tbutton.clicked.connect(self.about)

        self.back_tbutton.installEventFilter(
            ToolTipFilter(self.back_tbutton, 300, ToolTipPosition.TOP)
        )
        self.forward_tbutton.installEventFilter(
            ToolTipFilter(self.forward_tbutton, 300, ToolTipPosition.TOP)
        )
        self.home_tbutton.installEventFilter(
            ToolTipFilter(self.home_tbutton, 300, ToolTipPosition.TOP)
        )
        self.reload_tbutton.installEventFilter(
            ToolTipFilter(self.reload_tbutton, 300, ToolTipPosition.TOP)
        )
        self.download_ddtbutton.installEventFilter(
            ToolTipFilter(self.download_ddtbutton, 300, ToolTipPosition.TOP)
        )
        self.watch_in_pip_tbutton.installEventFilter(
            ToolTipFilter(self.watch_in_pip_tbutton, 300, ToolTipPosition.TOP)
        )
        self.settings_tbutton.installEventFilter(
            ToolTipFilter(self.settings_tbutton, 300, ToolTipPosition.TOP)
        )
        self.bug_report_tbutton.installEventFilter(
            ToolTipFilter(self.bug_report_tbutton, 300, ToolTipPosition.TOP)
        )
        self.about_tbutton.installEventFilter(
            ToolTipFilter(self.about_tbutton, 300, ToolTipPosition.TOP)
        )

        self.ToolBar.installEventFilter(self)
        if self.hide_toolbar_setting == 1:
            QTimer.singleShot(0, lambda: self.ToolBar.hide())

    def activate_plugins(self):
        qtwebchannel = QWebEngineScript()
        file = QFile(":/qtwebchannel/qwebchannel.js")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            script_code = stream.readAll()
            qtwebchannel.setSourceCode(script_code)
            file.close()
        qtwebchannel.setInjectionPoint(QWebEngineScript.DocumentReady)
        qtwebchannel.setWorldId(QWebEngineScript.MainWorld)
        qtwebchannel.setRunsOnSubFrames(False)
        self.webpage.profile().scripts().insert(qtwebchannel)

        if self.ad_blocker_setting == 1:
            skip_video_ads_script = QWebEngineScript()
            skip_video_ads_script.setName("SkipVideoAds")
            skip_video_ads_script.setSourceCode(self.read_script("skip_video_ads.js"))
            skip_video_ads_script.setInjectionPoint(QWebEngineScript.Deferred)
            skip_video_ads_script.setWorldId(QWebEngineScript.MainWorld)
            skip_video_ads_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(skip_video_ads_script)

        scrollbar_styles_script = QWebEngineScript()
        scrollbar_styles_script.setName("ScrollbarStyles")
        scrollbar_styles_script.setSourceCode(self.read_script("scrollbar_styles.js"))
        scrollbar_styles_script.setInjectionPoint(QWebEngineScript.Deferred)
        scrollbar_styles_script.setWorldId(QWebEngineScript.MainWorld)
        scrollbar_styles_script.setRunsOnSubFrames(False)
        self.webpage.profile().scripts().insert(scrollbar_styles_script)

        self.run_discord_rpc()

        ytmusic_observer_script = QWebEngineScript()
        ytmusic_observer_script.setName("YtMusicObserver")
        ytmusic_observer_script.setSourceCode(self.read_script("ytmusic_observer.js"))
        ytmusic_observer_script.setInjectionPoint(QWebEngineScript.Deferred)
        ytmusic_observer_script.setWorldId(QWebEngineScript.MainWorld)
        ytmusic_observer_script.setRunsOnSubFrames(False)
        self.webpage.profile().scripts().insert(ytmusic_observer_script)

        if platform.system() == "Windows":
            self.win_thumbnail_toolbar = QWinThumbnailToolBar(self)
            self.create_previous_button()
            self.create_play_pause_button()
            self.create_next_button()
            self.win_thumbnail_toolbar.setWindow(self.windowHandle())
        else:
            self.win_thumbnail_toolbar = None

        if self.tray_icon_setting == 1:
            self.system_tray_icon = SystemTrayIcon(self.windowIcon(), self)
            self.system_tray_icon.show()
        else:
            self.system_tray_icon = None

        if self.hotkey_playback_control_setting == 1:
            self.hotkey_controller_thread = HotkeyController(self)
            self.hotkey_controller_thread.previous.connect(self.previous)
            self.hotkey_controller_thread.play_pause.connect(self.play_pause)
            self.hotkey_controller_thread.next.connect(self.next)
            self.hotkey_controller_thread.start()

        if self.only_audio_mode_setting == 1:
            audio_only_mode_source = f"""
            window.AUDIO_ONLY_MODE_SETTINGS = {{
                useHDThumbnails: {self.use_hd_thumbnails_setting}
            }};
            """ + self.read_script(
                "audio_only_mode.js"
            )

            audio_only_mode_script = QWebEngineScript()
            audio_only_mode_script.setName("AudioOnlyMode")
            audio_only_mode_script.setSourceCode(audio_only_mode_source)
            audio_only_mode_script.setInjectionPoint(QWebEngineScript.Deferred)
            audio_only_mode_script.setWorldId(QWebEngineScript.MainWorld)
            audio_only_mode_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(audio_only_mode_script)

            block_video_script = QWebEngineScript()
            block_video_script.setName("BlockVideo")
            block_video_script.setSourceCode(self.read_script("block_video.js"))
            block_video_script.setInjectionPoint(QWebEngineScript.DocumentCreation)
            block_video_script.setWorldId(QWebEngineScript.MainWorld)
            block_video_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(block_video_script)

        if self.nonstop_music_setting == 1:
            non_stop_music_script = QWebEngineScript()
            non_stop_music_script.setName("NonStopMusic")
            non_stop_music_script.setSourceCode(self.read_script("non_stop_music.js"))
            non_stop_music_script.setInjectionPoint(QWebEngineScript.Deferred)
            non_stop_music_script.setWorldId(QWebEngineScript.MainWorld)
            non_stop_music_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(non_stop_music_script)

        if self.hide_mini_player_setting == 1:
            hide_mini_player_script = QWebEngineScript()
            hide_mini_player_script.setName("HideMiniPlayer")
            hide_mini_player_script.setSourceCode(
                self.read_script("hide_mini_player.js")
            )
            hide_mini_player_script.setInjectionPoint(QWebEngineScript.Deferred)
            hide_mini_player_script.setWorldId(QWebEngineScript.MainWorld)
            hide_mini_player_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(hide_mini_player_script)

    def on_load_progress(self, progress):
        if progress > 80:
            self.reload_tbutton.setToolTip("Reload")
            self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
            self.reload_tbutton.clicked.disconnect()
            self.reload_tbutton.clicked.connect(self.reload)

            self.reload_action.setText("Reload")
            self.reload_action.setShortcut("Ctrl+R")
            self.reload_action.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
            self.reload_action.triggered.disconnect()
            self.reload_action.triggered.connect(self.reload)

            self.stop_shortcut.setEnabled(False)

            if self.splash_screen is not None:
                self.close_splash_screen()
                self.check_updates()

                if self.proxy_error_message is not None:
                    self.show_error_message(self.proxy_error_message, "Proxy Error")
                    self.proxy_error_message = None

    def on_load_started(self):
        self.reload_tbutton.setToolTip("Stop")
        self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/close.png"))
        self.reload_tbutton.clicked.disconnect()
        self.reload_tbutton.clicked.connect(self.stop)

        self.reload_action.setText("Stop")
        self.reload_action.setShortcut("Esc")
        self.reload_action.setIcon(QIcon(f"{self.icon_folder}/close.png"))
        self.reload_action.triggered.disconnect()
        self.reload_action.triggered.connect(self.reload)

        self.stop_shortcut.setEnabled(True)

    def close_splash_screen(self):
        self.splash_screen.deleteLater()
        self.splash_screen = None

    def check_updates(self):
        self.update_checker_thread = UpdateChecker(self)
        self.update_checker_thread.update_checked.connect(self.on_update_checked)
        self.update_checker_thread.start()

    def on_update_checked(self, last_version, title, whats_new, last_release_url):
        self.update_checker_thread = None

        if pkg_version.parse(self.version) < pkg_version.parse(last_version):
            msg_box = MessageBox(title, whats_new, self)
            msg_box.yesButton.setText("Download")
            msg_box.cancelButton.setText("Later")
            if msg_box.exec_():
                open_url(last_release_url)
                self.force_exit = True
                self.close()

    def on_fullscreen_requested(self, request):
        if not self.isFullScreen():
            self.ToolBar.hide()
            self.showFullScreen()
            self.main_menu.setActionVisible(self.exit_full_screen_action, True)
        else:
            if self.hide_toolbar_setting == 0:
                self.ToolBar.show()
            self.showNormal()
            self.main_menu.setActionVisible(self.exit_full_screen_action, False)

        request.accept()

    def exit_full_screen(self):
        self.webpage.triggerAction(QWebEnginePage.WebAction.ExitFullScreen)

    def on_url_changed(self, url):
        self.current_url = url.toString()
        self.url_line_edit.setText(self.current_url)
        self.url_line_edit.setCursorPosition(0)

        can_go_back = self.webview.history().canGoBack()
        can_go_forward = self.webview.history().canGoForward()
        self.back_action.setEnabled(can_go_back)
        self.back_tbutton.setEnabled(can_go_back)
        self.forward_action.setEnabled(can_go_forward)
        self.forward_tbutton.setEnabled(can_go_forward)

        self.update_download_buttons_state()

    def run_discord_rpc(self):
        if self.discord_rpc_setting == 1:
            try:
                self.discord_rpc = RPC(
                    app_id="1254202610781655050",
                    output=False,
                    exit_if_discord_close=False,
                    exit_on_disconnect=False,
                )
            except Exception as e:
                self.discord_rpc = None
                logging.error(f"Failed to activate Discord RPC: {str(e)}")

    def update_discord_rpc(self):
        if not self.discord_rpc:
            self.run_discord_rpc()

        if self.discord_rpc:
            details = self.title[:128]
            state = self.artist[:128]
            large_image = self.artwork
            small_image = (
                "https://cdn.discordapp.com/app-icons/1254202610781655050/"
                "b4ede41d663f6caa7e45c6a042e447c9.png?size=32"
            )
            project_url = f"https://github.com/{self.author}/{self.name}"
            video_url = f"https://music.youtube.com/watch?v={self.video_id}"

            try:
                self.discord_rpc.set_activity(
                    details=details,
                    state=state,
                    large_image=large_image,
                    small_image=small_image,
                    act_type=Activity.Listening,
                    **ProgressBar(0, self.duration),
                    buttons=[
                        Button("Play in Browser", video_url),
                        Button("Get App on GitHub", project_url),
                    ],
                )
            except Exception as e:
                if "[Errno 22]" in str(e) or "[Errno 32]" in str(e):
                    self.reconnect_discord_rpc()
                else:
                    logging.error(f"Failed to update Discord RPC: {str(e)}")

    def clear_discord_rpc(self):
        if self.discord_rpc:
            try:
                self.discord_rpc.clear()
            except Exception as e:
                logging.error(f"Failed to clear Discord RPC: {str(e)}")

    def reconnect_discord_rpc(self):
        if self.discord_rpc:
            self.run_discord_rpc()
            self.update_discord_rpc()

    def update_system_tray_icon_song_state(self):
        if self.tray_icon_setting == 1 and self.system_tray_icon:
            if self.song_state == "Playing":
                self.system_tray_icon.play_pause_action.setIcon(
                    QIcon(f"{self.icon_folder}/pause.png")
                )
                self.system_tray_icon.play_pause_action.setEnabled(True)
                self.system_tray_icon.like_action.setEnabled(True)
                self.system_tray_icon.previous_action.setEnabled(True)
                self.system_tray_icon.next_action.setEnabled(True)
                self.system_tray_icon.dislike_action.setEnabled(True)
            elif self.song_state == "Paused":
                self.system_tray_icon.play_pause_action.setIcon(
                    QIcon(f"{self.icon_folder}/play.png")
                )
                self.system_tray_icon.play_pause_action.setEnabled(True)
                self.system_tray_icon.like_action.setEnabled(True)
                self.system_tray_icon.previous_action.setEnabled(True)
                self.system_tray_icon.next_action.setEnabled(True)
                self.system_tray_icon.dislike_action.setEnabled(True)
            else:
                self.system_tray_icon.play_pause_action.setIcon(
                    QIcon(f"{self.icon_folder}/play.png")
                )
                self.system_tray_icon.play_pause_action.setEnabled(False)
                self.system_tray_icon.like_action.setEnabled(False)
                self.system_tray_icon.previous_action.setEnabled(False)
                self.system_tray_icon.next_action.setEnabled(False)
                self.system_tray_icon.dislike_action.setEnabled(False)

    def update_system_tray_icon_song_status(self):
        if self.tray_icon_setting == 1 and self.system_tray_icon:
            if self.song_status == "Like":
                self.system_tray_icon.like_action.setIcon(
                    QIcon(f"{self.icon_folder}/like-filled.png")
                )
                self.system_tray_icon.dislike_action.setIcon(
                    QIcon(f"{self.icon_folder}/dislike.png")
                )
            elif self.song_status == "Dislike":
                self.system_tray_icon.like_action.setIcon(
                    QIcon(f"{self.icon_folder}/like.png")
                )
                self.system_tray_icon.dislike_action.setIcon(
                    QIcon(f"{self.icon_folder}/dislike-filled.png")
                )
            else:
                self.system_tray_icon.like_action.setIcon(
                    QIcon(f"{self.icon_folder}/like.png")
                )
                self.system_tray_icon.dislike_action.setIcon(
                    QIcon(f"{self.icon_folder}/dislike.png")
                )

    def update_win_thumbnail_buttons_song_state(self):
        if self.win_thumbnail_toolbar:
            if self.song_state == "Playing":
                self.tool_btn_previous.setIcon(
                    QIcon(f"{self.icon_folder}/previous-filled-border.png")
                )
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/pause-filled-border.png")
                )
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setIcon(
                    QIcon(f"{self.icon_folder}/next-filled-border.png")
                )
                self.tool_btn_next.setEnabled(True)
            elif self.song_state == "Paused":
                self.tool_btn_previous.setIcon(
                    QIcon(f"{self.icon_folder}/previous-filled-border.png")
                )
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled-border.png")
                )
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setIcon(
                    QIcon(f"{self.icon_folder}/next-filled-border.png")
                )
                self.tool_btn_next.setEnabled(True)
            else:
                self.tool_btn_previous.setIcon(
                    QIcon(f"{self.icon_folder}/previous-filled-border-disabled.png")
                )
                self.tool_btn_previous.setEnabled(False)
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled-border-disabled.png")
                )
                self.tool_btn_play_pause.setEnabled(False)
                self.tool_btn_next.setIcon(
                    QIcon(f"{self.icon_folder}/next-filled-border-disabled.png")
                )
                self.tool_btn_next.setEnabled(False)

    def update_picture_in_picture_song_info(self):
        if self.picture_in_picture_dialog:
            self.picture_in_picture_dialog.title_label.setText(self.title)
            self.picture_in_picture_dialog.title_label.setToolTip(self.title)
            self.picture_in_picture_dialog.artist_label.setText(self.artist)
            self.picture_in_picture_dialog.artist_label.setToolTip(self.artist)
            self.picture_in_picture_dialog.load_artwork(self.artwork)

    def update_picture_in_picture_song_state(self):
        if self.picture_in_picture_dialog:
            if self.song_state == "Playing":
                self.picture_in_picture_dialog.dislike_button.setEnabled(True)
                self.picture_in_picture_dialog.previous_button.setEnabled(True)
                self.picture_in_picture_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/pause-filled.png")
                )
                self.picture_in_picture_dialog.play_pause_button.setEnabled(True)
                self.picture_in_picture_dialog.next_button.setEnabled(True)
                self.picture_in_picture_dialog.like_button.setEnabled(True)
            elif self.song_state == "Paused":
                self.picture_in_picture_dialog.dislike_button.setEnabled(True)
                self.picture_in_picture_dialog.previous_button.setEnabled(True)
                self.picture_in_picture_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled.png")
                )
                self.picture_in_picture_dialog.play_pause_button.setEnabled(True)
                self.picture_in_picture_dialog.next_button.setEnabled(True)
                self.picture_in_picture_dialog.like_button.setEnabled(True)
            else:
                self.picture_in_picture_dialog.dislike_button.setEnabled(False)
                self.picture_in_picture_dialog.previous_button.setEnabled(False)
                self.picture_in_picture_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled.png")
                )
                self.picture_in_picture_dialog.play_pause_button.setEnabled(False)
                self.picture_in_picture_dialog.next_button.setEnabled(False)
                self.picture_in_picture_dialog.like_button.setEnabled(False)

    def update_picture_in_picture_song_progress(self):
        if self.picture_in_picture_dialog:
            self.picture_in_picture_dialog.BodyLabel.setText(self.current_time)
            self.picture_in_picture_dialog.BodyLabel_2.setText(self.total_time)

    def update_picture_in_picture_song_status(self):
        if self.picture_in_picture_dialog:
            if self.song_status == "Like":
                self.picture_in_picture_dialog.dislike_button.setIcon(
                    QIcon(f"{self.icon_folder}/dislike.png")
                )
                self.picture_in_picture_dialog.like_button.setIcon(
                    QIcon(f"{self.icon_folder}/like-filled.png")
                )
            elif self.song_status == "Dislike":
                self.picture_in_picture_dialog.dislike_button.setIcon(
                    QIcon(f"{self.icon_folder}/dislike-filled.png")
                )
                self.picture_in_picture_dialog.like_button.setIcon(
                    QIcon(f"{self.icon_folder}/like.png")
                )
            else:
                self.picture_in_picture_dialog.dislike_button.setIcon(
                    QIcon(f"{self.icon_folder}/dislike.png")
                )
                self.picture_in_picture_dialog.like_button.setIcon(
                    QIcon(f"{self.icon_folder}/like.png")
                )

    def create_previous_button(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_previous.setToolTip("Previous")
        self.tool_btn_previous.setEnabled(False)
        self.tool_btn_previous.setIcon(
            QIcon(f"{self.icon_folder}/previous-filled-border-disabled.png")
        )
        self.tool_btn_previous.clicked.connect(self.previous)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_previous)

    def create_play_pause_button(self):
        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_play_pause.setToolTip("Play/Pause")
        self.tool_btn_play_pause.setEnabled(False)
        self.tool_btn_play_pause.setIcon(
            QIcon(f"{self.icon_folder}/play-filled-border-disabled.png")
        )
        self.tool_btn_play_pause.clicked.connect(self.play_pause)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_play_pause)

    def create_next_button(self):
        self.tool_btn_next = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_next.setToolTip("Next")
        self.tool_btn_next.setEnabled(False)
        self.tool_btn_next.setIcon(
            QIcon(f"{self.icon_folder}/next-filled-border-disabled.png")
        )
        self.tool_btn_next.clicked.connect(self.next)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_next)

    def dislike(self):
        self.run_js_script("dislike.js")

    def previous(self):
        self.run_js_script("previous.js")

    def play_pause(self):
        self.run_js_script("play_pause.js")

    def next(self):
        self.run_js_script("next.js")

    def like(self):
        self.run_js_script("like.js")

    def run_js_script(self, script_name):
        self.webpage.runJavaScript(self.read_script(script_name))

    def read_script(self, filename):
        with open(f"{self.current_dir}/core/js/{filename}", "r", encoding="utf-8") as f:
            return f.read()

    def back(self):
        self.webview.back()

    def forward(self):
        self.webview.forward()

    def home(self):
        self.webview.load(QUrl("https://music.youtube.com/"))

    def reload(self):
        self.webview.reload()

    def stop(self):
        self.webview.stop()

    def go_to_youtube(self):
        open_url(f"https://www.youtube.com/watch?v={self.video_id}")

    def select_download_folder(self):
        title = "Select Folder"
        folder = QFileDialog.getExistingDirectory(
            self, title, self.last_download_folder_setting
        )
        return folder if folder else None

    def download_song(self):
        self.start_download(f"https://music.youtube.com/watch?v={self.video_id}")

    def download_album(self):
        self.start_download(self.current_url)

    def start_download(self, download_url):
        download_folder = self.select_download_folder()
        if not download_folder:
            return

        self.last_download_folder_setting = download_folder
        self.settings_.setValue("last_download_folder", download_folder)

        self.is_downloading = True
        self.update_download_buttons_state()

        self.download_thread = DownloadThread(
            download_url,
            download_folder,
            use_cookies=self.use_cookies_action.isChecked(),
            convert_to_mp3=self.convert_to_mp3_action.isChecked(),
            auto_update=self.auto_update_action.isChecked(),
            parent=self,
        )
        self.download_thread.downloading_ffmpeg.connect(self.on_downloading_ffmpeg)
        self.download_thread.downloading_ffmpeg_success.connect(
            self.on_downloading_ffmpeg_success
        )

        self.download_thread.downloading_deno.connect(self.on_downloading_deno)
        self.download_thread.downloading_deno_success.connect(
            self.on_downloading_deno_success
        )

        self.download_thread.downloading_ytdlp.connect(self.on_downloading_ytdlp)
        self.download_thread.downloading_ytdlp_success.connect(
            self.on_downloading_ytdlp_success
        )

        self.download_thread.downloading_audio.connect(self.on_downloading_audio)
        self.download_thread.downloading_audio_error.connect(
            self.on_downloading_audio_error
        )
        self.download_thread.downloading_audio_success.connect(
            self.on_downloading_audio_success
        )

        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def show_downloading_state_tooltip(self, title, content):
        def calculate_tooltip_pos(
            parent_widget,
            tooltip_widget,
            margin=20,
            top_offset=63 if self.hide_toolbar_setting == 0 else 20,
        ):
            parent_width = parent_widget.width()
            parent_height = parent_widget.height()

            tooltip_width = tooltip_widget.width()
            tooltip_height = tooltip_widget.height()

            x = parent_width - tooltip_width - margin
            y = top_offset

            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x + tooltip_width > parent_width:
                x = parent_width - tooltip_width
            if y + tooltip_height > parent_height:
                y = parent_height - tooltip_height

            return QPoint(x, y)

        self.downloading_state_tool_tip = StateToolTip(title, content, self)
        pos = calculate_tooltip_pos(self, self.downloading_state_tool_tip)
        self.downloading_state_tool_tip.move(pos)
        self.downloading_state_tool_tip.show()

    def hide_downloading_state_tooltip(self):
        if self.downloading_state_tool_tip is not None:
            self.downloading_state_tool_tip.setState(True)
            self.downloading_state_tool_tip = None

    def on_downloading_ffmpeg(self):
        self.show_downloading_state_tooltip("Downloading ffmpeg", "Please wait...")

    def on_downloading_ffmpeg_success(self):
        self.hide_downloading_state_tooltip()

    def on_downloading_deno(self):
        self.show_downloading_state_tooltip("Downloading deno", "Please wait...")

    def on_downloading_deno_success(self):
        self.hide_downloading_state_tooltip()

    def on_downloading_ytdlp(self):
        self.show_downloading_state_tooltip("Downloading yt-dlp", "Please wait...")

    def on_downloading_ytdlp_success(self):
        self.hide_downloading_state_tooltip()

    def on_downloading_audio(self):
        self.show_downloading_state_tooltip("Downloading audio", "Please wait...")

    def on_downloading_audio_error(self, msg, title):
        self.hide_downloading_state_tooltip()

        info_bar = InfoBar.error(
            title=f"{title}",
            content="Audio downloaded failed!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self,
        )

        button = PushButton(QIcon(f"{self.icon_folder}/show.png"), "Show Error", self)
        button.clicked.connect(lambda: self.show_download_error(msg, info_bar))
        info_bar.addWidget(button)

    def on_downloading_audio_success(self, folder, title):
        self.hide_downloading_state_tooltip()

        info_bar = InfoBar.success(
            title=f"{title}",
            content="Audio downloaded successfully!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self,
        )

        button = PushButton(
            QIcon(f"{self.icon_folder}/open_folder.png"), "Open Folder", self
        )
        button.clicked.connect(lambda: self.open_download_folder(folder, info_bar))
        info_bar.addWidget(button)

    def show_download_error(self, msg, info_bar):
        info_bar.close()

        QTimer.singleShot(0, lambda: self.show_error_message(msg, "yt-dlp Error"))

    def open_download_folder(self, folder, info_bar):
        info_bar.close()
        open_url(folder)

    def on_download_finished(self):
        self.download_thread = None
        self.hide_downloading_state_tooltip()

        self.is_downloading = False
        self.update_download_buttons_state()

    def update_download_buttons_state(self):
        can_download_song = not self.is_downloading and bool(self.video_id)
        can_download_album = not self.is_downloading and "playlist" in self.current_url

        self.download_song_action.setEnabled(can_download_song)
        self.download_song_shortcut.setEnabled(can_download_song)
        self.download_album_action.setEnabled(can_download_album)
        self.download_album_shortcut.setEnabled(can_download_album)

    def watch_in_pip(self):
        if self.song_state == "Playing" or "Paused":
            self.show_picture_in_picture()
            self.hide()
            self.hide_system_tray_icon()

    def show_picture_in_picture(self):
        self.picture_in_picture_dialog = PictureInPictureDialog(self)
        self.update_picture_in_picture_song_info()
        self.update_picture_in_picture_song_state()
        self.update_picture_in_picture_song_progress()
        self.update_picture_in_picture_song_status()
        self.picture_in_picture_dialog.show()
        self.picture_in_picture_dialog.activateWindow()

    def show_system_tray_icon(self):
        if self.system_tray_icon:
            self.system_tray_icon.show()

    def hide_system_tray_icon(self):
        if self.system_tray_icon:
            self.system_tray_icon.hide()

    def load_url(self, url):
        self.webview.load(QUrl(url))

    def settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def bug_report(self):
        open_url(f"https://github.com/{self.author}/{self.name}/issues")

    def hide_toolbar(self):
        if self.ToolBar.isHidden():
            self.ToolBar.show()
            self.hide_toolbar_setting = 0
        else:
            self.ToolBar.hide()
            self.hide_toolbar_setting = 1

    def cut(self):
        self.webpage.triggerAction(QWebEnginePage.Cut)

    def copy(self):
        self.webpage.triggerAction(QWebEnginePage.Copy)

    def paste(self):
        self.webpage.triggerAction(QWebEnginePage.Paste)

    def save_settings(self):
        if self.open_last_url_at_startup_setting == 1 and is_valid_ytmusic_url(
            self.current_url
        ):
            self.last_url_setting = self.current_url
            self.settings_.setValue("last_url", self.last_url_setting)

        if self.save_last_win_geometry_setting == 1:
            if not self.isMaximized() and not self.isFullScreen():
                self.last_win_geometry_setting = self.geometry()
                self.settings_.setValue(
                    "last_win_geometry", self.last_win_geometry_setting
                )

        if self.save_last_zoom_factor_setting == 1:
            self.last_zoom_factor_setting = self.webview.zoomFactor()
            self.settings_.setValue("last_zoom_factor", self.last_zoom_factor_setting)

        self.settings_.setValue("hide_toolbar", self.hide_toolbar_setting)
        self.settings_.setValue("use_cookies", self.use_cookies_action.isChecked())
        self.settings_.setValue(
            "convert_to_mp3", self.convert_to_mp3_action.isChecked()
        )
        self.settings_.setValue(
            "auto_update_ytdlp", self.auto_update_action.isChecked()
        )

    def show_window(self):
        if self.isMinimized() or self.isHidden():
            if self.isMinimized():
                self.showNormal()
            else:
                self.show()
        self.activateWindow()

    def show_window_or_picture_in_picture(self):
        if self.picture_in_picture_dialog is None:
            self.show_window()
        else:
            if self.picture_in_picture_dialog.isMinimized():
                self.picture_in_picture_dialog.showNormal()

    def eventFilter(self, obj, event):
        if obj == self.ToolBar:
            if event.type() == QEvent.Show:
                self.hide_toolbar_action.setText("Hide Toolbar")
                self.hide_toolbar_action.setIcon(
                    QIcon(f"{self.icon_folder}/hide_toolbar.png")
                )
            elif event.type() == QEvent.Hide:
                self.hide_toolbar_action.setText("Show Toolbar")
                self.hide_toolbar_action.setIcon(
                    QIcon(f"{self.icon_folder}/toolbar.png")
                )
        return super().eventFilter(obj, event)

    def stop_running_threads(self):
        if (
            self.hotkey_controller_thread is not None
            and self.hotkey_controller_thread.isRunning()
        ):
            self.hotkey_controller_thread.stop()

        if self.download_thread is not None and self.download_thread.isRunning():
            self.download_thread.stop()

        if (
            self.update_checker_thread is not None
            and self.update_checker_thread.isRunning()
        ):
            self.update_checker_thread.stop()

    def app_quit(self):
        self.stop_running_threads()

    def closeEvent(self, event):
        self.save_settings()

        if self.tray_icon_setting == 1 and self.system_tray_icon is not None:
            if not self.force_exit:
                self.hide()
                event.ignore()
                return

        if self.song_state == "Playing":
            self.show_window()

            msg_box = MessageBox(
                "Exit Confirmation",
                (
                    "Exiting now will stop the current playback and "
                    "close the application.\n"
                    "Do you want to exit now?"
                ),
                self,
            )
            msg_box.yesButton.setText("Exit")
            if not msg_box.exec_():
                self.force_exit = False
                event.ignore()
                return

        event.accept()
