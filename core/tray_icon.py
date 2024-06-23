from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QIcon

from qfluentwidgets import SystemTrayMenu, Action

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
        
        if self.settings.value("hide_window_in_tray", "false") == "true":
            self.show() 
        else:
            self.hide()

        self._init_content()

    def _init_content(self):
        menu = SystemTrayMenu()

        self.hide_show_action = Action('Hide/Show', self)
        self.hide_show_action.triggered.connect(self.hide_show_check)
        self.hide_show_action.setIcon(QIcon(f"{self.window.icon_path}/eye_show.svg"))
        menu.addAction(self.hide_show_action)
        
        self.setContextMenu(menu)

        menu.addSeparator()

        self.play_pause_action = Action('Play/Pause', self)
        self.play_pause_action.triggered.connect(self.window.play_pause_track)
        self.play_pause_action.setIcon(QIcon(f"{self.window.icon_path}/play.svg"))
        menu.addAction(self.play_pause_action)
        
        self.previous_track_action = Action('Previous', self)
        self.previous_track_action.triggered.connect(self.window.previous_track)
        self.previous_track_action.setIcon(QIcon(f"{self.window.icon_path}/previous.svg"))
        menu.addAction(self.previous_track_action)        

        self.next_track_action = Action('Next', self)
        self.next_track_action.triggered.connect(self.window.next_track)
        self.next_track_action.setIcon(QIcon(f"{self.window.icon_path}/next.svg"))
        menu.addAction(self.next_track_action)

        menu.addSeparator()

        self.exit_action = Action('Exit', self)
        self.exit_action.triggered.connect(self.window.exit_app)
        self.exit_action.setIcon(QIcon(f"{self.window.icon_path}/dismiss.svg"))
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