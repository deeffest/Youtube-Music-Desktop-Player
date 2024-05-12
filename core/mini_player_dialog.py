from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi

import requests
import pytube

class MiniPlayerDlg(QDialog):
    def __init__(
        self,
        current_dir,
        name,
        settings,
        parent=None
    ):
        super().__init__(parent)

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings

        loadUi(
            f'{self.current_dir}/core/ui/mini_player_dialog.ui', self
        )

        self._init_window()
        self._init_attributes()
        self._init_content()
        self._init_connect()

        self.show()

    def _init_content(self):
        self.change_info(self.window.webview.url())
        self.update_play_pause_icon()

        self.TransparentToolButton.setIcon(            
            QIcon(f"{self.current_dir}/resources/icons/skip_previous_white_24dp.svg"))
        self.TransparentToolButton_3.setIcon(
            QIcon(f"{self.current_dir}/resources/icons/skip_next_white_24dp.svg"))

    def _init_connect(self):
        self.TransparentToolButton_2.clicked.connect(self.play_pause_track)
        self.TransparentToolButton.clicked.connect(self.window.previous_track)
        self.TransparentToolButton_3.clicked.connect(self.window.next_track)
        self.window.webview.titleChanged.connect(self.title_changed)

    def _init_attributes(self):
        self.previous_url = self.window.webview.url()

    def play_pause_track(self):
        with open(f"{self.current_dir}/core/js/play_pause_track.js", "r") as js_file:
            self.window.webview.page().runJavaScript(js_file.read())
        self.update_play_pause_icon()

    def update_play_pause_icon(self):
        with open(f"{self.current_dir}/core/js/get_play_pause_state.js", "r") as js_file:
            self.window.webview.page().runJavaScript(js_file.read(), self.set_play_pause_icon) 

    def set_play_pause_icon(self, is_paused):
        if is_paused:            
            self.TransparentToolButton_2.setIcon(
                QIcon(f"{self.current_dir}/resources/icons/play_arrow_white_24dp.svg"))
        else:
            self.TransparentToolButton_2.setIcon(
                QIcon(f"{self.current_dir}/resources/icons/pause_white_24dp.svg"))
    
    def set_track_image(self):
        with open(f"{self.current_dir}/core/js/get_track_image.js", "r") as js_file:
            self.window.webview.page().runJavaScript(js_file.read(), self.displayImage)

    def displayImage(self, url: str) -> None:
        if url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    self.pixmap = QPixmap()
                    self.pixmap.loadFromData(response.content)
                    self.pixmap = self.pixmap.scaled(60, 60, Qt.KeepAspectRatio) 
                    self.label.setPixmap(self.pixmap) 
            except Exception as e:
                print(e)

    def _init_window(self):
        self.window.hide()
        self.window.tray_icon.hide()

        self.setWindowTitle("Mini-Player")
        self.setWindowFlags(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setFixedSize(360, 150)
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico"))
        self.move_to_top_right_corner()

    def move_to_top_right_corner(self):
        available_geometry = QApplication.desktop().availableGeometry()

        x = available_geometry.right() - self.width() - 30
        y = available_geometry.top() + 30
        self.move(x, y)

    def update_info(self, url):
        try:
            yt = pytube.YouTube(QUrl(url).toString())
            self.StrongBodyLabel.setText(yt.title)
            self.StrongBodyLabel.setToolTip(yt.title)
            self.BodyLabel_2.setText(yt.author)
            self.BodyLabel_2.setToolTip(yt.author)
        except Exception as e:
            print(e)

    def change_info(self, url):
        self.set_track_image()
        self.update_info(url)

    def title_changed(self, title):
        if self.window.webview.url() != self.previous_url:
            self.change_info(self.window.webview.url())
            self.previous_url = self.window.webview.url()
        
        self.update_play_pause_icon()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.window.show()
        if self.settings.value("hide_window_in_tray", "true") == "true":
            self.window.tray_icon.show()
        self.deleteLater()