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

        self.connect_signals()
        self.create_context_menu()

    def connect_signals(self):
        self.activated.connect(self.on_tray_icon_activated)
        self.messageClicked.connect(self.window.show_window)

    def create_context_menu(self):
        self.tray_menu = SystemTrayMenu()

        self.show_action = Action("YTMDPlayer", self)
        self.show_action.setIcon(QIcon(f"{self.window.icon_folder}/logo.png"))
        self.show_action.triggered.connect(self.window.show_window)
        self.tray_menu.addAction(self.show_action)

        self.tray_menu.addSeparator()

        self.play_pause_action = Action("Play/Pause", self)
        self.play_pause_action.setIcon(QIcon(f"{self.window.icon_folder}/play.png"))
        self.play_pause_action.triggered.connect(self.window.play_pause)
        self.play_pause_action.setEnabled(False)
        self.tray_menu.addAction(self.play_pause_action)

        self.volume_up_action = Action("Volume Up", self)
        self.volume_up_action.setIcon(QIcon(f"{self.window.icon_folder}/volume_up.png"))
        self.volume_up_action.triggered.connect(self.window.volume_up)
        self.volume_up_action.setEnabled(False)
        self.tray_menu.addAction(self.volume_up_action)

        self.previous_action = Action("Previous", self)
        self.previous_action.setIcon(QIcon(f"{self.window.icon_folder}/previous.png"))
        self.previous_action.triggered.connect(self.window.skip_previous)
        self.previous_action.setEnabled(False)
        self.tray_menu.addAction(self.previous_action)

        self.next_action = Action("Next", self)
        self.next_action.setIcon(QIcon(f"{self.window.icon_folder}/next.png"))
        self.next_action.triggered.connect(self.window.skip_next)
        self.next_action.setEnabled(False)
        self.tray_menu.addAction(self.next_action)

        self.volume_down_action = Action("Volume Down", self)
        self.volume_down_action.setIcon(
            QIcon(f"{self.window.icon_folder}/volume_down.png")
        )
        self.volume_down_action.triggered.connect(self.window.volume_down)
        self.volume_down_action.setEnabled(False)
        self.tray_menu.addAction(self.volume_down_action)

        self.tray_menu.addSeparator()

        self.exit_action = Action("Exit", self)
        self.exit_action.setIcon(QIcon(f"{self.window.icon_folder}/exit.png"))
        self.exit_action.triggered.connect(self.close_window)
        self.tray_menu.addAction(self.exit_action)

        self.setContextMenu(self.tray_menu)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.window.show_window()

    def close_window(self):
        self.window.force_exit = True
        self.window.close()
