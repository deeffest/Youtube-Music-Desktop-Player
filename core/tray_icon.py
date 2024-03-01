from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from qfluentwidgets import SystemTrayMenu, Action

import requests
import sys

class TrayIcon(QSystemTrayIcon):
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

        self.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )
        self.activated.connect(self.on_tray_icon_activated)
        
        if self.settings.value("hide_window_in_tray", "true") == "true":
            self.show() 
        else:
            self.hide()  

        self._init_content()

    def _init_content(self):
        menu = SystemTrayMenu(parent=self.window)

        self.play_pause_action = Action('Play/Pause', triggered=self.window.play_pause_track)
        self.play_pause_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/play_arrow_white_24dp.svg"))
        menu.addAction(self.play_pause_action)

        menu.addSeparator()
        
        self.previous_track_action = Action('Previous', triggered=self.window.previous_track)
        self.previous_track_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/skip_previous_white_24dp.svg"))
        menu.addAction(self.previous_track_action)        

        self.next_track_action = Action('Next', triggered=self.window.next_track)
        self.next_track_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/skip_next_white_24dp.svg"))
        menu.addAction(self.next_track_action)

        menu.addSeparator()

        self.exit_action = Action('Exit', triggered=self.window.close_in_tray)
        self.exit_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/close_white_24dp.svg"))
        menu.addAction(self.exit_action)
        
        self.setContextMenu(menu)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.hide_show_check()

    def hide_show_check(self):
        if self.window.isMinimized():
            self.window.showNormal()
            self.window.activateWindow()
            self.hide()
        else:
            if self.window.isMinimized():
                self.window.showNormal()
                self.window.activateWindow()
                self.hide()
            elif self.window.isVisible():
                self.window.hide()
            else:
                self.window.showNormal()
                self.window.activateWindow()
                self.hide()

