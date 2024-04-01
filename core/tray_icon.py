from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QAction, QMenu
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

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
        menu = QMenu()

        self.hide_show_action = QAction('Hide/Show', self)
        self.hide_show_action.triggered.connect(self.hide_show_check)
        self.hide_show_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/visibility_white_24dp.svg"))
        menu.addAction(self.hide_show_action)
        
        self.setContextMenu(menu)

        menu.addSeparator()

        self.play_pause_action = QAction('Play/Pause', self)
        self.play_pause_action.triggered.connect(self.window.play_pause_track)
        self.play_pause_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/play_arrow_white_24dp.svg"))
        menu.addAction(self.play_pause_action)
        
        self.previous_track_action = QAction('Previous', self)
        self.previous_track_action.triggered.connect(self.window.previous_track)
        self.previous_track_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_previous_white_24dp.svg"))
        menu.addAction(self.previous_track_action)        

        self.next_track_action = QAction('Next', self)
        self.next_track_action.triggered.connect(self.window.next_track)
        self.next_track_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/skip_next_white_24dp.svg"))
        menu.addAction(self.next_track_action)

        menu.addSeparator()

        self.exit_action = QAction('Exit', self)
        self.exit_action.triggered.connect(self.window.close_in_tray)
        self.exit_action.setIcon(QIcon(
            f"{self.current_dir}/resources/icons/win_toolbar_icons/close_white_24dp.svg"))
        menu.addAction(self.exit_action)
        
        self.setContextMenu(menu)

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