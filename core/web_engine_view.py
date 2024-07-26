from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData

class WebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)

    def contextMenuEvent(self, event):
        context_data = self.page().contextMenuData()            
        flags = context_data.editFlags()

        self.window().copy_action.setEnabled(flags & QWebEngineContextMenuData.CanCopy)
        self.window().paste_action.setEnabled(flags & QWebEngineContextMenuData.CanPaste)

        if self.page().selectedText() or context_data.isContentEditable():
            self.window().edit_menu.exec(event.globalPos())
        else:
            self.window().main_menu.exec(event.globalPos())