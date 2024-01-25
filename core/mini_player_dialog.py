from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import (
    QPixmap, QIcon, QPainter, QPen, QColor
)
from PyQt5.uic import loadUi

import requests

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
        self._init_content()
        self._init_connect()

    def _init_content(self):
        self.update_play_pause_icon()
        self.set_track_image()
        self.update_window_title(self.window.windowTitle())

        self.TransparentToolButton_2.setIcon(
            QIcon(f"{self.current_dir}/resources/icons/close_white_24dp.svg")
        )
        self.TransparentToolButton_6.setIcon(            
            QIcon(f"{self.current_dir}/resources/icons/replay_5_white_24dp.svg")
        )
        self.TransparentToolButton_5.setIcon(            
            QIcon(f"{self.current_dir}/resources/icons/skip_previous_white_24dp.svg")
        )
        self.TransparentToolButton_3.setIcon(
            QIcon(f"{self.current_dir}/resources/icons/skip_next_white_24dp.svg")
        )
        self.TransparentToolButton_4.setIcon(            
            QIcon(f"{self.current_dir}/resources/icons/forward_5_white_24dp.svg")
        )

    def _init_connect(self):
        self.TransparentToolButton_2.clicked.connect(self.close)
        self.TransparentToolButton.clicked.connect(self.play_pause_track)
        self.TransparentToolButton_5.clicked.connect(self.previous_track)
        self.TransparentToolButton_6.clicked.connect(self.skip_back)
        self.TransparentToolButton_3.clicked.connect(self.next_track)
        self.TransparentToolButton_4.clicked.connect(self.skip_forward)
        self.window.webview.titleChanged.connect(self.update_window_title)

    def play_pause_track(self):
        script = "var video = document.getElementsByTagName('video')[0];" \
                 "if (video.paused) video.play(); else video.pause();"
        self.window.webview.page().runJavaScript(script)

        self.update_play_pause_icon()

    def update_play_pause_icon(self):
        self.window.webview.page().runJavaScript(
            "var video = document.getElementsByTagName('video')[0]; video.paused;", 
            self.set_play_pause_icon
        )

    def set_play_pause_icon(self, is_paused):
        if is_paused:            
            self.TransparentToolButton.setIcon(
                QIcon(f"{self.current_dir}/resources/icons/play_circle_white_24dp.svg")
            )
        else:
            self.TransparentToolButton.setIcon(
                QIcon(f"{self.current_dir}/resources/icons/pause_circle_white_24dp.svg")
            )
    
    def set_track_image(self):
        self.window.webview.page().runJavaScript(
            'document.querySelector(".image.style-scope.ytmusic-player-bar").getAttribute("src")', 
            self.displayImage
        )

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

    def previous_track(self):
        self.window.webview.page().runJavaScript(
            'document.querySelector(".previous-button").click();'
        )   

    def skip_back(self):
        self.window.webview.page().runJavaScript(
            'document.querySelector("video").currentTime -= 5'
        )    

    def next_track(self):
        self.window.webview.page().runJavaScript(
            'document.querySelector(".next-button").click();'
        )  

    def skip_forward(self):
        self.window.webview.page().runJavaScript(
            'document.querySelector("video").currentTime += 5'
        )      

    def show_state(self):
        self.setFixedSize(243, 142)
        screen_geometry = QApplication.desktop().availableGeometry()
        self.setGeometry(
            QRect(
                screen_geometry.width() - 243, 
                screen_geometry.height() - 180,
                243,
                142 
            )
        )

    def enterEvent(self, event):
        super().enterEvent(event)
        self.show_state()

    def hide_state(self):
        self.setFixedSize(3, 142)
        screen_geometry = QApplication.desktop().availableGeometry()
        self.setGeometry(
            QRect(
                screen_geometry.width() - 3,
                screen_geometry.height() - 180, 
                243,
                142
            )
        )

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.hide_state()

    def _init_window(self):
        self.window.hide()
        self.show_state()

        self.setWindowTitle(self.name)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(243, 142)
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )

    def update_window_title(self, title):
        track_name = title.split("- YouTube Music")[0].strip()
        self.BodyLabel.setText(track_name)
        self.BodyLabel.setToolTip(track_name)

        self.update_play_pause_icon()
        self.set_track_image()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(0.7)
        painter.setBrush(Qt.black)        

        pen = QPen(QColor(84, 84, 84))
        pen.setWidth(2)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)

        painter.drawRect(self.contentsRect())

    def closeEvent(self, event):
        self.window.show()
        event.accept()