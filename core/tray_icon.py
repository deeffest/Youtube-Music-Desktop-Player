from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import requests

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
        self.show()    

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.hide_show_check()

    def hide_show_check(self):
        if self.window.isMinimized():
            self.window.showNormal()
            self.window.activateWindow()
        else:
            if self.window.isMinimized():
                self.window.showNormal()
                self.window.activateWindow()
            elif self.window.isVisible():
                self.window.hide()
            else:
                self.window.showNormal()
                self.window.activateWindow()

