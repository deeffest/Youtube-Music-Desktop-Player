from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit


class InputMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title_label = SubtitleLabel(self)
        self.line_edit = LineEdit(self)
        self.line_edit.setClearButtonEnabled(True)

        self.line_edit.returnPressed.connect(self.yesButton.click)
        self.line_edit.textChanged.connect(self.on_text_changed)

        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.line_edit)

        self.yesButton.setText("OK")
        self.cancelButton.setText("Cancel")

        self.widget.setMinimumWidth(400)
        self.yesButton.setDisabled(True)

    def on_text_changed(self, text):
        self.yesButton.setEnabled(bool(text))

    def showEvent(self, event):
        super().showEvent(event)
        self.line_edit.setFocus()
        self.line_edit.selectAll()
