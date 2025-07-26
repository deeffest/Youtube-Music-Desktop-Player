from qfluentwidgets import MessageBoxBase, SubtitleLabel, TextEdit


class TextViewDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title_label = SubtitleLabel(self)
        self.text_edit = TextEdit(self)
        self.text_edit.setReadOnly(True)

        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.text_edit)

        self.widget.setMinimumWidth(400)
        self.widget.setMinimumHeight(550)
