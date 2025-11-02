import logging
import platform
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QDesktopWidget
from qfluentwidgets import ToolTipFilter, ToolTipPosition

from core.thumbnail_loader import ThumbnailLoader
from core.helpers import get_taskbar_position, get_current_desktop_environment
from core.ui.ui_mini_player_dialog import Ui_MiniPlayerDialog

if TYPE_CHECKING:
    from core.main_window import MainWindow


class MiniPlayerDialog(QDialog, Ui_MiniPlayerDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent
        self.thumbnail_loader_thread = None

        self.configure_window()
        self.configure_ui_elements()

    def configure_window(self):
        if platform.system() == "Windows":
            from pywinstyles import apply_style  # type: ignore

            try:
                apply_style(self, "dark")
            except Exception as e:
                logging.error(f"Failed to apply dark style: + {str(e)}")

        self.setupUi(self)
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

    def configure_ui_elements(self):
        self.previous_button.clicked.connect(self.window.skip_previous)
        self.play_pause_button.clicked.connect(self.window.play_pause)
        self.next_button.clicked.connect(self.window.skip_next)
        self.volume_down_button.clicked.connect(self.window.volume_down)
        self.volume_up_button.clicked.connect(self.window.volume_up)

        if get_current_desktop_environment() != "Xfce":
            self.previous_button.installEventFilter(
                ToolTipFilter(self.previous_button, 300, ToolTipPosition.TOP)
            )
            self.play_pause_button.installEventFilter(
                ToolTipFilter(self.play_pause_button, 300, ToolTipPosition.TOP)
            )
            self.next_button.installEventFilter(
                ToolTipFilter(self.next_button, 300, ToolTipPosition.TOP)
            )
            self.volume_down_button.installEventFilter(
                ToolTipFilter(self.volume_down_button, 300, ToolTipPosition.TOP)
            )
            self.volume_up_button.installEventFilter(
                ToolTipFilter(self.volume_up_button, 300, ToolTipPosition.TOP)
            )

        self.previous_button.setIcon(
            QIcon(f"{self.window.icon_folder}/previous-filled.png")
        )
        self.play_pause_button.setIcon(
            QIcon(f"{self.window.icon_folder}/play-filled.png")
        )
        self.next_button.setIcon(QIcon(f"{self.window.icon_folder}/next-filled.png"))
        self.volume_down_button.setIcon(
            QIcon(f"{self.window.icon_folder}/volume_down.png")
        )
        self.volume_up_button.setIcon(QIcon(f"{self.window.icon_folder}/volume_up.png"))

    def load_thumbnail(self, url):
        self.stop_running_threads()

        self.thumbnail_loader_thread = ThumbnailLoader(url, self.window)
        self.thumbnail_loader_thread.thumbnail_loaded.connect(self.on_thumbnail_loaded)
        self.thumbnail_loader_thread.start()

    def on_thumbnail_loaded(self, pixmap):
        self.thumbnail_loader_thread = None

        self.thumbnail = pixmap
        self.thumbnail_label.setPixmap(self.thumbnail)

    def save_geometry_of_mp(self):
        if self.window.save_last_pos_of_mp_setting == 1:
            self.window.geometry_of_mp_setting = self.geometry()
            self.window.settings_.setValue(
                "geometry_of_mp", self.window.geometry_of_mp_setting
            )

    def stop_running_threads(self):
        if (
            self.thumbnail_loader_thread is not None
            and self.thumbnail_loader_thread.isRunning()
        ):
            self.thumbnail_loader_thread.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.save_geometry_of_mp()
        self.stop_running_threads()

        self.window.show()
        self.window.show_tray_icon()

        self.window.mini_player_dialog = None
        event.accept()
