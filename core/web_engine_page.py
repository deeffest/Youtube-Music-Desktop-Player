import re
import logging
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

        patterns = [
            r"^https://music\.youtube\.com/.*$",
            r"^https://accounts\.google\..*/.*$",
            r"^https://accounts\.youtube\.com/.*$",
            r"^https://www\.youtube\.com/signin.*action_handle_signin.*$",
            r"^https://www\.google\.com/recaptcha.*$",
            r"^https://consent\.youtube\.com/.*$",
            r"^https://www\.google\.com/tools/feedback/.*$",
        ]

        for pattern in patterns:
            if re.match(pattern, url_str):
                return True

        return False

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
        w.title_label.setText(msg)
        w.line_edit.setText(defaultValue)
        if w.exec_():
            return (True, w.line_edit.text())
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
