import sys
import pywinstyles

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QProcess
from PyQt5.uic import loadUi
from qfluentwidgets import MessageBox

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = parent

        self.load_ui()
        self.set_connect()
        self.set_icons()
        self.configure_tabs()
        self.setup_settings()

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
        self.SwitchButton_9.setChecked(self.window.close_cmd_after_downloading_setting)

    def set_icons(self):
        self.PillPushButton_4.setIcon(self.window.icon_folder+"/plugins.png")

    def set_connect(self):
        self.PillPushButton.clicked.connect(self.configure_tabs)
        self.PillPushButton_2.clicked.connect(self.configure_tabs)
        self.PillPushButton_3.clicked.connect(self.configure_tabs)
        self.PillPushButton_4.clicked.connect(self.configure_tabs)
        self.PillPushButton_5.clicked.connect(self.configure_tabs)
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
        self.window.close_cmd_after_downloading_setting = int(self.SwitchButton_9.isChecked())

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
        self.window.settings_.setValue("close_cmd_after_downloading", self.window.close_cmd_after_downloading_setting)

        self.close()

        w = MessageBox(
            "Restart Confirmation",
            (
                "Restarting will close the current session and re-open the application with the new settings.\n"
                "Would you like to restart now or later?"
            ),
            self.window
        )
        w.yesButton.setText("Restart Now")
        w.cancelButton.setText("Restart Later")
        if w.exec_() == True:
            self.window.save_settings()
            QApplication.quit()
            QProcess.startDetached(sys.executable, sys.argv)

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
            
        elif self.PillPushButton_5.isChecked():
            self.frame_5.show()

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