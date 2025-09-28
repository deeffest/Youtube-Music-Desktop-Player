import sys
import logging
import platform
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt, QProcess, QRegExp, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QApplication, QSystemTrayIcon
from qfluentwidgets import (
    MessageBox,
    ToolTipFilter,
    ToolTipPosition,
)

from core.ui.ui_settings_dialog import Ui_SettingsDialog

if TYPE_CHECKING:
    from main_window import MainWindow


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

        self.configure_window()
        self.configure_ui_elements()

    def configure_window(self):
        if platform.system() == "Windows":
            from pywinstyles import apply_style

            try:
                apply_style(self, "dark")
            except Exception as e:
                logging.error(f"Failed to apply dark style: + {str(e)}")

        self.setupUi(self)
        self.setWindowTitle("Settings")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(f"{self.window.icon_folder}/settings.png"))
        self.setFixedSize(self.size())

    def configure_ui_elements(self):
        self.PillPushButton.setChecked(True)
        regex = QRegExp(r"^[1-9][0-9]{0,4}$")
        regex_validator = QRegExpValidator(regex)
        self.LineEdit_2.setValidator(regex_validator)
        self.proxy_types = ["HttpProxy", "Socks5Proxy", "DefaultProxy", "NoProxy"]
        self.ComboBox.addItems(self.proxy_types)
        self.opengl_enviroments = ["Desktop", "Angle", "Software", "Auto"]
        self.ComboBox_3.addItems(self.opengl_enviroments)

        self.PillPushButton.clicked.connect(self.configure_tabs)
        self.PillPushButton_2.clicked.connect(self.configure_tabs)
        self.PillPushButton_3.clicked.connect(self.configure_tabs)
        self.PillPushButton_4.clicked.connect(self.configure_tabs)
        self.PushButton_2.clicked.connect(self.restart_app)
        self.PrimaryPushButton.clicked.connect(self.save_settings)
        self.PushButton.clicked.connect(self.close)
        self.ComboBox.currentIndexChanged.connect(self.toggle_proxy_config)

        self.SwitchButton.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_4.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_3.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_5.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_6.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_2.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_8.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_7.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_12.checkedChanged.connect(self.check_if_settings_changed)
        self.ComboBox.currentIndexChanged.connect(self.check_if_settings_changed)
        self.LineEdit.textChanged.connect(self.check_if_settings_changed)
        self.LineEdit_2.textChanged.connect(self.check_if_settings_changed)
        self.LineEdit_3.textChanged.connect(self.check_if_settings_changed)
        self.PasswordLineEdit.textChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_14.checkedChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_15.checkedChanged.connect(self.check_if_settings_changed)
        self.ComboBox_3.currentIndexChanged.connect(self.check_if_settings_changed)
        self.SwitchButton_16.checkedChanged.connect(self.check_if_settings_changed)
        self.checkBox.toggled.connect(self.check_if_settings_changed)

        self.configure_tabs()

        self.SwitchButton.setChecked(self.window.save_last_win_geometry_setting)
        self.SwitchButton_4.setChecked(self.window.open_last_url_at_startup_setting)
        self.SwitchButton_3.setChecked(self.window.ad_blocker_setting)
        self.SwitchButton_5.setChecked(self.window.fullscreen_mode_support_setting)
        self.SwitchButton_6.setChecked(self.window.support_animated_scrolling_setting)
        self.SwitchButton_2.setChecked(self.window.save_last_pos_of_mp_setting)
        self.SwitchButton_8.setChecked(self.window.save_last_zoom_factor_setting)
        self.SwitchButton_7.setChecked(self.window.discord_rpc_setting)
        self.SwitchButton_12.setChecked(self.window.tray_icon_setting)
        self.ComboBox.setCurrentIndex(
            self.proxy_types.index(self.window.proxy_type_setting)
        )
        self.toggle_proxy_config()
        if self.window.proxy_host_name_setting is not None:
            self.LineEdit.setText(self.window.proxy_host_name_setting)
        if self.window.proxy_port_setting is not None:
            self.LineEdit_2.setText(str(self.window.proxy_port_setting))
        if self.window.proxy_login_setting is not None:
            self.LineEdit_3.setText(self.window.proxy_login_setting)
        if self.window.proxy_password_setting is not None:
            self.PasswordLineEdit.setText(self.window.proxy_password_setting)
        self.SwitchButton_14.setChecked(self.window.hotkey_playback_control_setting)
        self.SwitchButton_15.setChecked(self.window.only_audio_mode_setting)
        self.ComboBox_3.setCurrentIndex(
            self.opengl_enviroments.index(self.window.opengl_enviroment_setting)
        )
        self.SwitchButton_16.setChecked(self.window.nonstop_music_setting)
        self.checkBox.setChecked(self.window.block_video_setting)

        self.check_settings_dependency()
        self.SwitchButton_12.checkedChanged.connect(self.check_settings_dependency)
        self.SwitchButton_15.checkedChanged.connect(self.check_settings_dependency)

        self.check_if_settings_changed()

        self.PushButton_2.setIcon(QIcon(f"{self.window.icon_folder}/restart.png"))
        self.PillPushButton_4.setIcon(
            QIcon(QPixmap(f"{self.window.icon_folder}/plugins.png"))
        )
        self.label.setPixmap(QPixmap(f"{self.window.icon_folder}/adblock.png"))
        self.label_2.setPixmap(QPixmap(f"{self.window.icon_folder}/discord.png"))
        self.label_4.setPixmap(QPixmap(f"{self.window.icon_folder}/logo.png"))
        self.label_7.setPixmap(QPixmap(f"{self.window.icon_folder}/hotkeys.png"))
        self.label_9.setPixmap(QPixmap(f"{self.window.icon_folder}/audio.png"))
        self.label_11.setPixmap(QPixmap(f"{self.window.icon_folder}/nonstop-music.png"))

        self.label_8.setToolTip(
            "• HttpProxy: For HTTP/HTTPS traffic.\n"
            "• Socks5Proxy: For TCP/UDP, anonymity.\n"
            "• DefaultProxy: Uses system proxy.\n"
            "• NoProxy: Direct connection."
        )
        self.label_8.installEventFilter(
            ToolTipFilter(self.label_8, 300, ToolTipPosition.TOP)
        )

        self.label_10.setToolTip(
            "• Desktop: Native OpenGL implementation.\n"
            "• Angle: OpenGL over Direct3D.\n"
            "• Software: Software-based rendering.\n"
            "• Auto: Automatic selection based on system."
        )
        self.label_10.installEventFilter(
            ToolTipFilter(self.label_10, 300, ToolTipPosition.TOP)
        )

        self.label_6.setToolTip(
            "• Ctrl + Shift + Space: Play/Pause.\n"
            "• Ctrl + Shift + Right: Skip Next.\n"
            "• Ctrl + Shift + Left: Skip Previous.\n"
            "• Ctrl + Shift + Up: Volume Up.\n"
            "• Ctrl + Shift + Down: Volume Down."
        )
        self.label_6.installEventFilter(
            ToolTipFilter(self.label_6, 300, ToolTipPosition.TOP)
        )

        self.label_5.hide()
        self.label_3.hide()

    def check_settings_dependency(self):
        if not self.SwitchButton_15.isChecked():
            self.checkBox.setEnabled(False)
        else:
            self.checkBox.setEnabled(True)

        self.check_if_settings_changed()

    def restart_app(self):
        msg_box = None

        if self.window.video_state == "VideoPlaying":
            msg_box = MessageBox(
                "Restart Confirmation",
                (
                    "Restarting now will stop the current playback and "
                    "close the application.\n"
                    "Do you want to restart now?"
                ),
                self,
            )
            msg_box.yesButton.setText("Restart")
        if not msg_box or msg_box.exec_():
            self.window.save_settings()
            if self.PrimaryPushButton.isEnabled():
                if not self.save_settings():
                    return

            QProcess.startDetached(sys.executable, sys.argv)
            QApplication.quit()

    def save_settings(self):
        proxy_type = self.ComboBox.currentText()
        proxy_host = self.LineEdit.text().strip()

        port_text_raw = self.LineEdit_2.text()
        port_text = port_text_raw.strip()
        port_is_valid_number = port_text.isdigit()

        proxy_error_message = None

        if proxy_type in ["HttpProxy", "Socks5Proxy"]:
            if not proxy_host:
                proxy_error_message = "Proxy host cannot be empty."
            elif port_is_valid_number and int(port_text) > 65535:
                proxy_error_message = "Proxy port cannot exceed 65535."

        if proxy_error_message:
            self.label_5.setText(proxy_error_message)
            self.label_5.show()

            if not self.PillPushButton.isChecked():
                self.PillPushButton.setChecked(True)
                self.configure_tabs()

            QTimer.singleShot(
                0, lambda: self.ScrollArea.ensureWidgetVisible(self.label_5)
            )
            return False
        else:
            self.label_5.hide()

        tray_error_message = None

        if (
            not QSystemTrayIcon.isSystemTrayAvailable()
            and self.SwitchButton_12.isChecked()
        ):
            tray_error_message = "System tray is not available on this system."

        if tray_error_message:
            self.label_3.setText(tray_error_message)
            self.label_3.show()

            if not self.PillPushButton_4.isChecked():
                self.PillPushButton_4.setChecked(True)
                self.configure_tabs()

            QTimer.singleShot(
                0, lambda: self.ScrollArea.ensureWidgetVisible(self.label_3)
            )
            return False
        else:
            self.label_3.hide()

        self.window.save_last_win_geometry_setting = int(self.SwitchButton.isChecked())
        self.window.open_last_url_at_startup_setting = int(
            self.SwitchButton_4.isChecked()
        )
        self.window.ad_blocker_setting = int(self.SwitchButton_3.isChecked())
        self.window.fullscreen_mode_support_setting = int(
            self.SwitchButton_5.isChecked()
        )
        self.window.support_animated_scrolling_setting = int(
            self.SwitchButton_6.isChecked()
        )
        self.window.save_last_pos_of_mp_setting = int(self.SwitchButton_2.isChecked())
        self.window.save_last_zoom_factor_setting = int(self.SwitchButton_8.isChecked())
        self.window.discord_rpc_setting = int(self.SwitchButton_7.isChecked())
        self.window.tray_icon_setting = int(self.SwitchButton_12.isChecked())
        self.window.proxy_type_setting = proxy_type
        self.window.proxy_host_name_setting = proxy_host
        self.window.proxy_port_setting = (
            int(port_text) if port_is_valid_number else None
        )
        self.window.proxy_login_setting = self.LineEdit_3.text()
        self.window.proxy_password_setting = self.PasswordLineEdit.text()
        self.window.hotkey_playback_control_setting = int(
            self.SwitchButton_14.isChecked()
        )
        self.window.only_audio_mode_setting = int(self.SwitchButton_15.isChecked())
        self.window.opengl_enviroment_setting = self.ComboBox_3.currentText()
        self.window.nonstop_music_setting = int(self.SwitchButton_16.isChecked())
        self.window.block_video_setting = int(self.checkBox.isChecked())

        self.window.settings_.setValue(
            "save_last_win_geometry", self.window.save_last_win_geometry_setting
        )
        self.window.settings_.setValue(
            "open_last_url_at_startup", self.window.open_last_url_at_startup_setting
        )
        self.window.settings_.setValue("ad_blocker", self.window.ad_blocker_setting)
        self.window.settings_.setValue(
            "fullscreen_mode_support", self.window.fullscreen_mode_support_setting
        )
        self.window.settings_.setValue(
            "support_animated_scrolling", self.window.support_animated_scrolling_setting
        )
        self.window.settings_.setValue(
            "save_last_pos_of_mp", self.window.save_last_pos_of_mp_setting
        )
        self.window.settings_.setValue(
            "save_last_zoom_factor", self.window.save_last_zoom_factor_setting
        )
        self.window.settings_.setValue("discord_rpc", self.window.discord_rpc_setting)
        self.window.settings_.setValue("tray_icon", self.window.tray_icon_setting)
        self.window.settings_.setValue("proxy_type", self.window.proxy_type_setting)
        self.window.settings_.setValue(
            "proxy_host_name", self.window.proxy_host_name_setting
        )
        self.window.settings_.setValue("proxy_port", self.window.proxy_port_setting)
        self.window.settings_.setValue("proxy_login", self.window.proxy_login_setting)
        self.window.settings_.setValue(
            "proxy_password", self.window.proxy_password_setting
        )
        self.window.settings_.setValue(
            "hotkey_playback_control", self.window.hotkey_playback_control_setting
        )
        self.window.settings_.setValue(
            "only_audio_mode", self.window.only_audio_mode_setting
        )
        self.window.settings_.setValue(
            "opengl_enviroment", self.window.opengl_enviroment_setting
        )
        self.window.settings_.setValue(
            "nonstop_music", self.window.nonstop_music_setting
        )
        self.window.settings_.setValue("block_video", self.window.block_video_setting)

        self.check_if_settings_changed()
        return True

    def configure_tabs(self):
        self.frame.hide()
        self.frame_2.hide()
        self.frame_3.hide()
        self.frame_4.hide()

        icon_path = self.window.icon_folder + "/plugins.png"

        if self.PillPushButton.isChecked():
            self.frame.show()
            self.ScrollArea.verticalScrollBar().setValue(0)
        elif self.PillPushButton_2.isChecked():
            self.frame_2.show()
        elif self.PillPushButton_3.isChecked():
            self.frame_3.show()
        else:
            self.frame_4.show()
            self.ScrollArea.verticalScrollBar().setValue(0)
            icon_path = self.window.icon_folder + "/plugins-black.png"

        self.PillPushButton_4.setIcon(icon_path)

    def toggle_proxy_config(self):
        proxy_type = self.ComboBox.currentText()
        should_show = proxy_type in ["HttpProxy", "Socks5Proxy"]

        self.BodyLabel_10.setVisible(should_show)
        self.LineEdit.setVisible(should_show)
        self.BodyLabel_14.setVisible(should_show)
        self.LineEdit_2.setVisible(should_show)
        self.BodyLabel_16.setVisible(should_show)
        self.LineEdit_3.setVisible(should_show)
        self.BodyLabel_17.setVisible(should_show)
        self.PasswordLineEdit.setVisible(should_show)

        self.label_5.hide()

    def check_if_settings_changed(self):
        if (
            self.SwitchButton.isChecked() != self.window.save_last_win_geometry_setting
            or self.SwitchButton_4.isChecked()
            != self.window.open_last_url_at_startup_setting
            or self.SwitchButton_3.isChecked() != self.window.ad_blocker_setting
            or self.SwitchButton_5.isChecked()
            != self.window.fullscreen_mode_support_setting
            or self.SwitchButton_6.isChecked()
            != self.window.support_animated_scrolling_setting
            or self.SwitchButton_2.isChecked()
            != self.window.save_last_pos_of_mp_setting
            or self.SwitchButton_8.isChecked()
            != self.window.save_last_zoom_factor_setting
            or self.SwitchButton_7.isChecked() != self.window.discord_rpc_setting
            or self.SwitchButton_12.isChecked() != self.window.tray_icon_setting
            or self.ComboBox.currentText() != self.window.proxy_type_setting
            or self.LineEdit.text() != self.window.proxy_host_name_setting
            or self.LineEdit_2.text()
            != (
                str(self.window.proxy_port_setting)
                if self.window.proxy_port_setting is not None
                else ""
            )
            or self.LineEdit_3.text() != self.window.proxy_login_setting
            or self.PasswordLineEdit.text() != self.window.proxy_password_setting
            or self.SwitchButton_14.isChecked()
            != self.window.hotkey_playback_control_setting
            or self.SwitchButton_15.isChecked() != self.window.only_audio_mode_setting
            or self.ComboBox_3.currentText() != self.window.opengl_enviroment_setting
            or self.SwitchButton_16.isChecked() != self.window.nonstop_music_setting
            or self.checkBox.isChecked() != self.window.block_video_setting
        ):

            self.PrimaryPushButton.setEnabled(True)
            self.PushButton_2.setText("Restart && Save")
        else:
            self.PrimaryPushButton.setEnabled(False)
            self.PushButton_2.setText("Restart")

        self.label_3.hide()

    def closeEvent(self, event):
        self.window.show()
        event.accept()
