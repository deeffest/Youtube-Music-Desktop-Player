# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (LineEdit, ToolButton)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(789, 495)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_frame = QFrame(self.centralwidget)
        self.toolbar_frame.setObjectName(u"toolbar_frame")
        self.toolbar_layout = QHBoxLayout(self.toolbar_frame)
        self.toolbar_layout.setSpacing(6)
        self.toolbar_layout.setObjectName(u"toolbar_layout")
        self.toolbar_layout.setContentsMargins(6, 6, 6, 6)
        self.back_tbutton = ToolButton(self.toolbar_frame)
        self.back_tbutton.setObjectName(u"back_tbutton")
        self.back_tbutton.setEnabled(False)

        self.toolbar_layout.addWidget(self.back_tbutton)

        self.forward_tbutton = ToolButton(self.toolbar_frame)
        self.forward_tbutton.setObjectName(u"forward_tbutton")
        self.forward_tbutton.setEnabled(False)

        self.toolbar_layout.addWidget(self.forward_tbutton)

        self.home_tbutton = ToolButton(self.toolbar_frame)
        self.home_tbutton.setObjectName(u"home_tbutton")

        self.toolbar_layout.addWidget(self.home_tbutton)

        self.reload_tbutton = ToolButton(self.toolbar_frame)
        self.reload_tbutton.setObjectName(u"reload_tbutton")

        self.toolbar_layout.addWidget(self.reload_tbutton)

        self.LineEdit = LineEdit(self.toolbar_frame)
        self.LineEdit.setObjectName(u"LineEdit")
        self.LineEdit.setReadOnly(True)

        self.toolbar_layout.addWidget(self.LineEdit)

        self.download_tbutton = ToolButton(self.toolbar_frame)
        self.download_tbutton.setObjectName(u"download_tbutton")

        self.toolbar_layout.addWidget(self.download_tbutton)

        self.mini_player_tbutton = ToolButton(self.toolbar_frame)
        self.mini_player_tbutton.setObjectName(u"mini_player_tbutton")

        self.toolbar_layout.addWidget(self.mini_player_tbutton)

        self.settings_tbutton = ToolButton(self.toolbar_frame)
        self.settings_tbutton.setObjectName(u"settings_tbutton")

        self.toolbar_layout.addWidget(self.settings_tbutton)


        self.verticalLayout.addWidget(self.toolbar_frame)

        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName(u"main_layout")
        self.verticalSpacer = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.main_layout.addItem(self.verticalSpacer)


        self.verticalLayout.addLayout(self.main_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.back_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Back", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.forward_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Forward", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.home_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Home", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.reload_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Reload", None))
#endif // QT_CONFIG(tooltip)
        self.LineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"https://music.youtube.com/", None))
#if QT_CONFIG(tooltip)
        self.download_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Download", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mini_player_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Mini-Player", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.settings_tbutton.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

