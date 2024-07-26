# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'options_dialog.ui'
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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CaptionLabel, ComboBox, PillPushButton,
    PrimaryPushButton, PushButton, SwitchButton, ToggleButton)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 270)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(500, 270))
        Dialog.setStyleSheet(u"QDialog {\n"
"	background-color: rgb(39,39,39);\n"
"}")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalFrame_2 = QFrame(Dialog)
        self.verticalFrame_2.setObjectName(u"verticalFrame_2")
        self.verticalFrame_2.setStyleSheet(u"background-color: rgb(28, 28, 28);")
        self.verticalLayout_5 = QVBoxLayout(self.verticalFrame_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.PillPushButton = PillPushButton(self.verticalFrame_2)
        self.PillPushButton.setObjectName(u"PillPushButton")
        self.PillPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.PillPushButton)

        self.PillPushButton_2 = PillPushButton(self.verticalFrame_2)
        self.PillPushButton_2.setObjectName(u"PillPushButton_2")

        self.verticalLayout_5.addWidget(self.PillPushButton_2)

        self.PillPushButton_3 = PillPushButton(self.verticalFrame_2)
        self.PillPushButton_3.setObjectName(u"PillPushButton_3")

        self.verticalLayout_5.addWidget(self.PillPushButton_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addWidget(self.verticalFrame_2)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.BodyLabel = BodyLabel(self.frame_3)
        self.BodyLabel.setObjectName(u"BodyLabel")

        self.horizontalLayout_3.addWidget(self.BodyLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.SwitchButton = SwitchButton(self.frame_3)
        self.SwitchButton.setObjectName(u"SwitchButton")
        self.SwitchButton.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_3.addWidget(self.SwitchButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.BodyLabel_8 = BodyLabel(self.frame_3)
        self.BodyLabel_8.setObjectName(u"BodyLabel_8")

        self.horizontalLayout_16.addWidget(self.BodyLabel_8)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_8)

        self.SwitchButton_6 = SwitchButton(self.frame_3)
        self.SwitchButton_6.setObjectName(u"SwitchButton_6")
        self.SwitchButton_6.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_16.addWidget(self.SwitchButton_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.BodyLabel_4 = BodyLabel(self.frame_3)
        self.BodyLabel_4.setObjectName(u"BodyLabel_4")

        self.horizontalLayout_7.addWidget(self.BodyLabel_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.SwitchButton_4 = SwitchButton(self.frame_3)
        self.SwitchButton_4.setObjectName(u"SwitchButton_4")
        self.SwitchButton_4.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_7.addWidget(self.SwitchButton_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.BodyLabel_2 = BodyLabel(self.frame_3)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")
        self.BodyLabel_2.setWordWrap(False)

        self.horizontalLayout_4.addWidget(self.BodyLabel_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.SwitchButton_2 = SwitchButton(self.frame_3)
        self.SwitchButton_2.setObjectName(u"SwitchButton_2")
        self.SwitchButton_2.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_4.addWidget(self.SwitchButton_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.BodyLabel_6 = BodyLabel(self.frame_3)
        self.BodyLabel_6.setObjectName(u"BodyLabel_6")

        self.horizontalLayout_8.addWidget(self.BodyLabel_6)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_9)

        self.SwitchButton_7 = SwitchButton(self.frame_3)
        self.SwitchButton_7.setObjectName(u"SwitchButton_7")
        self.SwitchButton_7.setFocusPolicy(Qt.NoFocus)
        self.SwitchButton_7.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_8.addWidget(self.SwitchButton_7)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.BodyLabel_3 = BodyLabel(self.frame_4)
        self.BodyLabel_3.setObjectName(u"BodyLabel_3")

        self.horizontalLayout_6.addWidget(self.BodyLabel_3)

        self.horizontalSpacer_3 = QSpacerItem(281, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.SwitchButton_3 = SwitchButton(self.frame_4)
        self.SwitchButton_3.setObjectName(u"SwitchButton_3")
        self.SwitchButton_3.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_6.addWidget(self.SwitchButton_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.BodyLabel_7 = BodyLabel(self.frame_4)
        self.BodyLabel_7.setObjectName(u"BodyLabel_7")

        self.horizontalLayout_15.addWidget(self.BodyLabel_7)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_7)

        self.SwitchButton_5 = SwitchButton(self.frame_4)
        self.SwitchButton_5.setObjectName(u"SwitchButton_5")
        self.SwitchButton_5.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_15.addWidget(self.SwitchButton_5)


        self.verticalLayout_7.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.BodyLabel_9 = BodyLabel(self.frame_4)
        self.BodyLabel_9.setObjectName(u"BodyLabel_9")

        self.horizontalLayout_9.addWidget(self.BodyLabel_9)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_10)

        self.PushButton_3 = PushButton(self.frame_4)
        self.PushButton_3.setObjectName(u"PushButton_3")

        self.horizontalLayout_9.addWidget(self.PushButton_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.CaptionLabel = CaptionLabel(self.frame_4)
        self.CaptionLabel.setObjectName(u"CaptionLabel")
        self.CaptionLabel.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.CaptionLabel)


        self.verticalLayout_3.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.BodyLabel_5 = BodyLabel(self.frame_5)
        self.BodyLabel_5.setObjectName(u"BodyLabel_5")

        self.horizontalLayout_5.addWidget(self.BodyLabel_5)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.ComboBox = ComboBox(self.frame_5)
        self.ComboBox.setObjectName(u"ComboBox")

        self.horizontalLayout_5.addWidget(self.ComboBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addWidget(self.frame_5)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

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
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.PushButton = PrimaryPushButton(self.frame)
        self.PushButton.setObjectName(u"PushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.PushButton.sizePolicy().hasHeightForWidth())
        self.PushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.PushButton)

        self.PushButton_2 = PushButton(self.frame)
        self.PushButton_2.setObjectName(u"PushButton_2")
        sizePolicy2.setHeightForWidth(self.PushButton_2.sizePolicy().hasHeightForWidth())
        self.PushButton_2.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.PushButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.PillPushButton.setText(QCoreApplication.translate("Dialog", u"Main", None))
        self.PillPushButton_2.setText(QCoreApplication.translate("Dialog", u"Web Engine", None))
        self.PillPushButton_3.setText(QCoreApplication.translate("Dialog", u"Mini-Player", None))
        self.BodyLabel.setText(QCoreApplication.translate("Dialog", u"Save last Window size:", None))
        self.BodyLabel_8.setText(QCoreApplication.translate("Dialog", u"Open last URL at startup:", None))
        self.BodyLabel_4.setText(QCoreApplication.translate("Dialog", u"Check for Updates at startup:", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("Dialog", u"System Tray app icon:", None))
        self.BodyLabel_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:11pt; color:#ff0000; vertical-align:super;\">NEW</span><span style=\" font-size:11pt;\"> Discord Integration:</span></p></body></html>", None))
        self.BodyLabel_3.setText(QCoreApplication.translate("Dialog", u"Support for animated scrolling:", None))
        self.BodyLabel_7.setText(QCoreApplication.translate("Dialog", u"Support full screen mode:", None))
        self.BodyLabel_9.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:11pt; color:#ff0000; vertical-align:super;\">NEW</span><span style=\" font-size:11pt;\"> Default Page Zoom Factor:</span></p></body></html>", None))
        self.PushButton_3.setText(QCoreApplication.translate("Dialog", u"Set", None))
        self.CaptionLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:9pt; color:#cccccc;\">You can change the zoom factor by holding CTRL and scrolling the mouse wheel.</span></p></body></html>", None))
        self.BodyLabel_5.setText(QCoreApplication.translate("Dialog", u"Mini-player opening location:", None))
        self.PushButton.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.PushButton_2.setText(QCoreApplication.translate("Dialog", u"Cancel changes", None))
    # retranslateUi

