from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import (
    QWebEnginePage
)

from core.alert_dialog import AlertDlg
from core.confirm_dialog import ConfirmDlg
from core.input_dialog import InputDlg

import webbrowser

class WebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if ("music.youtube.com" not in url.toString() and
            "accounts.google.com" not in url.toString() and
            "googlesyndication.com" not in url.toString()):
            webbrowser.open_new_tab(url.toString())
            return False

        return QWebEnginePage.acceptNavigationRequest(self, url, _type, isMainFrame)

    def javaScriptAlert(self, qurl, text):
        dialog = AlertDlg(
            self.parent().name,
            self.parent().current_dir,
            self.view()
        )
        dialog.setText(text)
        reply = dialog.exec_()

    def javaScriptConfirm(self, qurl, text):
        dialog = ConfirmDlg(
            self.parent().name,
            self.parent().current_dir,
            self.view()
        )
        dialog.setText(text)
        reply = dialog.exec_()
        return reply == True

    def javaScriptPrompt(self, qurl, text, text_value):
        dialog = InputDlg(
            self.parent().name,
            self.parent().current_dir,
            self.view()
        )
        dialog.setText(text)
        dialog.setTextValue(text_value)
        if dialog.exec_():
            return (True, dialog.textValue())
        else:
            return (False, "")