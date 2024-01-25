#main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QShortcut
)
from PyQt5.QtGui import (
    QIcon, QKeySequence
)
from PyQt5.QtCore import (
    QSize, Qt, QUrl, QThread, pyqtSlot, pyqtSignal
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEnginePage, QWebEngineSettings
)
from PyQt5 import uic

from qfluentwidgets import (
    InfoBar, InfoBarPosition, RoundMenu, Action, 
    MenuAnimationType, IndeterminateProgressRing,
    setTheme, setThemeColor, Theme
)
from core.custom_fluentwidgets.window.splash_screen import SplashScreen

import os
import sys
import requests
import webbrowser
from pytube import YouTube

from core.options_dialog import OptionsDlg
from core.about_dialog import AboutDlg
from core.mini_player_dialog import MiniPlayerDlg
from core.tray_icon import TrayIcon
from core.alert_dialog import AlertDlg
from core.confirm_dialog import ConfirmDlg
from core.input_dialog import InputDlg

class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if "music.youtube.com" not in url.toString() and "google.com" not in url.toString():
            webbrowser.open_new_tab(url.toString())
            return False

        return QWebEnginePage.acceptNavigationRequest(self, url, _type, isMainFrame)

    def javaScriptAlert(self, qurl, text):
        dialog = AlertDlg(
            self.parent().name, 
            self.parent().current_dir, 
            self.view()
        ) 
        dialog.setText(text)
        reply = dialog.exec_()

    def javaScriptConfirm(self, qurl, text):
        dialog = ConfirmDlg(            
            self.parent().name, 
            self.parent().current_dir, 
            self.view()
        ) 
        dialog.setText(text)
        reply = dialog.exec_()
        return reply == True

    def javaScriptPrompt(self, qurl, text, text_value):
        dialog = InputDlg(            
            self.parent().name, 
            self.parent().current_dir, 
            self.view()
        ) 
        dialog.setText(text)
        dialog.setTextValue(text_value)
        if dialog.exec_():
            return (True, dialog.textValue())
        else:
            return (False, "")

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

        go_download_action = Action("Download", shortcut="Ctrl+D")
        go_download_action.setIcon(
            QIcon(f"{self.window().current_dir}/resources/icons/file_download_white_24dp.svg")
        )
        go_download_action.triggered.connect(
            self.window().go_download
        )
        menu.addAction(go_download_action)

        open_mini_player_action = Action("Mini-Player (beta)", shortcut="Ctrl+M")
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
            go_download_action.setEnabled(False)
            open_mini_player_action.setEnabled(False)

        menu.exec(event.globalPos(), aniType=MenuAnimationType.DROP_DOWN)

class DownloadThread(QThread):
    downloadFinished = pyqtSignal(str)
    downloadError = pyqtSignal(str)

    def __init__(self, url, current_dir, yt, download_path):
        super().__init__()
        self.url = url
        self.current_dir = current_dir
        self.yt = yt
        self.download_path = download_path
    
    def run(self):
        try:
            stream = self.yt.streams.get_highest_resolution()
            start_download = stream.download(
                output_path=self.download_path
            )

            self.downloadFinished.emit(str(self.download_path)) 
        except Exception as e:
            self.downloadError.emit(str(e))

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
        self.CaptionLabel.mousePressEvent = self.open_in_browser

    def _init_shortcuts(self):
        shortcuts = {
            Qt.Key_Left: self.go_back,
            Qt.Key_Right: self.go_forward,
            Qt.CTRL + Qt.Key_H: self.go_home,
            Qt.CTRL + Qt.Key_R: self.go_reload,
            Qt.CTRL + Qt.Key_D: self.go_download,
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

    def go_download(self):
        if not "watch" in self.webview.url().toString():
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
            try:
                self.yt = YouTube(url)
            except Exception as e:
                self.on_download_error(e)
                return

            download_thread = DownloadThread(
                url, 
                self.current_dir, 
                self.yt, 
                download_path
            )
            download_thread.downloadFinished.connect(self.on_download_finished)
            download_thread.downloadError.connect(self.on_download_error)
            download_thread.start()

            self.donwload_info_bar = InfoBar.new(
                icon=QIcon(f"{self.current_dir}/resources/icons/file_download_white_24dp.svg"),
                title=self.yt.title,
                content=f"downloading...",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )

            spinner = IndeterminateProgressRing(self)
            spinner.setMaximumSize(20, 20)
            spinner.setMinimumSize(20, 20)
            self.donwload_info_bar.addWidget(spinner)   

    @pyqtSlot(str)
    def on_download_finished(self, download_path):
        try:
            self.donwload_info_bar.close()
        except:
            pass
        InfoBar.info(
            title=self.yt.title,
            content=f"successfully downloaded!",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self
        )

    @pyqtSlot(str)
    def on_download_error(self, error_message):
        try:
            self.donwload_info_bar.close()
        except:
            pass
        InfoBar.error(
            title="Error:",
            content=f"{error_message}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )

    def open_mini_player(self):
        if not "watch" in self.webview.url().toString():
            return
        Dlg = MiniPlayerDlg(
            self.current_dir,
            self.name,
            self.settings, 
            parent=self
            )
        Dlg.exec_()

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
                self.splashScreen.finish()
                if self.settings.value("check_for_updates_at_startup", "true") == "true":
                    self.check_for_updates(startup=True)
            self.splash_screen_is_over = True

            self.ProgressBar.hide()
            self.ProgressBar.setValue(0)

            with open(f"{self.current_dir}/core/js/add_styles.js", "r") as js_file:
                self.webview.page().runJavaScript(js_file.read())
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

    def update_url(self, url):
        self.CaptionLabel.setText(url.toString())
        self.CaptionLabel.setMaximumWidth(self.width() * 0.8)
        self.CaptionLabel.setToolTip(self.CaptionLabel.text())

        self.settings.setValue("last_url", url.toString())
        
    def check_for_updates(self, startup=None):
        response = requests.get(
            "https://api.github.com/repos/deeffest/Youtube-Music-Desktop-Player/releases/latest"
        )
        try:
            item_version = response.json()["name"]
            item_download = response.json().get("html_url")         

            if item_version != self.version:
                update_msg_box = InfoBar.new(
                    icon=FIF.UPDATE,
                    title=f"New update {item_version} is available!",
                    content="",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=-1,
                    parent=self
                )
                download_btn = PushButton("Download")
                download_btn.clicked.connect(
                    lambda: webbrowser.open_new_tab(item_download)
                )
                update_msg_box.addWidget(download_btn)     
            else:
                if not startup:
                    InfoBar.info(
                        title="No new updates found",
                        content="Wait for it...",
                        orient=Qt.Horizontal,
                        isClosable=False,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=2000,
                        parent=self
                    )
        except Exception as e:
            InfoBar.error(
                title="Update search error:",
                content=f"{e}",
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=2000,
                parent=self
            )

    def _move_window_to_center(self):    
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def resizeEvent(self, event):
        self.settings.setValue("last_window_size", event.size())
        self.CaptionLabel.setMaximumWidth(self.width() * 0.8)