import requests
import pywinstyles

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi

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
        pywinstyles.apply_style(self, "dark")

        self._init_window()
        self._init_attributes()
        self._init_content()
        self._init_connect()

        self.show()

    def _init_content(self):
        self.change_info()
        self.update_play_pause_icon()

        self.TransparentToolButton.setIcon(            
            QIcon(f"{self.window.icon_path}/previous-filled.svg"))
        self.TransparentToolButton_3.setIcon(
            QIcon(f"{self.window.icon_path}/next-filled.svg"))

    def _init_connect(self):
        self.TransparentToolButton_2.clicked.connect(self.play_pause_track)
        self.TransparentToolButton.clicked.connect(self.window.previous_track)
        self.TransparentToolButton_3.clicked.connect(self.window.next_track)
        self.window.webview.titleChanged.connect(self.title_changed)

    def _init_attributes(self):
        pass

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
                QIcon(f"{self.window.icon_path}/play-filled.svg"))
        else:
            self.TransparentToolButton_2.setIcon(
                QIcon(f"{self.window.icon_path}/pause-filled.svg"))

    def move_to(self):
        selected_index = self.settings.value("selected_location_index", 1)

        available_geometry = QApplication.desktop().availableGeometry()

        offset = 30
        if selected_index == 0:
            x = int(available_geometry.left() + offset)
            y = int(available_geometry.top() + offset)
        elif selected_index == 1:
            x = int(available_geometry.right() - self.width() - offset)
            y = int(available_geometry.top() + offset)
        elif selected_index == 2:
            x = int(available_geometry.left() + offset)
            y = int(available_geometry.center().y() - self.height() / 2)
        elif selected_index == 3:
            x = int(available_geometry.right() - self.width() - offset)
            y = int(available_geometry.center().y() - self.height() / 2)
        elif selected_index == 4:
            x = int(available_geometry.center().x() - self.width() / 2)
            y = int(available_geometry.top() + offset)
        elif selected_index == 5:
            x = int(available_geometry.center().x() - self.width() / 2)
            y = int(available_geometry.bottom() - self.height() - offset)
        elif selected_index == 6:
            x = int(available_geometry.center().x() - self.width() / 2)
            y = int(available_geometry.center().y() - self.height() / 2)
        elif selected_index == 7:
            x = int(available_geometry.left() + offset)
            y = int(available_geometry.bottom() - self.height() - offset)
        elif selected_index == 8:
            x = int(available_geometry.right() - self.width() - offset)
            y = int(available_geometry.bottom() - self.height() - offset)
        else:
            x = int(available_geometry.right() - self.width() - offset)
            y = int(available_geometry.top() + offset)

        self.move(x, y)
    
    def display_image(self):
        try:
            response = requests.get(self.window.current_image_url)
            if response.status_code == 200:
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(response.content)
                self.pixmap = self.pixmap.scaled(60, 60, Qt.KeepAspectRatio)
                self.label.setPixmap(self.pixmap)

                self.window.previous_image_url = self.window.current_image_url
        except Exception as e:
            print(f"Error displaying image in mini-player: {e}")

    def change_info(self):
        self.StrongBodyLabel.setText(self.window.track_title)
        self.StrongBodyLabel.setToolTip(self.window.track_title)
        self.BodyLabel_2.setText(self.window.track_author)
        self.BodyLabel_2.setToolTip(self.window.track_author)
        self.display_image()
        
    def title_changed(self, title):
        self.change_info()
        self.update_play_pause_icon()

    def _init_window(self):
        self.window.hide()
        self.window.tray_icon.hide()

        self.setWindowTitle("Mini-Player")
        self.setWindowFlags(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setFixedSize(360, 150)
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico"))
        self.move_to()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.window.show()
        if self.settings.value("hide_window_in_tray", "false") == "true":
            self.window.tray_icon.show()
        self.deleteLater()