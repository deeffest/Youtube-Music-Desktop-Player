from typing import TYPE_CHECKING

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon
from qfluentwidgets import SystemTrayMenu, Action

if TYPE_CHECKING:
    from core.main_window import MainWindow


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.window: "MainWindow" = parent
        self.last_win_geo = None

        self.activated.connect(self.on_system_tray_icon_activated)
        self.create_context_menu()

    def create_context_menu(self):
        self.show_action = Action("YTMDPlayer", self)
        self.show_action.setIcon(QIcon(f"{self.window.icon_folder}/logo.png"))
        self.show_action.triggered.connect(
            lambda: self.window.show_window(self.last_win_geo)
        )

        self.play_pause_action = Action("Play/Pause", self)
        self.play_pause_action.setIcon(QIcon(f"{self.window.icon_folder}/play.png"))
        self.play_pause_action.setEnabled(False)
        self.play_pause_action.triggered.connect(self.window.play_pause)

        self.like_action = Action("Like", self)
        self.like_action.setIcon(QIcon(f"{self.window.icon_folder}/like.png"))
        self.like_action.setEnabled(False)
        self.like_action.triggered.connect(self.window.like)

        self.previous_action = Action("Previous", self)
        self.previous_action.setIcon(QIcon(f"{self.window.icon_folder}/previous.png"))
        self.previous_action.setEnabled(False)
        self.previous_action.triggered.connect(self.window.previous)

        self.next_action = Action("Next", self)
        self.next_action.setIcon(QIcon(f"{self.window.icon_folder}/next.png"))
        self.next_action.setEnabled(False)
        self.next_action.triggered.connect(self.window.next)

        self.dislike_action = Action("Dislike", self)
        self.dislike_action.setIcon(QIcon(f"{self.window.icon_folder}/dislike.png"))
        self.dislike_action.setEnabled(False)
        self.dislike_action.triggered.connect(self.window.dislike)

        self.exit_action = Action("Exit", self)
        self.exit_action.setIcon(QIcon(f"{self.window.icon_folder}/exit.png"))
        self.exit_action.triggered.connect(self.close_window)

        self.sytem_tray_menu = SystemTrayMenu()
        self.sytem_tray_menu.addAction(self.show_action)
        self.sytem_tray_menu.addSeparator()
        self.sytem_tray_menu.addAction(self.play_pause_action)
        self.sytem_tray_menu.addAction(self.like_action)
        self.sytem_tray_menu.addAction(self.previous_action)
        self.sytem_tray_menu.addAction(self.next_action)
        self.sytem_tray_menu.addAction(self.dislike_action)
        self.sytem_tray_menu.addSeparator()
        self.sytem_tray_menu.addAction(self.exit_action)

        self.setContextMenu(self.sytem_tray_menu)

    def on_system_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.window.show_window(self.last_win_geo)

    def close_window(self):
        self.window.force_exit = True
        self.window.close()
