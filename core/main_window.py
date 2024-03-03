from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QShortcut
)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtWinExtras import (
    QWinThumbnailToolBar, QWinThumbnailToolButton  
)
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5 import uic

from qfluentwidgets import (
    InfoBar, InfoBarPosition, IndeterminateProgressRing,
    setTheme, setThemeColor, Theme, SplashScreen, 
    PushButton, ToolTipFilter, ToolTipPosition
)

import os
import sys
import requests
import webbrowser
from threading import Thread

from core.web_engine_page import WebEnginePage
from core.web_engine_view import WebEngineView
from core.download_manager import DownloadManager
from core.options_dialog import OptionsDlg
from core.about_dialog import AboutDlg
from core.mini_player_dialog import MiniPlayerDlg
from core.tray_icon import TrayIcon

class Window(QMainWindow):
    def __init__(
        self,
        name,
        version,
        current_dir,
        settings,
        parent=None
    ):
        super().__init__(parent)

        self.name = name
        self.version = version
        self.current_dir = current_dir
        self.settings = settings

        self.win_toolbar = QWinThumbnailToolBar(self)
        self.create_win_toolbar_buttons()

        uic.loadUi(
            f"{self.current_dir}/core/ui/main_window.ui", self
        ) 

        setTheme(Theme.DARK)
        setThemeColor("red")
        
        self._init_attributes()
        self._init_window()
        self._init_content()
        self._init_connect()
        
    def _init_attributes(self):
        pass

    def _init_connect(self):
        self.webview.titleChanged.connect(self.update_window_title)
        self.webview.urlChanged.connect(self.update_url)
        self.webview.loadProgress.connect(self.on_load_progress)
        self.label.mousePressEvent = self.open_in_browser
        self.tool_btn_previous.clicked.connect(self.previous_track)
        self.tool_btn_next.clicked.connect(self.next_track)
        self.tool_btn_play_pause.clicked.connect(self.play_pause_track)

    def _init_shortcuts(self):
        shortcuts = {
            Qt.Key_Left: self.go_back,
            Qt.Key_Right: self.go_forward,
            Qt.CTRL + Qt.Key_H: self.go_home,
            Qt.CTRL + Qt.Key_R: self.go_reload,
            Qt.CTRL + Qt.Key_D: lambda: self.window().go_download('track'),
            Qt.CTRL + Qt.Key_P: lambda: self.window().go_download('playlist'),
            Qt.CTRL + Qt.Key_M: self.open_mini_player,
            Qt.CTRL + Qt.Key_S: self.open_settings_dialog,
        }
        for key, value in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(value)

    def _init_content(self):
        self._init_webview()
        self._init_splash_screen()  

    def _init_webview(self):
        self.webview = WebEngineView()

        self.webpage = WebEnginePage(self.webview)
        self.webpage.setParent(self)
        self.webview.setPage(self.webpage)
        self.webpage.fullScreenRequested.connect(
            self.handleFullscreen
        )

        self.websettings = QWebEngineSettings.globalSettings()
        self.websettings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, 
            self.settings.value(
                "support_full_screen_mode", "true").lower() == "true"
        )
        self.websettings.setAttribute(
            QWebEngineSettings.ScrollAnimatorEnabled, 
            self.settings.value(
                "support_for_animated_scrolling", "true").lower() == "true"
        )

        if self.settings.value("open_last_url_at_startup", "false") == "true":
            self.webview.load(QUrl(self.settings.value("last_url")))
        else:
            self.webview.load(QUrl("https://music.youtube.com"))
        
        self.horizontalLayout.addWidget(self.webview)

        self._init_tray_icon()
        self._init_shortcuts()

    def _init_tray_icon(self):
        self.tray_icon = TrayIcon(            
            self.current_dir,
            self.name,
            self.settings, 
            parent=self
        )
        self.tray_icon.hide()

    def _init_splash_screen(self):
        self.splash_screen_is_over = False
        
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()

    def go_back(self):
        self.webview.back()

    def go_forward(self):
        self.webview.forward()

    def go_home(self):
        self.webview.load(QUrl("https://music.youtube.com"))

    def go_reload(self):
        self.webview.reload()

    def go_download(self, download_type):
        if download_type == "track":
            if not "watch" in self.webview.url().toString():
                return
        elif download_type == "playlist":
            if not "playlist" in self.webview.url().toString():
                return

        last_download_path = self.settings.value(
            "last_download_path", 
            self.current_dir
        )
        download_path = QFileDialog.getExistingDirectory(
            self, 
            "Select Directory", 
            last_download_path, 
            QFileDialog.ShowDirsOnly
        )
        
        if download_path:
            self.settings.setValue(
                "last_download_path", 
                download_path
            )
            url = self.webview.url().toString()

            self.download_manager = DownloadManager(self.current_dir, self.settings)
            self.download_manager.downloadFinished.connect(
                self.on_download_finished
            )
            self.download_manager.downloadError.connect(
                self.on_download_error
            )

            Thread(
                target=self.download_manager.download_external_process, 
                args=(url, download_path, download_type)
            ).start()

            self.add_download_progress()

    def add_download_progress(self):
        self.download_info_bar = InfoBar.new(
            icon=QIcon(f"{self.current_dir}/resources/icons/file_download_white_24dp.svg"),
            title="",
            content=f"Downloading...",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )

        spinner = IndeterminateProgressRing(self)
        spinner.setMaximumSize(20, 20)
        spinner.setMinimumSize(20, 20)
        self.download_info_bar.addWidget(spinner)   

    def on_download_finished(self, download_path):
        if self.isHidden():
            self.show()
            self.download_info_bar.close()
            self.hide()
        else:
            self.download_info_bar.close()

        InfoBar.info(
            title="",
            content=f"Successfully downloaded!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )

    def on_download_error(self, error_message):
        if self.isHidden():
            self.show()
            self.download_info_bar.close()
            self.hide()
        else:
            self.download_info_bar.close()

        InfoBar.error(
            title="",
            content=f"Download error:(",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )

        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            if isinstance(error_message, str):
                error_message = error_message.encode('utf-8')
            f.write(error_message)
            f.flush()
            os.startfile(f.name)

    def open_mini_player(self):
        if not "watch" in self.webview.url().toString():
            return
        Dlg = MiniPlayerDlg(
            self.current_dir,
            self.name,
            self.settings, 
            parent=self
        )

    def handleFullscreen(self, request):
        if(request.toggleOn()):
            request.accept()
            self.showFullScreen()
            self.frame_2.hide()
        else:
            request.accept()
            self.showNormal()
            self.frame_2.show()

    def open_in_browser(self, event):
        if event.button() == Qt.LeftButton:
            webbrowser.open_new_tab(
                self.webview.url().toString()
            )

    def on_load_progress(self, progress):
        if progress == 100:
            if not self.splash_screen_is_over:
                if self.isHidden():
                    self.show()
                    self.splashScreen.finish()
                    self.hide()
                else:
                    self.splashScreen.finish()

                if self.settings.value("check_for_updates_at_startup", "true") == "true":
                    self.check_for_updates(startup=True)
            self.splash_screen_is_over = True

            self.ProgressBar.hide()
            self.ProgressBar.setValue(0)

            with open(f"{self.current_dir}/core/js/add_styles.js", "r") as js_file:
                self.webview.page().runJavaScript(js_file.read())

            self.update_play_pause_icon() 
        else:
            self.ProgressBar.setValue(progress)
            if self.ProgressBar.isHidden():
                self.ProgressBar.show()

    def open_settings_dialog(self):
        Dlg = OptionsDlg(
            self.current_dir,
            self.name,
            self.settings, 
            parent=self
            )
        Dlg.exec_()

    def open_about_dialog(self):
        Dlg = AboutDlg(
            self.current_dir,
            self.name,
            self.settings, 
            self.version,
            parent=self
            )
        Dlg.exec_()

    def create_win_toolbar_buttons(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_previous.setToolTip('Previous')
        self.tool_btn_previous.setEnabled(False)
        self.tool_btn_previous.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_previous_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_previous)

        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_play_pause.setToolTip('Play/Pause')
        self.tool_btn_play_pause.setEnabled(False)
        self.tool_btn_play_pause.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
        ))                     
        self.win_toolbar.addButton(self.tool_btn_play_pause)

        self.tool_btn_next = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_next.setToolTip('Next')
        self.tool_btn_next.setEnabled(False)
        self.tool_btn_next.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_next_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_next)

    def previous_track(self):
        with open(f"{self.current_dir}/core/js/previous_track.js", "r") as js_file:
            self.webview.page().runJavaScript(js_file.read())  

    def next_track(self):
        with open(f"{self.current_dir}/core/js/next_track.js", "r") as js_file:
            self.webview.page().runJavaScript(js_file.read())  

    def play_pause_track(self):
        with open(f"{self.current_dir}/core/js/play_pause_track.js", "r") as js_file:
            self.webview.page().runJavaScript(js_file.read())
        self.update_play_pause_icon()

    def update_play_pause_icon(self):
        with open(f"{self.current_dir}/core/js/get_play_pause_state.js", "r") as js_file:
            self.webview.page().runJavaScript(js_file.read(), self.set_play_pause_icon) 
  
    def set_play_pause_icon(self, is_paused):
        if is_paused: 
            if "watch" in self.webview.url().toString():           
                self.tool_btn_play_pause.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/win_toolbar_icons/play_arrow_white_24dp.svg"
                ))                   
                self.tray_icon.play_pause_action.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/play_arrow_white_24dp.svg"
                ))  
            else:
                self.tool_btn_play_pause.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/disabled_win_toolbar_icons/play_arrow_white_24dp.svg"
                ))  
                self.tray_icon.play_pause_action.setEnabled(False)
        else:
            if "watch" in self.webview.url().toString():            
                self.tool_btn_play_pause.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
                ))             
                self.tray_icon.play_pause_action.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/pause_white_24dp.svg"
                ))    
            else:
                self.tool_btn_play_pause.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/disabled_win_toolbar_icons/pause_white_24dp.svg"
                ))  
                self.tray_icon.play_pause_action.setEnabled(False)

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )    
        if self.settings.value("save_last_window_size", "true") == "true":
            size = self.settings.value("last_window_size", QSize(800,600))
        else:
            size = QSize(800,600)
        self.resize(size)

        self._move_window_to_center()
        self.raise_()
        self.activateWindow()

    def update_window_title(self, title):
        self.setWindowTitle(title) 
        self.tray_icon.setToolTip(title)
        self.tray_icon.installEventFilter(
            ToolTipFilter(
                self.tray_icon, 0, 
                ToolTipPosition.TOP
        ))
        self.update_play_pause_icon()

    def update_url(self, url):
        self.label.setText(url.toString())
        self.label.setMaximumWidth(self.width() * 0.8)
        self.label.setToolTip(self.label.text())
        self.label.installEventFilter(
            ToolTipFilter(
                self.label, 0, 
                ToolTipPosition.TOP
        ))
        
        self.settings.setValue("last_url", url.toString())
        
        if "watch" in url.toString():
            self.tool_btn_previous.setEnabled(True)
            self.tool_btn_previous.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_previous_white_24dp.svg"
            ))     
            self.tray_icon.previous_track_action.setEnabled(True)       

            self.tool_btn_play_pause.setEnabled(True)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
            ))
            self.tray_icon.play_pause_action.setEnabled(True)  

            self.tool_btn_next.setEnabled(True) 
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_next_white_24dp.svg"
            ))   
            self.tray_icon.next_track_action.setEnabled(True)  
        else:
            self.tool_btn_previous.setEnabled(False)
            self.tool_btn_previous.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_win_toolbar_icons/skip_previous_white_24dp.svg"
            ))
            self.tray_icon.previous_track_action.setEnabled(False)  

            self.tool_btn_play_pause.setEnabled(False)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_win_toolbar_icons/pause_white_24dp.svg"
            ))   
            self.tray_icon.play_pause_action.setEnabled(False)  

            self.tool_btn_next.setEnabled(False)
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_win_toolbar_icons/skip_next_white_24dp.svg"
            ))
            self.tray_icon.next_track_action.setEnabled(False) 
            
    def check_for_updates(self, startup=None):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/Youtube-Music-Desktop-Player/releases/latest"
            )
        except Exception as e:
            print(e)
        try:
            item_version = response.json()["name"]
            item_download = response.json().get("html_url")         

            if item_version != self.version:
                update_msg_box = InfoBar.new(
                    icon=f"{self.current_dir}/resources/icons/upgrade_white_24dp.svg",
                    title=f"New update {item_version} is available!",
                    content="",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM,
                    duration=-1,
                    parent=self
                )
                download_btn = PushButton("Download")
                download_btn.clicked.connect(
                    lambda: [
                        webbrowser.open_new_tab(item_download),
                        sys.exit(),
                    ]
                )
                update_msg_box.addWidget(download_btn)  
            else:
                if not startup:
                    InfoBar.info(
                        title="No new updates found",
                        content="Wait for it...",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=-1,
                        parent=self
                    )
        except Exception as e:
            InfoBar.error(
                title="Update search error:",
                content=f"{e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )

    def _move_window_to_center(self):    
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.win_toolbar.window():
            self.win_toolbar.setWindow(self.windowHandle())

    def resizeEvent(self, event):
        self.settings.setValue("last_window_size", event.size())
        self.label.setMaximumWidth(self.width() * 0.8)

    def close_in_tray(self):
        sys.exit(0)

    def closeEvent(self, event):
        if self.settings.value("hide_window_in_tray", "true") == "true":
            self.hide()
            self.tray_icon.show()
            event.ignore()
        else:
            event.accept()