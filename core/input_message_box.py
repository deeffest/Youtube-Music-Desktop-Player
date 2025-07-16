from PyQt5.QtCore import QTimer
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit


class InputMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title_label = SubtitleLabel(self)
        self.line_edit = LineEdit(self)
        self.line_edit.setClearButtonEnabled(True)

        self.line_edit.returnPressed.connect(self.yesButton.click)
        self.line_edit.textChanged.connect(self._validate_text)

        QTimer.singleShot(0, self._focus_input)

        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.line_edit)

        self.yesButton.setText("OK")
        self.cancelButton.setText("Cancel")

        self.widget.setMinimumWidth(400)
        self.yesButton.setDisabled(True)

    def _validate_text(self, text):
        self.yesButton.setEnabled(bool(text))

    def _focus_input(self):
        self.line_edit.setFocus()
        self.line_edit.selectAll()
