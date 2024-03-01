from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtWebEngineWidgets import (
    QWebEngineSettings
)

import os

class OptionsDlg(QDialog):
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
            f'{self.current_dir}/core/ui/options_dialog.ui', self
        )

        self._init_window()
        self._init_content()
        self._init_connect()
        self._init_tab_1()

    def _init_tab_1(self):
        self.PillPushButton.setChecked(True)
        self.PillPushButton_2.setChecked(False)

        self.frame_3.show()

        self.frame_4.hide()

    def _init_tab_2(self):
        self.PillPushButton_2.setChecked(True)
        self.PillPushButton.setChecked(False)

        self.frame_4.show()
        self.frame_3.hide()

    def _init_content(self):
        if self.settings.value("save_last_window_size", "true") == "true":
            self.SwitchButton.setChecked(True)
        else:
            self.SwitchButton.setChecked(False)

        if self.settings.value("open_last_url_at_startup", "false") == "true":
            self.SwitchButton_6.setChecked(True)
        else:
            self.SwitchButton_6.setChecked(False)

        if self.settings.value("check_for_updates_at_startup", "true") == "true":
            self.SwitchButton_4.setChecked(True)
        else:
            self.SwitchButton_4.setChecked(False)

        if self.settings.value("support_for_animated_scrolling", "true") == "true":
            self.SwitchButton_3.setChecked(True)
        else:
            self.SwitchButton_3.setChecked(False)

        if self.settings.value("support_full_screen_mode", "true") == "true":
            self.SwitchButton_5.setChecked(True)
        else:
            self.SwitchButton_5.setChecked(False)

        if self.settings.value("hide_window_in_tray", "true") == "true":
            self.SwitchButton_2.setChecked(True)
        else:
            self.SwitchButton_2.setChecked(False)

    def _init_connect(self):
        self.PushButton.clicked.connect(self.close)
        self.SwitchButton.checkedChanged.connect(self.save_last_window_size)
        self.SwitchButton_6.checkedChanged.connect(self.open_last_url_at_startup)
        self.SwitchButton_4.checkedChanged.connect(self.check_for_updates_at_startup)
        self.SwitchButton_3.checkedChanged.connect(self.support_for_animated_scrolling)
        self.SwitchButton_5.checkedChanged.connect(self.support_full_screen_mode)
        self.SwitchButton_2.checkedChanged.connect(self.hide_window_in_tray)

        self.PillPushButton.clicked.connect(self._init_tab_1)
        self.PillPushButton_2.clicked.connect(self._init_tab_2)

    def add_to_autorun(self):
        if self.settings.value("add_to_autorun", "false") == "false":
            self.settings.setValue("add_to_autorun", "true")
            self.add_from_autorun()
        else:
            self.settings.setValue("add_to_autorun", "false")           
            self.remove_from_autorun()

    def hide_window_in_tray(self):
        if self.settings.value("hide_window_in_tray", "true") == "true":
            self.settings.setValue("hide_window_in_tray", "false")
        else:
            self.settings.setValue("hide_window_in_tray", "true")

    def support_full_screen_mode(self):
        if self.settings.value("support_full_screen_mode", "true") == "true":
            self.settings.setValue("support_full_screen_mode", "false")
        else:
            self.settings.setValue("support_full_screen_mode", "true")

        self.window.websettings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, 
            self.settings.value(
                "support_full_screen_mode", "true").lower() == "true"
        )

    def support_for_animated_scrolling(self):
        if self.settings.value("support_for_animated_scrolling", "true") == "true":
            self.settings.setValue("support_for_animated_scrolling", "false")
        else:
            self.settings.setValue("support_for_animated_scrolling", "true")

        self.window.websettings.setAttribute(
            QWebEngineSettings.ScrollAnimatorEnabled, 
            self.settings.value(
                "support_for_animated_scrolling", "true").lower() == "true"
        )

    def check_for_updates_at_startup(self):
        if self.settings.value("check_for_updates_at_startup", "true") == "true":
            self.settings.setValue("check_for_updates_at_startup", "false")
        else:
            self.settings.setValue("check_for_updates_at_startup", "true")

    def open_last_url_at_startup(self):
        if self.settings.value("open_last_url_at_startup", "false") == "true":
            self.settings.setValue("open_last_url_at_startup", "false")
        else:
            self.settings.setValue("open_last_url_at_startup", "true")

    def save_last_window_size(self):
        if self.settings.value("save_last_window_size", "true") == "true":
            self.settings.setValue("save_last_window_size", "false")
        else:
            self.settings.setValue("save_last_window_size", "true")

    def _init_window(self):
        self.setWindowTitle(self.name)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(
            f"{self.current_dir}/resources/icons/icon.ico")
        )