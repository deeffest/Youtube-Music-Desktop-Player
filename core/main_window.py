import logging
import platform
import traceback
import webbrowser

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
from PyQt5.QtGui import QIcon, QKeySequence, QDesktopServices
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
from discordrpc import RPC, Button

from core.about_dialog import AboutDialog
from core.mini_player_dialog import MiniPlayerDialog
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
)
from core.ui.ui_main_window import Ui_MainWindow
from core.hotkey_controller import HotkeyController
from core.text_view_dialog import TextViewDialog
from core.signal_bus import signal_bus

if platform.system() == "Windows":
    from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton # type: ignore
    from pywinstyles import apply_style # type: ignore


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app_settings, opengl_enviroment_setting, app_info):
        super().__init__()
        self.name = app_info[0]
        self.app_author = app_info[1]
        self.version = app_info[2]
        self.current_dir = app_info[3]
        self.icon_folder = f"{self.current_dir}/resources/icons"

        self.title = "Unknown"
        self.author = "Unknown"
        self.thumbnail_url = None
        self.video_id = None
        self.current_url = None
        self.current_time = "NaN"
        self.total_time = "NaN"
        self.video_state = None
        self.is_video_or_playlist = False
        self.proxy_error_message = None

        self.force_exit = False
        self.is_downloading = False

        self.settings_ = app_settings
        self.opengl_enviroment_setting = opengl_enviroment_setting

        self.mini_player_dialog = None
        self.download_thread = None
        self.update_checker_thread = None
        self.hotkey_controller_thread = None
        self.downloading_state_tool_tip = None

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
            self.settings_.setValue("save_last_pos_of_mp", 1)
        if self.settings_.value("last_win_geometry") is None:
            self.settings_.setValue(
                "last_win_geometry", QRect(get_centered_geometry(1000, 799))
            )
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
        self.save_geometry_of_mp_setting = int(
            self.settings_.value("save_geometry_of_mp")
        )
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
        signal_bus.show_window_sig.connect(self.show_window_or_mini_player)
        signal_bus.app_error_sig.connect(self.show_error_message)

    def show_error_message(self, msg, title=None):
        text_view_dialog = TextViewDialog(
            f"{title}" if title else "Unhandled exception", msg, self
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
        self.back_shortcut.activated.connect(self.go_back)

        self.forward_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Right), self)
        self.forward_shortcut.activated.connect(self.go_forward)

        self.home_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_H), self)
        self.home_shortcut.activated.connect(self.go_to_home)

        self.reload_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self)
        self.reload_shortcut.activated.connect(self.reload_page)

        self.stop_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.stop_shortcut.setEnabled(False)
        self.stop_shortcut.activated.connect(self.stop)

        self.download_with_oauth_shortcut = QShortcut(
            QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_D), self
        )
        self.download_with_oauth_shortcut.setEnabled(False)
        self.download_with_oauth_shortcut.activated.connect(
            lambda: self.start_download(use_cookies=True)
        )

        self.download_as_unauthorized_shortcut = QShortcut(
            QKeySequence(Qt.CTRL + Qt.Key_D), self
        )
        self.download_as_unauthorized_shortcut.setEnabled(False)
        self.download_as_unauthorized_shortcut.activated.connect(
            lambda: self.start_download(use_cookies=False)
        )

        self.mini_player_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), self)
        self.mini_player_shortcut.setEnabled(False)
        self.mini_player_shortcut.activated.connect(self.open_mini_player)

        self.settings_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.settings_shortcut.activated.connect(self.open_settings)

        self.hide_toolbar_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), self)
        self.hide_toolbar_shortcut.activated.connect(self.hide_toolbar)

    def show_splash_screen(self):
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(102, 102))
        self.splash_screen.titleBar.hide()

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
        self.back_action = Action("Back", shortcut="Alt+Left")
        self.back_action.setIcon(QIcon(f"{self.icon_folder}/left.png"))
        self.back_action.setEnabled(False)
        self.back_action.triggered.connect(self.go_back)

        self.forward_action = Action("Forward", shortcut="Alt+Right")
        self.forward_action.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_action.setEnabled(False)
        self.forward_action.triggered.connect(self.go_forward)

        self.home_action = Action("Home", shortcut="Ctrl+H")
        self.home_action.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_action.triggered.connect(self.go_to_home)

        self.reload_action = Action("Reload", shortcut="Ctrl+R")
        self.reload_action.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_action.triggered.connect(self.reload_page)

        self.download_with_oauth_action = Action("Signed In", shortcut="Ctrl+Shift+D")
        self.download_with_oauth_action.setIcon(
            QIcon(f"{self.icon_folder}/authorized.png")
        )
        self.download_with_oauth_action.setEnabled(True)
        self.download_with_oauth_action.triggered.connect(
            lambda: self.start_download(use_cookies=True)
        )

        self.download_as_unauthorized_action = Action("Guest Mode", shortcut="Ctrl+D")
        self.download_as_unauthorized_action.setIcon(
            QIcon(f"{self.icon_folder}/unauthorized.png")
        )
        self.download_as_unauthorized_action.setEnabled(False)
        self.download_as_unauthorized_action.triggered.connect(
            lambda: self.start_download(use_cookies=False)
        )

        self.mini_player_action = Action("Mini-Player", shortcut="Ctrl+M")
        self.mini_player_action.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_action.setEnabled(False)
        self.mini_player_action.triggered.connect(self.open_mini_player)

        self.settings_action = Action("Settings", shortcut="Ctrl+S")
        self.settings_action.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_action.triggered.connect(self.open_settings)

        self.bug_report_action = Action("Bug Report")
        self.bug_report_action.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_action.triggered.connect(self.send_bug_report)

        self.about_action = Action("About")
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

        self.download_menu = RoundMenu("Get Audio", self)
        self.download_menu.setIcon(QIcon(f"{self.icon_folder}/download.png"))
        self.download_menu.addAction(self.download_with_oauth_action)
        self.download_menu.addAction(self.download_as_unauthorized_action)

        self.main_menu = RoundMenu()
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
        self.main_menu.addSeparator()
        self.main_menu.addAction(self.hide_toolbar_action)

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
        self.back_tbutton.installEventFilter(
            ToolTipFilter(self.back_tbutton, 300, ToolTipPosition.TOP)
        )
        self.back_tbutton.clicked.connect(self.go_back)

        self.forward_tbutton.setIcon(QIcon(f"{self.icon_folder}/right.png"))
        self.forward_tbutton.setEnabled(False)
        self.forward_tbutton.installEventFilter(
            ToolTipFilter(self.forward_tbutton, 300, ToolTipPosition.TOP)
        )
        self.forward_tbutton.clicked.connect(self.go_forward)

        self.home_tbutton.setIcon(QIcon(f"{self.icon_folder}/home.png"))
        self.home_tbutton.installEventFilter(
            ToolTipFilter(self.home_tbutton, 300, ToolTipPosition.TOP)
        )
        self.home_tbutton.clicked.connect(self.go_to_home)

        self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
        self.reload_tbutton.installEventFilter(
            ToolTipFilter(self.reload_tbutton, 300, ToolTipPosition.TOP)
        )
        self.reload_tbutton.clicked.connect(self.reload_page)

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
        self.download_ddtbutton.installEventFilter(
            ToolTipFilter(self.download_ddtbutton, 300, ToolTipPosition.TOP)
        )

        self.mini_player_tbutton.setIcon(QIcon(f"{self.icon_folder}/mini-player.png"))
        self.mini_player_tbutton.setEnabled(False)
        self.mini_player_tbutton.installEventFilter(
            ToolTipFilter(self.mini_player_tbutton, 300, ToolTipPosition.TOP)
        )
        self.mini_player_tbutton.clicked.connect(self.open_mini_player)

        self.settings_tbutton.setIcon(QIcon(f"{self.icon_folder}/settings.png"))
        self.settings_tbutton.installEventFilter(
            ToolTipFilter(self.settings_tbutton, 300, ToolTipPosition.TOP)
        )
        self.settings_tbutton.clicked.connect(self.open_settings)

        self.bug_report_tbutton.setIcon(QIcon(f"{self.icon_folder}/bug.png"))
        self.bug_report_tbutton.installEventFilter(
            ToolTipFilter(self.bug_report_tbutton, 300, ToolTipPosition.TOP)
        )
        self.bug_report_tbutton.clicked.connect(self.send_bug_report)

        self.about_tbutton.setIcon(QIcon(f"{self.icon_folder}/about.png"))
        self.about_tbutton.installEventFilter(
            ToolTipFilter(self.about_tbutton, 300, ToolTipPosition.TOP)
        )
        self.about_tbutton.clicked.connect(self.about)

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
            ad_blocker_plugin = QWebEngineScript()
            ad_blocker_plugin.setName("AdBlocker")
            ad_blocker_plugin.setSourceCode(self.read_script("ad_blocker.js"))
            ad_blocker_plugin.setInjectionPoint(QWebEngineScript.Deferred)
            ad_blocker_plugin.setWorldId(QWebEngineScript.MainWorld)
            ad_blocker_plugin.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(ad_blocker_plugin)

        scrollbar_styles_plugin = QWebEngineScript()
        scrollbar_styles_plugin.setName("ScrollbarStyles")
        scrollbar_styles_plugin.setSourceCode(self.read_script("scrollbar_styles.js"))
        scrollbar_styles_plugin.setInjectionPoint(QWebEngineScript.Deferred)
        scrollbar_styles_plugin.setWorldId(QWebEngineScript.MainWorld)
        scrollbar_styles_plugin.setRunsOnSubFrames(False)
        self.webpage.profile().scripts().insert(scrollbar_styles_plugin)

        self.run_discord_rpc()

        ytmusic_observer_plugin = QWebEngineScript()
        ytmusic_observer_plugin.setName("YtMusicObserver")
        ytmusic_observer_plugin.setSourceCode(self.read_script("ytmusic_observer.js"))
        ytmusic_observer_plugin.setInjectionPoint(QWebEngineScript.Deferred)
        ytmusic_observer_plugin.setWorldId(QWebEngineScript.MainWorld)
        ytmusic_observer_plugin.setRunsOnSubFrames(False)
        self.webpage.profile().scripts().insert(ytmusic_observer_plugin)

        if platform.system() == "Windows":
            self.win_thumbnail_toolbar = QWinThumbnailToolBar(self)
            self.create_volume_down_button()
            self.create_previous_button()
            self.create_play_pause_button()
            self.create_next_button()
            self.create_volume_up_button()
            self.win_thumbnail_toolbar.setWindow(self.windowHandle())
        else:
            self.win_thumbnail_toolbar = None

        if self.tray_icon_setting == 1:
            self.tray_icon = SystemTrayIcon(self.windowIcon(), self)
            self.tray_icon.show()
        else:
            self.tray_icon = None

        if self.hotkey_playback_control_setting == 1:
            self.hotkey_controller_thread = HotkeyController(self)
            self.hotkey_controller_thread.play_pause.connect(self.play_pause)
            self.hotkey_controller_thread.skip_next.connect(self.skip_next)
            self.hotkey_controller_thread.skip_previous.connect(self.skip_previous)
            self.hotkey_controller_thread.volume_up.connect(self.volume_up)
            self.hotkey_controller_thread.volume_down.connect(self.volume_down)
            self.hotkey_controller_thread.start()

        if self.only_audio_mode_setting == 1:
            only_audio_source = f"""
            window.ONLY_AUDIO_SETTINGS = {{
                useHDThumbnails: {self.use_hd_thumbnails_setting}
            }};
            """ + self.read_script(
                "only_audio.js"
            )

            only_audio_script = QWebEngineScript()
            only_audio_script.setName("OnlyAudio")
            only_audio_script.setSourceCode(only_audio_source)
            only_audio_script.setInjectionPoint(QWebEngineScript.Deferred)
            only_audio_script.setWorldId(QWebEngineScript.MainWorld)
            only_audio_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(only_audio_script)

            block_video_script = QWebEngineScript()
            block_video_script.setName("BlockVideo")
            block_video_script.setSourceCode(self.read_script("block_video.js"))
            block_video_script.setInjectionPoint(QWebEngineScript.DocumentCreation)
            block_video_script.setWorldId(QWebEngineScript.MainWorld)
            block_video_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(block_video_script)

        if self.nonstop_music_setting == 1:
            nonstop_music_script = QWebEngineScript()
            nonstop_music_script.setName("NonstopMusic")
            nonstop_music_script.setSourceCode(self.read_script("nonstop_music.js"))
            nonstop_music_script.setInjectionPoint(QWebEngineScript.Deferred)
            nonstop_music_script.setWorldId(QWebEngineScript.MainWorld)
            nonstop_music_script.setRunsOnSubFrames(False)
            self.webpage.profile().scripts().insert(nonstop_music_script)

    def on_load_progress(self, progress):
        if progress > 80:
            self.reload_tbutton.setToolTip("Reload")
            self.reload_tbutton.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
            self.reload_tbutton.clicked.disconnect()
            self.reload_tbutton.clicked.connect(self.reload_page)

            self.reload_action.setText("Reload")
            self.reload_action.setShortcut("Ctrl+R")
            self.reload_action.setIcon(QIcon(f"{self.icon_folder}/reload.png"))
            self.reload_action.triggered.disconnect()
            self.reload_action.triggered.connect(self.reload_page)

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
        self.reload_action.triggered.connect(self.reload_page)

        self.stop_shortcut.setEnabled(True)

    def close_splash_screen(self):
        self.splash_screen.finish()
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
                webbrowser.open_new_tab(last_release_url)
                self.force_exit = True
                self.close()

    def on_fullscreen_requested(self, request):
        if not self.isFullScreen():
            self.ToolBar.hide()
            self.showFullScreen()
        else:
            if self.hide_toolbar_setting == 0:
                self.ToolBar.show()
            self.showNormal()

        request.accept()

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

        self.is_video_or_playlist = (
            "watch" in self.current_url or "playlist" in self.current_url
        )
        if not self.is_downloading:
            self.download_with_oauth_action.setEnabled(self.is_video_or_playlist)
            self.download_as_unauthorized_action.setEnabled(self.is_video_or_playlist)
            self.download_with_oauth_shortcut.setEnabled(self.is_video_or_playlist)
            self.download_as_unauthorized_shortcut.setEnabled(self.is_video_or_playlist)

    def update_mini_player_track_info(self):
        if self.mini_player_dialog:
            self.mini_player_dialog.title_label.setText(self.title)
            self.mini_player_dialog.title_label.setToolTip(self.title)
            self.mini_player_dialog.author_label.setText(self.author)
            self.mini_player_dialog.author_label.setToolTip(self.author)
            self.mini_player_dialog.load_thumbnail(self.thumbnail_url)

    def run_discord_rpc(self):
        self.discord_rpc = None
        try:
            if self.discord_rpc_setting == 1:
                self.discord_rpc = RPC(app_id="1254202610781655050", output=False)
        except Exception as e:
            logging.error(f"Failed to activate Discord RPC: {str(e)}")

    def update_discord_rpc(self):
        if not self.discord_rpc:
            self.run_discord_rpc()

        if self.discord_rpc:
            details = self.title[:128]
            state = self.author[:128]
            large_image = self.thumbnail_url
            small_image = (
                "https://cdn.discordapp.com/app-icons/1254202610781655050/"
                "b4ede41d663f6caa7e45c6a042e447c9.png?size=32"
            )
            project_url = f"https://github.com/{self.app_author}/{self.name}"
            video_url = f"https://music.youtube.com/watch?v={self.video_id}"
            buttons = Button(
                button_one_label="Play in Browser",
                button_one_url=video_url,
                button_two_label="Get App on GitHub",
                button_two_url=project_url,
            )

            try:
                self.discord_rpc.set_activity(
                    details=details,
                    state=state,
                    large_image=large_image,
                    small_image=small_image,
                    act_type=2,
                    buttons=buttons,
                )
            except Exception as e:
                if "[Errno 22]" in str(e) or "[Errno 32]" in str(e):
                    self.reconnect_discord_rpc("update_discord_rpc")
                else:
                    logging.error(
                        f"An error occurred while updating Discord RPC: {str(e)}"
                    )
                    if self.discord_rpc.is_connected():
                        self.discord_rpc.disconnect()

    def clear_discord_rpc(self):
        if not self.discord_rpc:
            self.run_discord_rpc()

        if self.discord_rpc:
            try:
                self.discord_rpc.set_activity(
                    details="Nothing's playing yet", act_type=2
                )
            except Exception as e:
                if "[Errno 22]" in str(e) or "[Errno 32]" in str(e):
                    self.reconnect_discord_rpc("clear_discord_rpc")
                else:
                    logging.error(
                        f"An error occurred while clearing Discord RPC: {str(e)}"
                    )
                    if self.discord_rpc.is_connected():
                        self.discord_rpc.disconnect()

    def reconnect_discord_rpc(self, method_to_reconnect):
        if self.discord_rpc:
            self.run_discord_rpc()
            if method_to_reconnect == "update_discord_rpc":
                self.update_discord_rpc()
            elif method_to_reconnect == "clear_discord_rpc":
                self.clear_discord_rpc()

    def update_mini_player_track_progress(self):
        if self.mini_player_dialog:
            self.mini_player_dialog.BodyLabel.setText(self.current_time)
            self.mini_player_dialog.BodyLabel_2.setText(self.total_time)

    def update_tray_icon_track_controls(self):
        if self.tray_icon_setting == 1 and self.tray_icon:
            if self.video_state == "VideoPlaying":
                self.tray_icon.volume_down_action.setEnabled(True)
                self.tray_icon.previous_action.setEnabled(True)
                self.tray_icon.play_pause_action.setIcon(
                    QIcon(f"{self.icon_folder}/pause.png")
                )
                self.tray_icon.play_pause_action.setEnabled(True)
                self.tray_icon.next_action.setEnabled(True)
                self.tray_icon.volume_up_action.setEnabled(True)
            elif self.video_state == "VideoPaused":
                self.tray_icon.volume_down_action.setEnabled(True)
                self.tray_icon.previous_action.setEnabled(True)
                self.tray_icon.play_pause_action.setIcon(
                    QIcon(f"{self.icon_folder}/play.png")
                )
                self.tray_icon.play_pause_action.setEnabled(True)
                self.tray_icon.next_action.setEnabled(True)
                self.tray_icon.volume_up_action.setEnabled(True)
            else:
                self.tray_icon.volume_down_action.setEnabled(False)
                self.tray_icon.previous_action.setEnabled(False)
                self.tray_icon.play_pause_action.setIcon(
                    QIcon(f"{self.icon_folder}/play.png")
                )
                self.tray_icon.play_pause_action.setEnabled(False)
                self.tray_icon.next_action.setEnabled(False)
                self.tray_icon.volume_up_action.setEnabled(False)

    def update_win_thumbnail_buttons_track_controls(self):
        if self.win_thumbnail_toolbar:
            if self.video_state == "VideoPlaying":
                self.tool_btn_volume_down.setIcon(
                    QIcon(f"{self.icon_folder}/volume_down-filled-border.png")
                )
                self.tool_btn_previous.setIcon(
                    QIcon(f"{self.icon_folder}/previous-filled-border.png")
                )
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/pause-filled-border.png")
                )
                self.tool_btn_next.setIcon(
                    QIcon(f"{self.icon_folder}/next-filled-border.png")
                )
                self.tool_btn_volume_up.setIcon(
                    QIcon(f"{self.icon_folder}/volume_up-filled-border.png")
                )
                self.tool_btn_volume_down.setEnabled(True)
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
                self.tool_btn_volume_up.setEnabled(True)
            elif self.video_state == "VideoPaused":
                self.tool_btn_volume_down.setIcon(
                    QIcon(f"{self.icon_folder}/volume_down-filled-border.png")
                )
                self.tool_btn_previous.setIcon(
                    QIcon(f"{self.icon_folder}/previous-filled-border.png")
                )
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled-border.png")
                )
                self.tool_btn_next.setIcon(
                    QIcon(f"{self.icon_folder}/next-filled-border.png")
                )
                self.tool_btn_volume_up.setIcon(
                    QIcon(f"{self.icon_folder}/volume_up-filled-border.png")
                )
                self.tool_btn_volume_down.setEnabled(True)
                self.tool_btn_previous.setEnabled(True)
                self.tool_btn_play_pause.setEnabled(True)
                self.tool_btn_next.setEnabled(True)
                self.tool_btn_volume_up.setEnabled(True)
            else:
                self.tool_btn_volume_down.setIcon(
                    QIcon(f"{self.icon_folder}/volume_down-filled-border-disabled.png")
                )
                self.tool_btn_previous.setIcon(
                    QIcon(f"{self.icon_folder}/previous-filled-border-disabled.png")
                )
                self.tool_btn_play_pause.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled-border-disabled.png")
                )
                self.tool_btn_next.setIcon(
                    QIcon(f"{self.icon_folder}/next-filled-border-disabled.png")
                )
                self.tool_btn_volume_up.setIcon(
                    QIcon(f"{self.icon_folder}/volume_up-filled-border-disabled.png")
                )
                self.tool_btn_volume_down.setEnabled(False)
                self.tool_btn_previous.setEnabled(False)
                self.tool_btn_play_pause.setEnabled(False)
                self.tool_btn_next.setEnabled(False)
                self.tool_btn_volume_up.setEnabled(False)

    def update_mini_player_track_controls(self):
        if self.mini_player_dialog:
            if self.video_state == "VideoPlaying":
                self.mini_player_dialog.previous_button.setEnabled(True)
                self.mini_player_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/pause-filled.png")
                )
                self.mini_player_dialog.play_pause_button.setEnabled(True)
                self.mini_player_dialog.next_button.setEnabled(True)
                self.mini_player_dialog.volume_up_button.setEnabled(True)
                self.mini_player_dialog.volume_down_button.setEnabled(True)
            elif self.video_state == "VideoPaused":
                self.mini_player_dialog.volume_down_button.setEnabled(True)
                self.mini_player_dialog.previous_button.setEnabled(True)
                self.mini_player_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled.png")
                )
                self.mini_player_dialog.play_pause_button.setEnabled(True)
                self.mini_player_dialog.next_button.setEnabled(True)
                self.mini_player_dialog.volume_up_button.setEnabled(True)
                self.mini_player_dialog.volume_down_button.setEnabled(True)
            else:
                self.mini_player_dialog.previous_button.setEnabled(False)
                self.mini_player_dialog.play_pause_button.setIcon(
                    QIcon(f"{self.icon_folder}/play-filled.png")
                )
                self.mini_player_dialog.play_pause_button.setEnabled(False)
                self.mini_player_dialog.next_button.setEnabled(False)
                self.mini_player_dialog.volume_up_button.setEnabled(False)
                self.mini_player_dialog.volume_down_button.setEnabled(False)

    def create_volume_down_button(self):
        self.tool_btn_volume_down = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_volume_down.setToolTip("Volume Down")
        self.tool_btn_volume_down.setEnabled(False)
        self.tool_btn_volume_down.setIcon(
            QIcon(f"{self.icon_folder}/volume_down-filled-border-disabled.png")
        )
        self.tool_btn_volume_down.clicked.connect(self.volume_down)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_volume_down)

    def create_previous_button(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_previous.setToolTip("Previous")
        self.tool_btn_previous.setEnabled(False)
        self.tool_btn_previous.setIcon(
            QIcon(f"{self.icon_folder}/previous-filled-border-disabled.png")
        )
        self.tool_btn_previous.clicked.connect(self.skip_previous)
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
        self.tool_btn_next.clicked.connect(self.skip_next)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_next)

    def create_volume_up_button(self):
        self.tool_btn_volume_up = QWinThumbnailToolButton(self.win_thumbnail_toolbar)
        self.tool_btn_volume_up.setToolTip("Volume Up")
        self.tool_btn_volume_up.setEnabled(False)
        self.tool_btn_volume_up.setIcon(
            QIcon(f"{self.icon_folder}/volume_up-filled-border-disabled.png")
        )
        self.tool_btn_volume_up.clicked.connect(self.volume_up)
        self.win_thumbnail_toolbar.addButton(self.tool_btn_volume_up)

    def play_pause(self):
        self.run_js_script("play_pause.js")

    def skip_next(self):
        self.run_js_script("skip_next.js")

    def skip_previous(self):
        self.run_js_script("skip_previous.js")

    def volume_up(self):
        self.run_js_script("volume_up.js")

    def volume_down(self):
        self.run_js_script("volume_down.js")

    def run_js_script(self, script_name):
        self.webpage.runJavaScript(self.read_script(script_name))

    def read_script(self, filename):
        with open(f"{self.current_dir}/core/js/{filename}", "r", encoding="utf-8") as f:
            return f.read()

    def go_back(self):
        self.webview.back()

    def go_forward(self):
        self.webview.forward()

    def go_to_home(self):
        self.webview.load(QUrl("https://music.youtube.com/"))

    def reload_page(self):
        self.webview.reload()

    def stop(self):
        self.webview.stop()

    def select_download_folder(self):
        title = "Select Folder"
        folder = QFileDialog.getExistingDirectory(
            self, title, self.last_download_folder_setting
        )
        return folder if folder else None

    def start_download(self, use_cookies=False):
        download_folder = self.select_download_folder()
        if not download_folder:
            return

        self.last_download_folder_setting = download_folder
        self.settings_.setValue("last_download_folder", download_folder)

        self.is_downloading = True
        self.update_download_buttons_state(self.is_downloading)

        self.download_thread = DownloadThread(
            self.current_url, download_folder, self, use_cookies=use_cookies
        )
        self.download_thread.downloading_ffmpeg.connect(self.on_downloading_ffmpeg)
        self.download_thread.downloading_ffmpeg_success.connect(
            self.on_downloading_ffmpeg_success
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

    def show_download_error(self, msg, info_bar):
        info_bar.close()

        QTimer.singleShot(0, lambda: self.show_error_message(msg, "yt-dlp Error"))

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

    def open_download_folder(self, folder, info_bar):
        if info_bar:
            info_bar.close()

        url = QUrl.fromLocalFile(folder)
        QDesktopServices.openUrl(url)

    def on_download_finished(self):
        self.download_thread = None
        self.hide_downloading_state_tooltip()

        self.is_downloading = False
        self.update_download_buttons_state(self.is_downloading)

    def update_download_buttons_state(self, is_downloading):
        self.download_with_oauth_action.setEnabled(not is_downloading)
        self.download_as_unauthorized_action.setEnabled(not is_downloading)
        self.download_with_oauth_shortcut.setEnabled(not is_downloading)
        self.download_as_unauthorized_shortcut.setEnabled(not is_downloading)

    def open_mini_player(self):
        if self.video_state == "VideoPlaying" or "VideoPaused":
            self.show_mini_player()
            self.hide()
            self.hide_tray_icon()

    def show_mini_player(self):
        self.mini_player_dialog = MiniPlayerDialog(self)
        self.update_mini_player_track_controls()
        self.update_mini_player_track_info()
        self.update_mini_player_track_progress()
        self.mini_player_dialog.show()

    def show_tray_icon(self):
        if self.tray_icon:
            self.tray_icon.show()

    def hide_tray_icon(self):
        if self.tray_icon:
            self.tray_icon.hide()

    def load_url(self, url):
        self.webview.load(QUrl(url))

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def send_bug_report(self):
        webbrowser.open_new_tab(
            f"https://github.com/{self.app_author}/{self.name}/issues"
        )

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

    def show_window(self):
        if self.isMinimized() or self.isHidden():
            if self.isMinimized():
                self.showNormal()
            else:
                self.show()
        self.activateWindow()

    def show_window_or_mini_player(self):
        if self.mini_player_dialog is None:
            self.show_window()
        else:
            if self.mini_player_dialog.isMinimized():
                self.mini_player_dialog.showNormal()

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

        if self.tray_icon_setting == 1 and self.tray_icon is not None:
            if not self.force_exit:
                self.hide()
                event.ignore()
                return

        if self.video_state == "VideoPlaying":
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
