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

from qfluentwidgets import (BodyLabel, CaptionLabel, HyperlinkButton, PrimaryPushButton,
    PushButton, TitleLabel)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(431, 306)
        Dialog.setStyleSheet(u"background-color: rgb(39,39,39);")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 9, 0, 0)
        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(12, 0, 12, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(64, 64))
        self.label.setMaximumSize(QSize(64, 64))
        self.label.setPixmap(QPixmap(u"../../resources/icons/icon.ico"))
        self.label.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.label)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.TitleLabel = TitleLabel(self.frame_3)
        self.TitleLabel.setObjectName(u"TitleLabel")

        self.verticalLayout_3.addWidget(self.TitleLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.BodyLabel_3 = BodyLabel(self.frame_3)
        self.BodyLabel_3.setObjectName(u"BodyLabel_3")

        self.horizontalLayout_2.addWidget(self.BodyLabel_3)

        self.BodyLabel_2 = BodyLabel(self.frame_3)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")
        self.BodyLabel_2.setStyleSheet(u"color: white;")

        self.horizontalLayout_2.addWidget(self.BodyLabel_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.BodyLabel = BodyLabel(self.frame_3)
        self.BodyLabel.setObjectName(u"BodyLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BodyLabel.sizePolicy().hasHeightForWidth())
        self.BodyLabel.setSizePolicy(sizePolicy)
        self.BodyLabel.setMinimumSize(QSize(0, 110))
        self.BodyLabel.setMaximumSize(QSize(16777215, 110))
        self.BodyLabel.setContextMenuPolicy(Qt.NoContextMenu)
        self.BodyLabel.setStyleSheet(u"color: gray;")
        self.BodyLabel.setScaledContents(False)
        self.BodyLabel.setWordWrap(True)
        self.BodyLabel.setOpenExternalLinks(True)

        self.verticalLayout_5.addWidget(self.BodyLabel)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.CaptionLabel = CaptionLabel(self.frame_3)
        self.CaptionLabel.setObjectName(u"CaptionLabel")

        self.horizontalLayout_4.addWidget(self.CaptionLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.HyperlinkButton = HyperlinkButton(self.frame_3)
        self.HyperlinkButton.setObjectName(u"HyperlinkButton")
        self.HyperlinkButton.setUrl(QUrl(u"https://deeffest.pythonanywhere.com"))

        self.horizontalLayout_4.addWidget(self.HyperlinkButton)

        self.HyperlinkButton_2 = HyperlinkButton(self.frame_3)
        self.HyperlinkButton_2.setObjectName(u"HyperlinkButton_2")
        self.HyperlinkButton_2.setUrl(QUrl(u"https://donationalerts.com/r/deeffest"))

        self.horizontalLayout_4.addWidget(self.HyperlinkButton_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(32,32,32);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 16, 9, 16)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.PushButton_2 = PushButton(self.frame)
        self.PushButton_2.setObjectName(u"PushButton_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PushButton_2.sizePolicy().hasHeightForWidth())
        self.PushButton_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.PushButton_2)

        self.PushButton = PrimaryPushButton(self.frame)
        self.PushButton.setObjectName(u"PushButton")
        sizePolicy1.setHeightForWidth(self.PushButton.sizePolicy().hasHeightForWidth())
        self.PushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.PushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText("")
        self.TitleLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:18pt;\">Youtube Music Desktop Player</span></p></body></html>", None))
        self.BodyLabel_3.setText(QCoreApplication.translate("Dialog", u"Current app version:", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("Dialog", u"1.1.2", None))
        self.BodyLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#d3d3d3;\">Displays Youtube Music site using QWebEngine to make your music listening experience even more convenient.</span></p><p><span style=\" font-size:11pt; color:#d3d3d3;\">Created with </span><a href=\"https://www.riverbankcomputing.com/software/pyqt/intro\"><span style=\" text-decoration: underline; color:#d3d3d3;\">PyQt5</span></a><span style=\" font-size:11pt; color:#d3d3d3;\"> + </span><a href=\"https://github.com/zhiyiYo/PyQt-Fluent-Widgets\"><span style=\" text-decoration: underline; color:#d3d3d3;\">PyQt-Fluent-Widgets</span></a><span style=\" font-size:11pt; color:#d3d3d3;\"> and distributed under the </span><a href=\"https://www.gnu.org/licenses/gpl-3.0.html\"><span style=\" text-decoration: underline; color:#d3d3d3;\">GNU GPL v3</span></a><span style=\" font-size:11pt; color:#d3d3d3;\"> license, source code is available on </span><a href=\"https://github.com/deeffest/Youtube-Music-Desktop-Player\"><span style=\" text-decoration: underline; color:#d3d3"
                        "d3;\">GitHub</span></a><span style=\" font-size:11pt; color:#d3d3d3;\">. </span></p></body></html>", None))
        self.CaptionLabel.setText(QCoreApplication.translate("Dialog", u"Created with \u2764 by deeffest, 2024", None))
        self.HyperlinkButton.setText(QCoreApplication.translate("Dialog", u"My Website", None))
        self.HyperlinkButton_2.setText(QCoreApplication.translate("Dialog", u"Donationalerts", None))
        self.PushButton_2.setText(QCoreApplication.translate("Dialog", u"What's new", None))
        self.PushButton.setText(QCoreApplication.translate("Dialog", u"OK", None))
    # retranslateUi

