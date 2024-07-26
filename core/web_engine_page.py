import webbrowser

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from qfluentwidgets import MessageBox
from core.input_message_box import InputMessageBox

class WebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if ("music.youtube.com" not in url.toString() and
            "accounts.google.com" not in url.toString() and
            "googlesyndication.com" not in url.toString() and
            "google.com/tools/feedback" not in url.toString() and
            "google.com/recaptcha" not in url.toString()):
            webbrowser.open_new_tab(url.toString())
            return False

        return QWebEnginePage.acceptNavigationRequest(self, url, _type, isMainFrame)

    def javaScriptAlert(self, qurl, text):
        w = MessageBox(f"JavaScript Alert - {qurl.toString()}", text, self.parent())
        w.cancelButton.hide()
        w.exec_()

    def javaScriptConfirm(self, qurl, text):
        w = MessageBox(f"JavaScript Confirm - {qurl.toString()}", text, self.parent())
        return w.exec_() == True

    def javaScriptPrompt(self, qurl, text, text_value):
        w = InputMessageBox(self.parent())
        w.titleLabel.setText(text)
        w.lineEdit.setText(text_value)
        if w.exec_():
            return (True, w.lineEdit.text())
        else:
            return (False, "")
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"js: {level} - {message} - {lineNumber} - {sourceID}")