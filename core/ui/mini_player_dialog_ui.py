# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mini_player_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, StrongBodyLabel, ToolButton, TransparentToolButton)

class Ui_MiniPlayerDialog(object):
    def setupUi(self, MiniPlayerDialog):
        if not MiniPlayerDialog.objectName():
            MiniPlayerDialog.setObjectName(u"MiniPlayerDialog")
        MiniPlayerDialog.resize(360, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MiniPlayerDialog.sizePolicy().hasHeightForWidth())
        MiniPlayerDialog.setSizePolicy(sizePolicy)
        MiniPlayerDialog.setMinimumSize(QSize(360, 150))
        MiniPlayerDialog.setMaximumSize(QSize(360, 150))
        MiniPlayerDialog.setMouseTracking(True)
        MiniPlayerDialog.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(MiniPlayerDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 18, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(16, -1, 16, 6)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.title_label = StrongBodyLabel(MiniPlayerDialog)
        self.title_label.setObjectName(u"title_label")

        self.verticalLayout_2.addWidget(self.title_label)

        self.author_label = BodyLabel(MiniPlayerDialog)
        self.author_label.setObjectName(u"author_label")
        self.author_label.setStyleSheet(u"QLabel {\n"
"	color: lightgray;\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_2.addWidget(self.author_label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.thumbnail_label = QLabel(MiniPlayerDialog)
        self.thumbnail_label.setObjectName(u"thumbnail_label")
        self.thumbnail_label.setMinimumSize(QSize(60, 60))
        self.thumbnail_label.setMaximumSize(QSize(60, 60))
        self.thumbnail_label.setScaledContents(True)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.thumbnail_label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(30)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 3, 4, 18)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.previous_button = TransparentToolButton(MiniPlayerDialog)
        self.previous_button.setObjectName(u"previous_button")
        self.previous_button.setMinimumSize(QSize(40, 40))
        self.previous_button.setMaximumSize(QSize(40, 40))
        icon = QIcon()
        icon.addFile(u"../../resources/icons/previous-filled.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.previous_button.setIcon(icon)
        self.previous_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.previous_button)

        self.play_pause_button = TransparentToolButton(MiniPlayerDialog)
        self.play_pause_button.setObjectName(u"play_pause_button")
        self.play_pause_button.setMinimumSize(QSize(40, 40))
        self.play_pause_button.setMaximumSize(QSize(40, 40))
        icon1 = QIcon()
        icon1.addFile(u"../../resources/icons/play-filled.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.play_pause_button.setIcon(icon1)
        self.play_pause_button.setIconSize(QSize(22, 22))

        self.horizontalLayout_3.addWidget(self.play_pause_button)

        self.next_button = TransparentToolButton(MiniPlayerDialog)
        self.next_button.setObjectName(u"next_button")
        self.next_button.setMinimumSize(QSize(40, 40))
        self.next_button.setMaximumSize(QSize(40, 40))
        icon2 = QIcon()
        icon2.addFile(u"../../resources/icons/next-filled.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.next_button.setIcon(icon2)
        self.next_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.next_button)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(MiniPlayerDialog)

        QMetaObject.connectSlotsByName(MiniPlayerDialog)
    # setupUi

    def retranslateUi(self, MiniPlayerDialog):
        MiniPlayerDialog.setWindowTitle(QCoreApplication.translate("MiniPlayerDialog", u"Dialog", None))
        self.title_label.setText("")
        self.author_label.setText("")
        self.thumbnail_label.setText("")
#if QT_CONFIG(shortcut)
        self.previous_button.setShortcut(QCoreApplication.translate("MiniPlayerDialog", u"Left", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(shortcut)
        self.play_pause_button.setShortcut(QCoreApplication.translate("MiniPlayerDialog", u"Space", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(shortcut)
        self.next_button.setShortcut(QCoreApplication.translate("MiniPlayerDialog", u"Right", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

