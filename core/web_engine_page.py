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
        self.window:"MainWindow" = parent

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if ("music.youtube.com" not in url.toString() and
            "accounts.google.com" not in url.toString() and
            "googlesyndication.com" not in url.toString() and
            "google.com/tools/feedback" not in url.toString() and
            "consent.youtube.com" not in url.toString() and
            "google.com/device" not in url.toString() and
            "google.com/recaptcha" not in url.toString()):
            webbrowser.open_new_tab(url.toString())
            return False

        return QWebEnginePage.acceptNavigationRequest(self, url, _type, isMainFrame)
    
    def createWindow(self, type):
        temp_page = QWebEnginePage(self.profile(), self)
        
        def handle_url_change(url):
            webbrowser.open_new_tab(url.toString())
            temp_page.deleteLater()
        
        temp_page.urlChanged.connect(handle_url_change)
        return temp_page

    def javaScriptAlert(self, qurl, text):
        w = MessageBox(f"JavaScript Alert - {qurl.toString()}", text, self.window)
        w.cancelButton.hide()
        w.exec_()

    def javaScriptConfirm(self, qurl, text):
        w = MessageBox(f"JavaScript Confirm - {qurl.toString()}", text, self.window)
        return w.exec_() == True

    def javaScriptPrompt(self, qurl, text, text_value):
        w = InputMessageBox(self.window)
        w.titleLabel.setText(text)
        w.lineEdit.setText(text_value)
        if w.exec_():
            return (True, w.lineEdit.text())
        else:
            return (False, "")
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if level == QWebEnginePage.ErrorMessageLevel:
            logging.error(f"JavaScript Console Error: {message} (Level: {level}, Line: {lineNumber}, Source: {sourceID})")
