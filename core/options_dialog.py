import pywinstyles

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

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
        self.settings = settings
        self.window = parent

        self.temp_settings = {}

        loadUi(
            f'{self.current_dir}/core/ui/options_dialog.ui', self
        )
        pywinstyles.apply_style(self, "dark")

        self._init_window()
        self._init_content()
        self._init_connect()
        self._init_tab_1()

    def _init_tab_1(self):
        self.PillPushButton.setChecked(True)
        self.PillPushButton_3.setChecked(False)
        self.PillPushButton_2.setChecked(False)

        self.frame_3.show()
        self.frame_4.hide()
        self.frame_5.hide()

    def _init_tab_2(self):
        self.PillPushButton_2.setChecked(True)
        self.PillPushButton_3.setChecked(False)
        self.PillPushButton.setChecked(False)

        self.frame_4.show()
        self.frame_3.hide()
        self.frame_5.hide()

    def _init_tab_3(self):
        self.PillPushButton_3.setChecked(True)
        self.PillPushButton_2.setChecked(False)
        self.PillPushButton.setChecked(False)

        self.frame_5.show()
        self.frame_4.hide()
        self.frame_3.hide()

    def _init_content(self):
        self.temp_settings["save_last_window_size"] = self.settings.value("save_last_window_size", "true") == "true"
        self.temp_settings["open_last_url_at_startup"] = self.settings.value("open_last_url_at_startup", "false") == "true"
        self.temp_settings["check_for_updates_at_startup"] = self.settings.value("check_for_updates_at_startup", "true") == "true"
        self.temp_settings["support_for_animated_scrolling"] = self.settings.value("support_for_animated_scrolling", "true") == "true"
        self.temp_settings["support_full_screen_mode"] = self.settings.value("support_full_screen_mode", "true") == "true"
        self.temp_settings["hide_window_in_tray"] = self.settings.value("hide_window_in_tray", "false") == "true"
        self.temp_settings["discord_integration"] = self.settings.value("discord_integration", "false") == "true"

        locations = ['Top Left Corner', 'Top Right Corner', 'Center Left', 'Center Right', 
                    'Center Top', 'Center Bottom', 'Center', 'Bottom Left Corner', 
                    'Bottom Right Corner']
        for location in locations:
            self.ComboBox.addItem(location)

        saved_index = self.settings.value("selected_location_index", 1)
        self.ComboBox.setCurrentIndex(saved_index)

        self.previous_zoom_factor = self.window.webview.zoomFactor()

        self.apply_settings()

    def apply_settings(self):
        self.SwitchButton.setChecked(self.temp_settings["save_last_window_size"])
        self.SwitchButton_6.setChecked(self.temp_settings["open_last_url_at_startup"])
        self.SwitchButton_4.setChecked(self.temp_settings["check_for_updates_at_startup"])
        self.SwitchButton_3.setChecked(self.temp_settings["support_for_animated_scrolling"])
        self.SwitchButton_5.setChecked(self.temp_settings["support_full_screen_mode"])
        self.SwitchButton_2.setChecked(self.temp_settings["hide_window_in_tray"])
        self.SwitchButton_7.setChecked(self.temp_settings["discord_integration"])

    def save_settings(self):
        self.settings.setValue("save_last_window_size", "true" if self.temp_settings["save_last_window_size"] else "false")
        self.settings.setValue("open_last_url_at_startup", "true" if self.temp_settings["open_last_url_at_startup"] else "false")
        self.settings.setValue("check_for_updates_at_startup", "true" if self.temp_settings["check_for_updates_at_startup"] else "false")
        self.settings.setValue("support_for_animated_scrolling", "true" if self.temp_settings["support_for_animated_scrolling"] else "false")
        self.settings.setValue("support_full_screen_mode", "true" if self.temp_settings["support_full_screen_mode"] else "false")
        self.settings.setValue("hide_window_in_tray", "true" if self.temp_settings["hide_window_in_tray"] else "false")
        self.settings.setValue("discord_integration", "true" if self.temp_settings["discord_integration"] else "false")

        self.window.websettings.setAttribute(
            QWebEngineSettings.FullScreenSupportEnabled, 
            self.settings.value("support_full_screen_mode", "true").lower() == "true"
        )

        self.window.websettings.setAttribute(
            QWebEngineSettings.ScrollAnimatorEnabled, 
            self.settings.value("support_for_animated_scrolling", "true").lower() == "true"
        )

        if self.settings.value("hide_window_in_tray", "false") == "true": 
            self.window.tray_icon.show() 
        else:
            self.window.tray_icon.hide()

        selected_index = self.ComboBox.currentIndex()
        self.settings.setValue("selected_location_index", selected_index)

        if self.settings.value("discord_integration", "false") == "true":
            if self.window.discord_rpc is None:
                self.window.setup_ds_integration()

    def _init_connect(self):
        self.PushButton.clicked.connect(self.save_and_close)
        self.PushButton_2.clicked.connect(self.cancel_and_close)
        self.PushButton_3.clicked.connect(self.set_default_zoom_factor)

        self.SwitchButton.checkedChanged.connect(self.set_temp_save_last_window_size)
        self.SwitchButton_6.checkedChanged.connect(self.set_temp_open_last_url_at_startup)
        self.SwitchButton_4.checkedChanged.connect(self.set_temp_check_for_updates_at_startup)
        self.SwitchButton_3.checkedChanged.connect(self.set_temp_support_for_animated_scrolling)
        self.SwitchButton_5.checkedChanged.connect(self.set_temp_support_full_screen_mode)
        self.SwitchButton_2.checkedChanged.connect(self.set_temp_hide_window_in_tray)
        self.SwitchButton_7.checkedChanged.connect(self.set_temp_discord_integration)

        self.PillPushButton.clicked.connect(self._init_tab_1)
        self.PillPushButton_2.clicked.connect(self._init_tab_2)
        self.PillPushButton_3.clicked.connect(self._init_tab_3)

    def set_default_zoom_factor(self):
        self.window.webview.setZoomFactor(1.0)

    def set_temp_save_last_window_size(self, state):
        self.temp_settings["save_last_window_size"] = state

    def set_temp_open_last_url_at_startup(self, state):
        self.temp_settings["open_last_url_at_startup"] = state

    def set_temp_check_for_updates_at_startup(self, state):
        self.temp_settings["check_for_updates_at_startup"] = state

    def set_temp_support_for_animated_scrolling(self, state):
        self.temp_settings["support_for_animated_scrolling"] = state

    def set_temp_support_full_screen_mode(self, state):
        self.temp_settings["support_full_screen_mode"] = state

    def set_temp_hide_window_in_tray(self, state):
        self.temp_settings["hide_window_in_tray"] = state

    def set_temp_discord_integration(self, state):
        self.temp_settings["discord_integration"] = state

    def _init_window(self):
        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(f"{self.window.icon_path}/settings.svg"))

    def save_and_close(self):
        self.save_settings()
        self.close()

    def cancel_and_close(self):
        self.window.webview.setZoomFactor(self.previous_zoom_factor)
        self.close()