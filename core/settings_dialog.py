import pywinstyles

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = parent

        self.load_ui()
        self.setup_content()
        self.set_connect()
        self.set_icons()
        self.configure_tabs()
        self.setup_settings()

    def setup_content(self):
        int_validator = QIntValidator()
        self.LineEdit_2.setValidator(int_validator)
        self.proxy_types = ["HttpProxy", "Socks5Proxy", 
                            "DefaultProxy", "NoProxy"]
        self.ComboBox.addItems(self.proxy_types)

    def setup_settings(self):
        self.SwitchButton.setChecked(self.window.save_last_win_size_setting)
        self.SwitchButton_4.setChecked(self.window.open_last_url_at_startup_setting)
        self.SwitchButton_3.setChecked(self.window.ad_blocker_setting)
        self.SwitchButton_5.setChecked(self.window.fullscreen_mode_support_setting)
        self.SwitchButton_6.setChecked(self.window.support_animated_scrolling_setting)
        self.SwitchButton_2.setChecked(self.window.save_last_pos_of_mp_setting)
        self.SwitchButton_8.setChecked(self.window.save_last_zoom_factor_setting)
        self.SwitchButton_7.setChecked(self.window.discord_rpc_setting)
        self.SwitchButton_11.setChecked(self.window.win_thumbmail_buttons_setting)
        self.SwitchButton_12.setChecked(self.window.tray_icon_setting)
        self.ComboBox.setCurrentIndex(self.proxy_types.index(self.window.proxy_type_setting))
        if self.window.proxy_host_name_setting is not None:
            self.LineEdit.setText(self.window.proxy_host_name_setting)
        if self.window.proxy_port_setting is not None:
            self.LineEdit_2.setText(str(self.window.proxy_port_setting))
        if self.window.proxy_login_setting is not None:
            self.LineEdit_3.setText(self.window.proxy_login_setting)
        if self.window.proxy_password_setting is not None:
            self.PasswordLineEdit.setText(self.window.proxy_password_setting)

    def set_icons(self):
        self.PillPushButton_4.setIcon(self.window.icon_folder+"/plugins.png")

    def set_connect(self):
        self.PillPushButton.clicked.connect(self.configure_tabs)
        self.PillPushButton_2.clicked.connect(self.configure_tabs)
        self.PillPushButton_3.clicked.connect(self.configure_tabs)
        self.PillPushButton_4.clicked.connect(self.configure_tabs)
        self.PrimaryPushButton.clicked.connect(self.save_and_close)
        self.PushButton.clicked.connect(self.close)

    def save_and_close(self):
        self.window.save_last_win_size_setting = int(self.SwitchButton.isChecked())
        self.window.open_last_url_at_startup_setting = int(self.SwitchButton_4.isChecked())
        self.window.ad_blocker_setting = int(self.SwitchButton_3.isChecked())
        self.window.fullscreen_mode_support_setting = int(self.SwitchButton_5.isChecked())
        self.window.support_animated_scrolling_setting = int(self.SwitchButton_6.isChecked())
        self.window.save_last_pos_of_mp_setting = int(self.SwitchButton_2.isChecked())
        self.window.save_last_zoom_factor_setting = int(self.SwitchButton_8.isChecked())
        self.window.discord_rpc_setting = int(self.SwitchButton_7.isChecked())
        self.window.win_thumbmail_buttons_setting = int(self.SwitchButton_11.isChecked())
        self.window.tray_icon_setting = int(self.SwitchButton_12.isChecked())
        self.window.proxy_type_setting = self.ComboBox.currentText()
        self.window.proxy_host_name_setting = self.LineEdit.text()
        port_text = self.LineEdit_2.text()
        self.window.proxy_port_setting = int(port_text) if port_text else None
        self.window.proxy_login_setting = self.LineEdit_3.text()
        self.window.proxy_password_setting = self.PasswordLineEdit.text()

        self.window.settings_.setValue("save_last_win_size", self.window.save_last_win_size_setting)
        self.window.settings_.setValue("open_last_url_at_startup", self.window.open_last_url_at_startup_setting)
        self.window.settings_.setValue("ad_blocker", self.window.ad_blocker_setting)
        self.window.settings_.setValue("fullscreen_mode_support", self.window.fullscreen_mode_support_setting)
        self.window.settings_.setValue("support_animated_scrolling", self.window.support_animated_scrolling_setting)
        self.window.settings_.setValue("save_last_pos_of_mp", self.window.save_last_pos_of_mp_setting)
        self.window.settings_.setValue("save_last_zoom_factor", self.window.save_last_zoom_factor_setting)
        self.window.settings_.setValue("discord_rpc", self.window.discord_rpc_setting)
        self.window.settings_.setValue("win_thumbmail_buttons", self.window.win_thumbmail_buttons_setting)
        self.window.settings_.setValue("tray_icon", self.window.tray_icon_setting)
        self.window.settings_.setValue("proxy_type", self.window.proxy_type_setting)
        self.window.settings_.setValue("proxy_host_name", self.window.proxy_host_name_setting)
        self.window.settings_.setValue("proxy_port", self.window.proxy_port_setting)
        self.window.settings_.setValue("proxy_login", self.window.proxy_login_setting)
        self.window.settings_.setValue("proxy_password", self.window.proxy_password_setting)

        self.close()

    def configure_tabs(self):
        self.frame.hide()
        self.frame_2.hide()
        self.frame_3.hide()
        self.frame_4.hide()
        self.frame_5.hide()

        icon_path = self.window.icon_folder + "/plugins.png"

        if self.PillPushButton.isChecked():
            self.frame.show()
        elif self.PillPushButton_2.isChecked():
            self.frame_2.show()
        elif self.PillPushButton_3.isChecked():
            self.frame_3.show()        
        else:
            self.frame_4.show()
            icon_path = self.window.icon_folder + "/plugins-black.png"

        self.PillPushButton_4.setIcon(icon_path)

    def load_ui(self):
        loadUi(f'{self.window.current_dir}/core/ui/settings_dialog.ui', self)
        pywinstyles.apply_style(self, "dark")

        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/settings-red.png"))
        
        self.setFixedSize(self.size())

    def closeEvent(self, event):
        self.window.show()
        event.accept()