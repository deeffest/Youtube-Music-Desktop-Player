from typing import TYPE_CHECKING

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineContextMenuRequest
from qfluentwidgets6 import RoundMenu

if TYPE_CHECKING:
    from core.main_window import MainWindow


class WebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.window: "MainWindow" = parent

    def contextMenuEvent(self, event):
        request = self.lastContextMenuRequest()
        flags = request.editFlags()
        EditFlag = QWebEngineContextMenuRequest.EditFlag

        menu = RoundMenu()
        has_content = False

        if request.isContentEditable():
            if flags & EditFlag.CanCut:
                menu.addAction(self.window.cut_action)
                has_content = True
            if flags & EditFlag.CanCopy:
                menu.addAction(self.window.copy_action)
                has_content = True
            if flags & EditFlag.CanPaste:
                menu.addAction(self.window.paste_action)
                has_content = True
            if flags & EditFlag.CanUndo:
                menu.addAction(self.window.cancel_action)
                has_content = True
            if flags & EditFlag.CanSelectAll:
                menu.addAction(self.window.select_all_action)
                has_content = True

        elif request.selectedText():
            menu.addAction(self.window.copy_action)
            has_content = True

        if has_content:
            menu.exec(event.globalPos())
        else:
            self.window.main_menu.exec(event.globalPos())

        request.setAccepted(True)
