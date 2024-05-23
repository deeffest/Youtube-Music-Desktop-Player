from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QFileDialog, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QSize, Qt, QUrl, QTimer
from PyQt5.QtWinExtras import QWinThumbnailToolBar, \
    QWinThumbnailToolButton
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5 import uic

from qfluentwidgets import InfoBar, InfoBarPosition, \
    setTheme, setThemeColor, Theme, SplashScreen, \
    PushButton, MessageBox

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
        self.timer_active = False

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
        self.label_3.hide()

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

    def _init_splash_screen(self):
        self.splash_screen_is_over = False
        
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.titleBar.hide()
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
        if hasattr(self, "dots_timer"):
            w = MessageBox(f"The current download request is denied.", 
                "Wait for the app to finish the current track/playlist download.", self)
            w.cancelButton.hide()
            w.exec_()
            return
        
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

            self.add_download_progress(download_type)

    def add_download_progress(self, download_type):
        self.label_2.setText(f"Downloading {download_type}...")
        self.label_3.show()
        self.dots_count = 0
        self.dots_timer = QTimer(self)
        self.dots_timer.timeout.connect(lambda: self.update_dots(download_type))
        self.dots_timer.start(500)

    def update_dots(self, download_type):
        self.dots_count = (self.dots_count + 1) % 4
        dots = "." * self.dots_count
        self.label_2.setText(f"Downloading {download_type}" + dots)

    def stop_download_progress(self):
        if hasattr(self, 'dots_timer'):
            self.dots_timer.stop()
            del self.dots_timer
            self.label_2.setText("")
            self.label_3.hide()

    def on_download_finished(self, download_path):
        self.stop_download_progress()

        path_msg_box = InfoBar.info(
            title="",
            content=f"Successfully downloaded!",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self
        )
        open_path_btn = PushButton("Download Path")
        open_path_btn.clicked.connect(lambda: self.open_download_path(download_path, path_msg_box))
        path_msg_box.addWidget(open_path_btn)

    def open_download_path(self, download_path, path_msg_box):
        os.startfile(download_path)
        path_msg_box.close()

    def on_download_error(self, error_message):
        self.stop_download_progress()

        error_msg_box = InfoBar.error(
            title="",
            content=f"Download error:(",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,
            parent=self
        )
        open_error_btn = PushButton("Error Message")
        open_error_btn.clicked.connect(lambda: self.open_temp_error(error_message, error_msg_box))
        error_msg_box.addWidget(open_error_btn)

    def open_temp_error(self, error_message, error_msg_box):
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode='w') as f:
            if isinstance(error_message, bytes):
                error_message = error_message.decode('utf-8')
            f.write(error_message)
            f.flush()
            os.startfile(f.name)

        error_msg_box.close()

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
                    self.check_for_updates()
            self.splash_screen_is_over = True

            with open(f"{self.current_dir}/core/js/add_styles.js", "r") as js_file:
                self.webview.page().runJavaScript(js_file.read())

            self.update_play_pause_icon() 

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
                    f"{self.current_dir}/resources/icons/win_toolbar_icons/play_arrow_white_24dp.svg"
                ))
            else:
                self.tool_btn_play_pause.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/disabled_icons/play_arrow_white_24dp.svg"
                ))  
                self.tray_icon.play_pause_action.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/disabled_icons/play_arrow_white_24dp.svg"
                ))
        else:
            if "watch" in self.webview.url().toString():            
                self.tool_btn_play_pause.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
                ))             
                self.tray_icon.play_pause_action.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
                ))    
            else:
                self.tool_btn_play_pause.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg"
                ))  
                self.tray_icon.play_pause_action.setIcon(QIcon(
                    f"{self.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg"
                ))

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
        self.update_play_pause_icon()

    def update_url(self, url):
        self.label.setText(url.toString())
        self.label.setMaximumWidth(int(self.width() * 0.8))
        self.label.setToolTip(f"{self.label.text()}<br><br>Click to open the current URL in the browser.")
        
        self.settings.setValue("last_url", url.toString())
        
        if "watch" in url.toString():
            self.tool_btn_previous.setEnabled(True)
            self.tool_btn_previous.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_previous_white_24dp.svg"
            ))     
            self.tray_icon.previous_track_action.setEnabled(True)
            self.tray_icon.previous_track_action.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_previous_white_24dp.svg"
            ))     

            self.tool_btn_play_pause.setEnabled(True)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
            ))
            self.tray_icon.play_pause_action.setEnabled(True)
            self.tray_icon.play_pause_action.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
            )) 

            self.tool_btn_next.setEnabled(True) 
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_next_white_24dp.svg"
            ))   
            self.tray_icon.next_track_action.setEnabled(True)
            self.tray_icon.next_track_action.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_next_white_24dp.svg"
            ))   
        else:
            self.tool_btn_previous.setEnabled(False)
            self.tool_btn_previous.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/skip_previous_white_24dp.svg"
            ))
            self.tray_icon.previous_track_action.setEnabled(False)
            self.tray_icon.previous_track_action.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/skip_previous_white_24dp.svg"
            ))

            self.tool_btn_play_pause.setEnabled(False)
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg"
            ))   
            self.tray_icon.play_pause_action.setEnabled(False)
            self.tray_icon.play_pause_action.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/pause_white_24dp.svg"
            )) 

            self.tool_btn_next.setEnabled(False)
            self.tool_btn_next.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/skip_next_white_24dp.svg"
            ))
            self.tray_icon.next_track_action.setEnabled(False)
            self.tray_icon.next_track_action.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/disabled_icons/skip_next_white_24dp.svg"
            ))
            
    def check_for_updates(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/Youtube-Music-Desktop-Player/releases/latest")
            item_version = response.json()["name"]
            item_download = response.json().get("html_url")         

            if item_version != self.version:
                update_msg_box = InfoBar.new(
                    icon=f"{self.current_dir}/resources/icons/upgrade_white_24dp.svg",
                    title="",
                    content=f"New update {item_version} is available!",
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

        except Exception as e:
            InfoBar.error(
                title="Update search error:",
                content=f"{e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=-1,
                parent=self
            )

    def open_changelog(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/deeffest/Youtube-Music-Desktop-Player/releases/latest")
            data = response.json()
            item_notes = data.get("body")
            w = MessageBox(f"Change log of the latest version", item_notes, self)
            w.cancelButton.hide()
            w.exec_()

        except Exception as e:
            InfoBar.error(
                title="Error in opening the change log:",
                content=f"{e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
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
        self.label.setMaximumWidth(int(self.width() * 0.8))

    def exit_app(self):
        sys.exit(0)

    def closeEvent(self, event):
        if self.settings.value("hide_window_in_tray", "true") == "true":
            self.hide()
            self.tray_icon.show()
            event.ignore()
        else:
            if "watch" in self.webview.url().toString():
                w = MessageBox(f"Confirmation of exit", 
                    "Do you really want to quit the app? The current playback will stop.", self)
                if w.exec_():
                    self.exit_app()
                else:
                    event.ignore()
            else:
                self.exit_app()