import re
import logging
import webbrowser
from typing import TYPE_CHECKING

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from qfluentwidgets import MessageBox

from core.input_message_box import InputMessageBox

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window: "MainWindow" = parent

    def acceptNavigationRequest(self, url, type, isMainFrame):
        url_str = url.toString()

        blocklist_patterns = [
            r"^.*googlesyndication\.com.*$",
            r"^.*googletagmanager\.com.*$",
            r"^.*googleadservices\.com.*$",
            r"^.*doubleclick\.net.*$",
        ]

        whitelist_patterns = [
            r"^https://music\.youtube\.com/.*$",
            r"^https://accounts\.google\..*/.*$",
            r"^https://consent\.youtube\.com/.*$",
            r"^https://accounts\.youtube\.com/.*$",
            r"^https://ogs\.google\.com/.*$",
            r"^https://www\.google\.com/device.*$",
            r"^https://www\.google\.com/recaptcha.*$",
            r"^https://www\.google\.com/tools/feedback/.*$",
            r"^https://www\.youtube\.com/signin.*action_handle_signin.*$",
        ]

        for pattern in blocklist_patterns:
            if re.match(pattern, url_str):
                logging.info(f"🚫 Blocked pattern: {pattern} - URL: {url_str}")
                return False

        for pattern in whitelist_patterns:
            if re.match(pattern, url_str):
                logging.info(f"✅ Allowed pattern: {pattern} - URL: {url_str}")
                return True

        logging.info(f"🌐 Opening URL: {url_str}")
        webbrowser.open_new_tab(url_str)
        return False

    def createWindow(self, type):
        temp_page = QWebEnginePage(self.profile(), self)

        def handle_url_change(url):
            self.window.load_url(url)
            temp_page.deleteLater()

        temp_page.urlChanged.connect(handle_url_change)
        return temp_page

    def javaScriptAlert(self, securityOrigin, msg):
        w = MessageBox(
            f"JavaScript Alert - {securityOrigin.toString()}", msg, self.window
        )
        w.cancelButton.hide()
        w.exec_()

    def javaScriptConfirm(self, securityOrigin, msg):
        w = MessageBox(
            f"JavaScript Confirm - {securityOrigin.toString()}", msg, self.window
        )
        return w.exec_()

    def javaScriptPrompt(self, securityOrigin, msg, defaultValue):
        w = InputMessageBox(self.window)
        w.titleLabel.setText(msg)
        w.lineEdit.setText(defaultValue)
        if w.exec_():
            return (True, w.lineEdit.text())
        else:
            return (False, "")

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if level == QWebEnginePage.InfoMessageLevel:
            logging.info(
                f"JavaScript Console Info: {message} (Level: {level}, "
                f"Line: {lineNumber}, Source: {sourceID})"
            )
        elif level == QWebEnginePage.WarningMessageLevel:
            logging.warning(
                f"JavaScript Console Warning: {message} (Level: {level}, "
                f"Line: {lineNumber}, Source: {sourceID})"
            )
        elif level == QWebEnginePage.ErrorMessageLevel:
            logging.error(
                f"JavaScript Console Error: {message} (Level: {level}, "
                f"Line: {lineNumber}, Source: {sourceID})"
            )
