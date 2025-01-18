import logging
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QDesktopWidget
from qfluentwidgets import ToolTipFilter, ToolTipPosition
from pywinstyles import apply_style

from core.thumbnail_loader import ThumbnailLoader
from core.helpers import get_taskbar_position
if TYPE_CHECKING:
    from core.main_window import MainWindow
from core.ui.ui_mini_player_dialog import Ui_MiniPlayerDialog


class MiniPlayerDialog(QDialog, Ui_MiniPlayerDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.window:"MainWindow" = parent

        try:
            apply_style(self, "dark")
        except Exception as e:
            logging.error("Failed to apply dark style: " + str(e))

        self.setWindowTitle("Mini-Player")
        self.setWindowFlags(Qt.Window)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        if self.window.save_last_pos_of_mp_setting == 1:
            self.setGeometry(self.window.geometry_of_mp_setting)
        else:
            screen_geometry = QDesktopWidget().screenGeometry()
            taskbar_position = get_taskbar_position()
            x = screen_geometry.width() - self.width() - 30
            y = screen_geometry.height() - self.height() - 30
            if taskbar_position == "Right":
                x = screen_geometry.width() - self.width() - 93
            elif taskbar_position == "Bottom":
                y = screen_geometry.height() - self.height() - 71
            self.setGeometry(x, y, self.width(), self.height())
        self.setFixedSize(self.size())

        self.thumbnail = QPixmap()
        self.current_loader = None
        
        self.previous_button.clicked.connect(self.window.skip_previous)
        self.play_pause_button.clicked.connect(self.window.play_pause)
        self.next_button.clicked.connect(self.window.skip_next)
        self.like_button.clicked.connect(self.window.like)
        self.dislike_button.clicked.connect(self.window.dislike)

        self.previous_button.installEventFilter(ToolTipFilter(self.previous_button, 300, ToolTipPosition.TOP))
        self.play_pause_button.installEventFilter(ToolTipFilter(self.play_pause_button, 300, ToolTipPosition.TOP))
        self.next_button.installEventFilter(ToolTipFilter(self.next_button, 300, ToolTipPosition.TOP))
        self.like_button.installEventFilter(ToolTipFilter(self.like_button, 300, ToolTipPosition.TOP))
        self.dislike_button.installEventFilter(ToolTipFilter(self.dislike_button, 300, ToolTipPosition.TOP))

        self.previous_button.setIcon(QIcon(f"{self.window.icon_folder}/previous-filled.png"))
        self.play_pause_button.setIcon(QIcon(f"{self.window.icon_folder}/play-filled.png"))
        self.next_button.setIcon(QIcon(f"{self.window.icon_folder}/next-filled.png"))
        self.like_button.setIcon(QIcon(f"{self.window.icon_folder}/like.png"))
        self.dislike_button.setIcon(QIcon(f"{self.window.icon_folder}/dislike.png"))

    def load_thumbnail(self, url):
        if hasattr(self, "thumbnail_loader") and self.thumbnail_loader.isRunning():
            self.thumbnail_loader.terminate()
            self.thumbnail_loader.wait()

        self.thumbnail_loader = ThumbnailLoader(url, self.window)
        self.thumbnail_loader.thumbnail_loaded.connect(self.on_thumbnail_loaded)
        self.thumbnail_loader.start()

    def on_thumbnail_loaded(self, pixmap):
        self.thumbnail = pixmap
        self.thumbnail_label.setPixmap(self.thumbnail)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
            
    def closeEvent(self, event):
        if self.window.save_last_pos_of_mp_setting == 1:
            self.window.geometry_of_mp_setting = self.geometry()
            self.window.settings_.setValue("geometry_of_mp", self.window.geometry_of_mp_setting)
        
        self.window.show()
        self.window.show_tray_icon()

        self.window.mini_player_dialog = None
        event.accept()
