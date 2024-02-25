from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import (
    QRect, Qt, QRectF, QUrl, QRegularExpression, 
    QStringListModel
)
from PyQt5.QtGui import (
    QPixmap, QIcon, QPainter, QPen, QColor, QMouseEvent,
    QPainterPath, QBrush
)
from PyQt5.QtWinExtras import (
    QWinThumbnailToolBar, QWinThumbnailToolButton  
)
from PyQt5.uic import loadUi
from qfluentwidgets import ToolTipFilter, ToolTipPosition

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
        super().__init__()

        self.current_dir = current_dir
        self.name = name
        self.window = parent
        self.settings = settings
        self.drag_position = None
        self.isDragging = False
        self.radius = 12        

        self.win_toolbar = QWinThumbnailToolBar(self)
        self.create_win_toolbar_buttons()

        loadUi(
            f'{self.current_dir}/core/ui/mini_player_dialog.ui', self
        )

        self._init_window()
        self._init_content()
        self._init_connect()

        self.show()

    def _init_content(self):
        self.change_info(self.window.webview.url())

        self.ToolButton.setIcon(
            QIcon(f"{self.current_dir}/resources/icons/close_white_24dp.svg")
        )
        self.ToolButton_2.setIcon(
            QIcon(f"{self.current_dir}/resources/icons/minimize_white_24dp.svg")
        )
        self.TransparentToolButton.setIcon(            
            QIcon(f"{self.current_dir}/resources/icons/skip_previous_white_24dp.svg")
        )
        self.TransparentToolButton_3.setIcon(
            QIcon(f"{self.current_dir}/resources/icons/skip_next_white_24dp.svg")
        )
        self.PillToolButton.setIcon(
            QIcon(f"{self.current_dir}/resources/icons/push_pin_white_24dp.svg")
        )

    def _init_connect(self):
        self.ToolButton.clicked.connect(self.close)
        self.ToolButton_2.clicked.connect(lambda: self.showMinimized())
        self.TransparentToolButton_2.clicked.connect(self.play_pause_track)
        self.TransparentToolButton.clicked.connect(self.previous_track)
        self.TransparentToolButton_3.clicked.connect(self.next_track)
        self.window.webview.urlChanged.connect(self.update_info)
        self.window.webview.titleChanged.connect(self.change_title)
        self.PillToolButton.clicked.connect(self.toggle_on_top_hint)
        self.tool_btn_previous.clicked.connect(self.previous_track)
        self.tool_btn_next.clicked.connect(self.next_track)
        self.tool_btn_play_pause.clicked.connect(self.play_pause_track)

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
            self.TransparentToolButton_2.setIcon(
                QIcon(f"{self.current_dir}/resources/icons/play_arrow_white_24dp.svg")
            )
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/play_arrow_white_24dp.svg"
            ))   
        else:
            self.TransparentToolButton_2.setIcon(
                QIcon(f"{self.current_dir}/resources/icons/pause_white_24dp.svg")
            )
            self.tool_btn_play_pause.setIcon(QIcon(
                f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
            ))  
    
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

    def next_track(self):
        self.window.webview.page().runJavaScript(
            'document.querySelector(".next-button").click();'
        )     

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            if not self.isDragging:
                self.isDragging = True
            self.move(event.globalPos() - self.drag_position)
        super(MiniPlayerDlg, self).mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
        self.isDragging = True
        super(MiniPlayerDlg, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.isDragging = False
        super(MiniPlayerDlg, self).mouseReleaseEvent(event)

    def toggle_on_top_hint(self):
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.PillToolButton.setChecked(False)
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.PillToolButton.setChecked(True)
        self.show()

    def _init_window(self):
        self.window.hide()

        self.setWindowTitle(self.name)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(360, 180)
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )

    def update_info(self, url):
        try:
            yt = pytube.YouTube(QUrl(url).toString())
            self.StrongBodyLabel.setText(yt.title)
            self.StrongBodyLabel.setToolTip(yt.title)
            self.StrongBodyLabel.installEventFilter(
                ToolTipFilter(
                    self.StrongBodyLabel, 0, 
                    ToolTipPosition.TOP
            ))
            self.BodyLabel_2.setText(yt.author)
            self.BodyLabel_2.setToolTip(yt.author)
            self.BodyLabel_2.installEventFilter(
                ToolTipFilter(
                    self.BodyLabel_2, 0, 
                    ToolTipPosition.TOP
            ))
        except pytube.exceptions.PytubeError as e:
            print("pytube error:", e)

    def change_info(self, url):
        self.set_track_image()
        self.update_play_pause_icon()
        self.update_info(url)

    def change_title(self, title):
        self.set_track_image()
        self.update_play_pause_icon()
        self.setWindowTitle(title)

    def create_win_toolbar_buttons(self):
        self.tool_btn_previous = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_previous.setToolTip('Previous')
        self.tool_btn_previous.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_previous_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_previous)

        self.tool_btn_play_pause = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_play_pause.setToolTip('Play/Pause')
        self.tool_btn_play_pause.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/pause_white_24dp.svg"
        ))                     
        self.win_toolbar.addButton(self.tool_btn_play_pause)

        self.tool_btn_next = QWinThumbnailToolButton(self.win_toolbar)
        self.tool_btn_next.setToolTip('Next')
        self.tool_btn_next.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_next_white_24dp.svg"
        ))
        self.win_toolbar.addButton(self.tool_btn_next)

    def _shape(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), self.radius, self.radius)
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(self._shape(), QBrush(QColor(0, 0, 0, 192)))
        painter.setPen(QPen(QColor(84, 84, 84), 2))
        painter.drawPath(self._shape())

    def showEvent(self, event):
        super().showEvent(event)
        if not self.win_toolbar.window():
            self.win_toolbar.setWindow(self.windowHandle())

    def closeEvent(self, event):
        self.window.show()
        self.deleteLater()