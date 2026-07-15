from typing import TYPE_CHECKING

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineContextMenuData
from qfluentwidgets5 import RoundMenu

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.window: "MainWindow" = parent

    def contextMenuEvent(self, event):
        context_data = self.page().contextMenuData()
        flags = context_data.editFlags()
 
        menu = RoundMenu()
        has_content = False
 
        if context_data.isContentEditable():
            if flags & QWebEngineContextMenuData.CanCut:
                menu.addAction(self.window.cut_action)
                has_content = True
            if flags & QWebEngineContextMenuData.CanCopy:
                menu.addAction(self.window.copy_action)
                has_content = True
            if flags & QWebEngineContextMenuData.CanPaste:
                menu.addAction(self.window.paste_action)
                has_content = True
            if flags & QWebEngineContextMenuData.CanUndo:
                menu.addAction(self.window.cancel_action)
                has_content = True
            if flags & QWebEngineContextMenuData.CanSelectAll:
                menu.addAction(self.window.select_all_action)
                has_content = True
 
        elif self.page().selectedText():
            menu.addAction(self.window.copy_action)
            has_content = True
 
        if has_content:
            menu.exec(event.globalPos())
        else:
            self.window.main_menu.exec(event.globalPos())
 
        event.accept()
