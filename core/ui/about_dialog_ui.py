# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (BodyLabel, PrimaryPushButton, PushButton, SubtitleLabel)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(383, 312)
        Dialog.setMinimumSize(QSize(383, 232))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 9, -1, -1)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(72, 72))
        self.label.setMaximumSize(QSize(72, 72))
        self.label.setPixmap(QPixmap(u"../../resources/icons/icon.ico"))
        self.label.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignTop)


        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 6, 9, 14)
        self.SubtitleLabel = SubtitleLabel(self.frame)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")

        self.verticalLayout_3.addWidget(self.SubtitleLabel)

        self.BodyLabel_2 = BodyLabel(self.frame)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")

        self.verticalLayout_3.addWidget(self.BodyLabel_2)

        self.BodyLabel = BodyLabel(self.frame)
        self.BodyLabel.setObjectName(u"BodyLabel")
        self.BodyLabel.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.BodyLabel)

        self.BodyLabel_3 = BodyLabel(self.frame)
        self.BodyLabel_3.setObjectName(u"BodyLabel_3")

        self.verticalLayout_3.addWidget(self.BodyLabel_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addWidget(self.frame)

        self.ButtonBox = QFrame(Dialog)
        self.ButtonBox.setObjectName(u"ButtonBox")
        self.ButtonBox.setFrameShape(QFrame.StyledPanel)
        self.ButtonBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.ButtonBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 16, 12, 16)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.PushButton = PushButton(self.ButtonBox)
        self.PushButton.setObjectName(u"PushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PushButton.sizePolicy().hasHeightForWidth())
        self.PushButton.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u"../../resources/icons/github.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.PushButton.setIcon(icon)
        self.PushButton.setIconSize(QSize(18, 18))
        self.PushButton.setProperty("hasIcon", True)

        self.horizontalLayout_5.addWidget(self.PushButton)

        self.PrimaryPushButton = PrimaryPushButton(self.ButtonBox)
        self.PrimaryPushButton.setObjectName(u"PrimaryPushButton")
        sizePolicy.setHeightForWidth(self.PrimaryPushButton.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton.setSizePolicy(sizePolicy)
        self.PrimaryPushButton.setMinimumSize(QSize(0, 0))
        self.PrimaryPushButton.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_5.addWidget(self.PrimaryPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.verticalLayout_2.addWidget(self.ButtonBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText("")
        self.SubtitleLabel.setText(QCoreApplication.translate("Dialog", u"Youtube Music Desktop Player", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("Dialog", u"Version: 1.8-beta", None))
        self.BodyLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#d3d3d3;\">Displays Youtube Music site using QWebEngine to make your music listening experience even more convenient. </span></p><p><span style=\" color:#d3d3d3;\">This App is licensed under GNU GPLv3 and the source code is available on Github.</span></p><p><span style=\" color:#d3d3d3;\">Enjoy listening:)</span></p></body></html>", None))
        self.BodyLabel_3.setText(QCoreApplication.translate("Dialog", u"Created with \u2764\ufe0f by deeffest, 2024", None))
        self.PushButton.setText(QCoreApplication.translate("Dialog", u"Visit Github", None))
        self.PrimaryPushButton.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi

