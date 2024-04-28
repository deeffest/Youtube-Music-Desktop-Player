from qfluentwidgets import MessageBoxBase, SubtitleLabel, \
    LineEdit

class InputMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self)
        self.lineEdit = LineEdit(self)

        self.lineEdit.setClearButtonEnabled(True)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.lineEdit)

        self.yesButton.setText('OK')
        self.cancelButton.setText('Cancel')

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.lineEdit.textChanged.connect(self._validateText)

    def _validateText(self, text):
        self.yesButton.setEnabled(bool(text))