# coding:utf-8
from typing import Union
from PyQt5 import QtGui

from PyQt5.QtCore import Qt, QSize, QRectF, QEvent
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsDropShadowEffect

from ..common.icon import FluentIconBase, drawIcon, toQIcon
from ..common.style_sheet import isDarkTheme, FluentStyleSheet
from ..components.widgets import IconWidget



class SplashScreen(QWidget):
    """ Splash screen """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None, enableShadow=True):
        super().__init__(parent=parent)
        self._icon = icon
        self._iconSize = QSize(96, 96)

        self.iconWidget = IconWidget(icon, self)
        self.shadowEffect = QGraphicsDropShadowEffect(self)

        self.iconWidget.setFixedSize(self._iconSize)
        self.shadowEffect.setColor(QColor(0, 0, 0, 50))
        self.shadowEffect.setBlurRadius(15)
        self.shadowEffect.setOffset(0, 4)

        if enableShadow:
            self.iconWidget.setGraphicsEffect(self.shadowEffect)

        if parent:
            parent.installEventFilter(self)

    def setIcon(self, icon: Union[str, QIcon, FluentIconBase]):
        self._icon = icon
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setIconSize(self, size: QSize):
        self._iconSize = size
        self.iconWidget.setFixedSize(size)
        self.update()

    def iconSize(self):
        return self._iconSize

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() == QEvent.Resize:
                self.resize(e.size())
            elif e.type() == QEvent.ChildAdded:
                self.raise_()

        return super().eventFilter(obj, e)

    def resizeEvent(self, e):
        iw, ih = self.iconSize().width(), self.iconSize().height()
        self.iconWidget.move(self.width()//2 - iw//2, self.height()//2 - ih//2)

    def finish(self):
        """ close splash screen """
        self.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        # draw background
        c = 32
        painter.setBrush(QColor(c, c, c))
        painter.drawRect(self.rect())
