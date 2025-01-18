from typing import TYPE_CHECKING

from PyQt5.QtCore import QTimer
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit
if TYPE_CHECKING:
    from main_window import MainWindow


class InputMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window:"MainWindow" = parent

        self.titleLabel = SubtitleLabel(self)
        self.lineEdit = LineEdit(self)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.returnPressed.connect(self.yesButton.click)
        self.lineEdit.textChanged.connect(self._validateText)
        QTimer.singleShot(0, self._setFocusAndSelectAll)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.lineEdit)

        self.yesButton.setText('OK')
        self.cancelButton.setText('Cancel')

        self.widget.setMinimumWidth(400)
        self.yesButton.setDisabled(True)
        
    def _validateText(self, text):
        self.yesButton.setEnabled(bool(text))
    
    def _setFocusAndSelectAll(self):
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()
