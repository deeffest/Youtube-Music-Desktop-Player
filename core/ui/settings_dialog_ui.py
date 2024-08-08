# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
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

from qfluentwidgets import (BodyLabel, HorizontalSeparator, LineEdit, PillPushButton,
    PrimaryPushButton, PushButton, ScrollArea, StrongBodyLabel,
    SwitchButton, ToggleButton)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(530, 300)
        Dialog.setMinimumSize(QSize(530, 300))
        self.verticalLayout_6 = QVBoxLayout(Dialog)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.SideBar = QFrame(Dialog)
        self.SideBar.setObjectName(u"SideBar")
        self.verticalLayout = QVBoxLayout(self.SideBar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.PillPushButton = PillPushButton(self.SideBar)
        self.PillPushButton.setObjectName(u"PillPushButton")
        self.PillPushButton.setChecked(True)
        self.PillPushButton.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.PillPushButton)

        self.PillPushButton_2 = PillPushButton(self.SideBar)
        self.PillPushButton_2.setObjectName(u"PillPushButton_2")
        self.PillPushButton_2.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.PillPushButton_2)

        self.PillPushButton_3 = PillPushButton(self.SideBar)
        self.PillPushButton_3.setObjectName(u"PillPushButton_3")
        self.PillPushButton_3.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.PillPushButton_3)

        self.HorizontalSeparator = HorizontalSeparator(self.SideBar)
        self.HorizontalSeparator.setObjectName(u"HorizontalSeparator")

        self.verticalLayout.addWidget(self.HorizontalSeparator)

        self.PillPushButton_4 = PillPushButton(self.SideBar)
        self.PillPushButton_4.setObjectName(u"PillPushButton_4")
        self.PillPushButton_4.setAutoExclusive(True)
        self.PillPushButton_4.setProperty("hasIcon", True)

        self.verticalLayout.addWidget(self.PillPushButton_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addWidget(self.SideBar)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.ScrollArea = ScrollArea(Dialog)
        self.ScrollArea.setObjectName(u"ScrollArea")
        self.ScrollArea.setFrameShape(QFrame.NoFrame)
        self.ScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 390, 860))
        self.verticalLayout_21 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.SettingBox = QFrame(self.frame)
        self.SettingBox.setObjectName(u"SettingBox")
        self.SettingBox.setFrameShape(QFrame.NoFrame)
        self.SettingBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.SettingBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.BodyLabel = BodyLabel(self.SettingBox)
        self.BodyLabel.setObjectName(u"BodyLabel")

        self.horizontalLayout.addWidget(self.BodyLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.SwitchButton = SwitchButton(self.SettingBox)
        self.SwitchButton.setObjectName(u"SwitchButton")
        self.SwitchButton.setLayoutDirection(Qt.RightToLeft)
        self.SwitchButton.setChecked(False)

        self.horizontalLayout.addWidget(self.SwitchButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.BodyLabel_4 = BodyLabel(self.SettingBox)
        self.BodyLabel_4.setObjectName(u"BodyLabel_4")
        self.BodyLabel_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.BodyLabel_4)


        self.verticalLayout_10.addWidget(self.SettingBox)

        self.SettingBox2 = QFrame(self.frame)
        self.SettingBox2.setObjectName(u"SettingBox2")
        self.SettingBox2.setFrameShape(QFrame.StyledPanel)
        self.SettingBox2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.SettingBox2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.BodyLabel_7 = BodyLabel(self.SettingBox2)
        self.BodyLabel_7.setObjectName(u"BodyLabel_7")

        self.horizontalLayout_6.addWidget(self.BodyLabel_7)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.SwitchButton_4 = SwitchButton(self.SettingBox2)
        self.SwitchButton_4.setObjectName(u"SwitchButton_4")
        self.SwitchButton_4.setLayoutDirection(Qt.RightToLeft)
        self.SwitchButton_4.setChecked(False)

        self.horizontalLayout_6.addWidget(self.SwitchButton_4)


        self.verticalLayout_14.addLayout(self.horizontalLayout_6)

        self.BodyLabel_8 = BodyLabel(self.SettingBox2)
        self.BodyLabel_8.setObjectName(u"BodyLabel_8")
        self.BodyLabel_8.setWordWrap(True)

        self.verticalLayout_14.addWidget(self.BodyLabel_8)


        self.verticalLayout_10.addWidget(self.SettingBox2)


        self.verticalLayout_21.addWidget(self.frame)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 16, 0)
        self.SettingBox3 = QFrame(self.frame_2)
        self.SettingBox3.setObjectName(u"SettingBox3")
        self.SettingBox3.setFrameShape(QFrame.StyledPanel)
        self.SettingBox3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.SettingBox3)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.BodyLabel_9 = BodyLabel(self.SettingBox3)
        self.BodyLabel_9.setObjectName(u"BodyLabel_9")

        self.horizontalLayout_7.addWidget(self.BodyLabel_9)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.SwitchButton_5 = SwitchButton(self.SettingBox3)
        self.SwitchButton_5.setObjectName(u"SwitchButton_5")
        self.SwitchButton_5.setLayoutDirection(Qt.RightToLeft)
        self.SwitchButton_5.setChecked(False)

        self.horizontalLayout_7.addWidget(self.SwitchButton_5)


        self.verticalLayout_13.addLayout(self.horizontalLayout_7)


        self.verticalLayout_12.addWidget(self.SettingBox3)

        self.SettingBox4 = QFrame(self.frame_2)
        self.SettingBox4.setObjectName(u"SettingBox4")
        self.SettingBox4.setFrameShape(QFrame.StyledPanel)
        self.SettingBox4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.SettingBox4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.BodyLabel_11 = BodyLabel(self.SettingBox4)
        self.BodyLabel_11.setObjectName(u"BodyLabel_11")

        self.horizontalLayout_8.addWidget(self.BodyLabel_11)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.SwitchButton_6 = SwitchButton(self.SettingBox4)
        self.SwitchButton_6.setObjectName(u"SwitchButton_6")
        self.SwitchButton_6.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_8.addWidget(self.SwitchButton_6)


        self.verticalLayout_11.addLayout(self.horizontalLayout_8)


        self.verticalLayout_12.addWidget(self.SettingBox4)

        self.SettingBox8 = QFrame(self.frame_2)
        self.SettingBox8.setObjectName(u"SettingBox8")
        self.SettingBox8.setFrameShape(QFrame.StyledPanel)
        self.SettingBox8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.SettingBox8)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.BodyLabel_13 = BodyLabel(self.SettingBox8)
        self.BodyLabel_13.setObjectName(u"BodyLabel_13")

        self.horizontalLayout_10.addWidget(self.BodyLabel_13)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_9)

        self.SwitchButton_8 = SwitchButton(self.SettingBox8)
        self.SwitchButton_8.setObjectName(u"SwitchButton_8")
        self.SwitchButton_8.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_10.addWidget(self.SwitchButton_8)


        self.verticalLayout_17.addLayout(self.horizontalLayout_10)

        self.BodyLabel_22 = BodyLabel(self.SettingBox8)
        self.BodyLabel_22.setObjectName(u"BodyLabel_22")
        self.BodyLabel_22.setWordWrap(True)

        self.verticalLayout_17.addWidget(self.BodyLabel_22)


        self.verticalLayout_12.addWidget(self.SettingBox8)

        self.SettingBox11 = QFrame(self.frame_2)
        self.SettingBox11.setObjectName(u"SettingBox11")
        self.SettingBox11.setFrameShape(QFrame.StyledPanel)
        self.SettingBox11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.SettingBox11)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.BodyLabel_5 = BodyLabel(self.SettingBox11)
        self.BodyLabel_5.setObjectName(u"BodyLabel_5")

        self.horizontalLayout_11.addWidget(self.BodyLabel_5)

        self.StrongBodyLabel = StrongBodyLabel(self.SettingBox11)
        self.StrongBodyLabel.setObjectName(u"StrongBodyLabel")

        self.horizontalLayout_11.addWidget(self.StrongBodyLabel)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_10)

        self.SwitchButton_9 = SwitchButton(self.SettingBox11)
        self.SwitchButton_9.setObjectName(u"SwitchButton_9")
        self.SwitchButton_9.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_11.addWidget(self.SwitchButton_9)


        self.verticalLayout_8.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.BodyLabel_10 = BodyLabel(self.SettingBox11)
        self.BodyLabel_10.setObjectName(u"BodyLabel_10")

        self.horizontalLayout_12.addWidget(self.BodyLabel_10)

        self.LineEdit = LineEdit(self.SettingBox11)
        self.LineEdit.setObjectName(u"LineEdit")
        self.LineEdit.setClearButtonEnabled(False)

        self.horizontalLayout_12.addWidget(self.LineEdit)

        self.BodyLabel_14 = BodyLabel(self.SettingBox11)
        self.BodyLabel_14.setObjectName(u"BodyLabel_14")

        self.horizontalLayout_12.addWidget(self.BodyLabel_14)

        self.LineEdit_2 = LineEdit(self.SettingBox11)
        self.LineEdit_2.setObjectName(u"LineEdit_2")
        self.LineEdit_2.setClearButtonEnabled(False)

        self.horizontalLayout_12.addWidget(self.LineEdit_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout_12)

        self.BodyLabel_15 = BodyLabel(self.SettingBox11)
        self.BodyLabel_15.setObjectName(u"BodyLabel_15")
        self.BodyLabel_15.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.BodyLabel_15)


        self.verticalLayout_12.addWidget(self.SettingBox11)


        self.verticalLayout_21.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.SettingBox5 = QFrame(self.frame_3)
        self.SettingBox5.setObjectName(u"SettingBox5")
        self.SettingBox5.setFrameShape(QFrame.StyledPanel)
        self.SettingBox5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.SettingBox5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.BodyLabel_2 = BodyLabel(self.SettingBox5)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")

        self.horizontalLayout_2.addWidget(self.BodyLabel_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.SwitchButton_2 = SwitchButton(self.SettingBox5)
        self.SwitchButton_2.setObjectName(u"SwitchButton_2")
        self.SwitchButton_2.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_2.addWidget(self.SwitchButton_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.BodyLabel_3 = BodyLabel(self.SettingBox5)
        self.BodyLabel_3.setObjectName(u"BodyLabel_3")
        self.BodyLabel_3.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.BodyLabel_3)


        self.verticalLayout_15.addWidget(self.SettingBox5)


        self.verticalLayout_21.addWidget(self.frame_3)

        self.frame_5 = QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_5)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_21.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.scrollAreaWidgetContents)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_4)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.SettingBox6 = QFrame(self.frame_4)
        self.SettingBox6.setObjectName(u"SettingBox6")
        self.SettingBox6.setFrameShape(QFrame.StyledPanel)
        self.SettingBox6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.SettingBox6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.SettingBox6)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(24, 24))
        self.label.setMaximumSize(QSize(24, 24))
        self.label.setPixmap(QPixmap(u"../../resources/icons/adblock.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.label)

        self.BodyLabel_6 = BodyLabel(self.SettingBox6)
        self.BodyLabel_6.setObjectName(u"BodyLabel_6")

        self.horizontalLayout_3.addWidget(self.BodyLabel_6)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.SwitchButton_3 = SwitchButton(self.SettingBox6)
        self.SwitchButton_3.setObjectName(u"SwitchButton_3")
        self.SwitchButton_3.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_3.addWidget(self.SwitchButton_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_16.addWidget(self.SettingBox6)

        self.SettingBox7 = QFrame(self.frame_4)
        self.SettingBox7.setObjectName(u"SettingBox7")
        self.SettingBox7.setFrameShape(QFrame.StyledPanel)
        self.SettingBox7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.SettingBox7)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(self.SettingBox7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(24, 24))
        self.label_2.setMaximumSize(QSize(24, 24))
        self.label_2.setPixmap(QPixmap(u"../../resources/icons/discord.png"))
        self.label_2.setScaledContents(True)

        self.horizontalLayout_9.addWidget(self.label_2)

        self.BodyLabel_12 = BodyLabel(self.SettingBox7)
        self.BodyLabel_12.setObjectName(u"BodyLabel_12")

        self.horizontalLayout_9.addWidget(self.BodyLabel_12)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_8)

        self.SwitchButton_7 = SwitchButton(self.SettingBox7)
        self.SwitchButton_7.setObjectName(u"SwitchButton_7")
        self.SwitchButton_7.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_9.addWidget(self.SwitchButton_7)


        self.verticalLayout_9.addLayout(self.horizontalLayout_9)


        self.verticalLayout_16.addWidget(self.SettingBox7)

        self.SettingBox9 = QFrame(self.frame_4)
        self.SettingBox9.setObjectName(u"SettingBox9")
        self.SettingBox9.setFrameShape(QFrame.StyledPanel)
        self.SettingBox9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.SettingBox9)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_3 = QLabel(self.SettingBox9)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(24, 24))
        self.label_3.setMaximumSize(QSize(24, 24))
        self.label_3.setPixmap(QPixmap(u"../../resources/icons/windows.png"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout_13.addWidget(self.label_3)

        self.BodyLabel_18 = BodyLabel(self.SettingBox9)
        self.BodyLabel_18.setObjectName(u"BodyLabel_18")

        self.horizontalLayout_13.addWidget(self.BodyLabel_18)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_12)

        self.SwitchButton_11 = SwitchButton(self.SettingBox9)
        self.SwitchButton_11.setObjectName(u"SwitchButton_11")
        self.SwitchButton_11.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_13.addWidget(self.SwitchButton_11)


        self.verticalLayout_20.addLayout(self.horizontalLayout_13)


        self.verticalLayout_16.addWidget(self.SettingBox9)

        self.SettingBox10 = QFrame(self.frame_4)
        self.SettingBox10.setObjectName(u"SettingBox10")
        self.SettingBox10.setFrameShape(QFrame.StyledPanel)
        self.SettingBox10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.SettingBox10)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_4 = QLabel(self.SettingBox10)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(24, 24))
        self.label_4.setMaximumSize(QSize(24, 24))
        self.label_4.setPixmap(QPixmap(u"../../resources/icons/icon.ico"))
        self.label_4.setScaledContents(True)

        self.horizontalLayout_14.addWidget(self.label_4)

        self.BodyLabel_20 = BodyLabel(self.SettingBox10)
        self.BodyLabel_20.setObjectName(u"BodyLabel_20")

        self.horizontalLayout_14.addWidget(self.BodyLabel_20)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_13)

        self.SwitchButton_12 = SwitchButton(self.SettingBox10)
        self.SwitchButton_12.setObjectName(u"SwitchButton_12")
        self.SwitchButton_12.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_14.addWidget(self.SwitchButton_12)


        self.verticalLayout_22.addLayout(self.horizontalLayout_14)


        self.verticalLayout_16.addWidget(self.SettingBox10)


        self.verticalLayout_21.addWidget(self.frame_4)

        self.verticalSpacer_5 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_21.addItem(self.verticalSpacer_5)

        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.ScrollArea)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.ButtonBox = QFrame(Dialog)
        self.ButtonBox.setObjectName(u"ButtonBox")
        self.ButtonBox.setFrameShape(QFrame.StyledPanel)
        self.ButtonBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.ButtonBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(12, 16, 12, 16)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.PrimaryPushButton = PrimaryPushButton(self.ButtonBox)
        self.PrimaryPushButton.setObjectName(u"PrimaryPushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton.setSizePolicy(sizePolicy)
        self.PrimaryPushButton.setMinimumSize(QSize(160, 0))
        self.PrimaryPushButton.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_5.addWidget(self.PrimaryPushButton)

        self.PushButton = PushButton(self.ButtonBox)
        self.PushButton.setObjectName(u"PushButton")
        sizePolicy.setHeightForWidth(self.PushButton.sizePolicy().hasHeightForWidth())
        self.PushButton.setSizePolicy(sizePolicy)
        self.PushButton.setMinimumSize(QSize(160, 0))
        self.PushButton.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_5.addWidget(self.PushButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)


        self.verticalLayout_6.addWidget(self.ButtonBox)


        self.retranslateUi(Dialog)

        self.PillPushButton_2.setDefault(False)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Settings", None))
        self.PillPushButton.setText(QCoreApplication.translate("Dialog", u"Main", None))
        self.PillPushButton_2.setText(QCoreApplication.translate("Dialog", u"Web Engine", None))
        self.PillPushButton_3.setText(QCoreApplication.translate("Dialog", u"Mini-Player", None))
        self.PillPushButton_4.setText(QCoreApplication.translate("Dialog", u"Plugins", None))
        self.BodyLabel.setText(QCoreApplication.translate("Dialog", u"Save and restore window size", None))
        self.BodyLabel_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#808080;\">When enabled, the application remembers the window size for your next session.</span></p></body></html>", None))
        self.BodyLabel_7.setText(QCoreApplication.translate("Dialog", u"Save and restore last URL", None))
        self.BodyLabel_8.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#808080;\">When enabled, the application remembers the last URL for your next session.</span></p></body></html>", None))
        self.BodyLabel_9.setText(QCoreApplication.translate("Dialog", u"Full screen mode support", None))
        self.BodyLabel_11.setText(QCoreApplication.translate("Dialog", u"Animated scrolling support", None))
        self.BodyLabel_13.setText(QCoreApplication.translate("Dialog", u"Save and restore zoom factor", None))
        self.BodyLabel_22.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#808080;\">When enabled, the application remembers the last zoom factor for your next session.</span></p></body></html>", None))
        self.BodyLabel_5.setText(QCoreApplication.translate("Dialog", u"Application Proxy Support", None))
        self.StrongBodyLabel.setText(QCoreApplication.translate("Dialog", u"(BETA)", None))
        self.BodyLabel_10.setText(QCoreApplication.translate("Dialog", u"Host:", None))
        self.LineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"192.168.1.100", None))
        self.BodyLabel_14.setText(QCoreApplication.translate("Dialog", u"Port:", None))
        self.LineEdit_2.setPlaceholderText(QCoreApplication.translate("Dialog", u"8080", None))
        self.BodyLabel_15.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#808080;\">When enabled, this setting allows you to specify a custom proxy server for accessing the YouTube Music website. </span></p></body></html>", None))
        self.BodyLabel_2.setText(QCoreApplication.translate("Dialog", u"Save and restore mini-player position", None))
        self.BodyLabel_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#808080;\">When enabled, the mini-player will open at the last position it was moved to.</span></p></body></html>", None))
        self.label.setText("")
        self.BodyLabel_6.setText(QCoreApplication.translate("Dialog", u"Ad Blocker (Skipper)", None))
        self.label_2.setText("")
        self.BodyLabel_12.setText(QCoreApplication.translate("Dialog", u"Discord Rich Presence", None))
        self.label_3.setText("")
        self.BodyLabel_18.setText(QCoreApplication.translate("Dialog", u"Windows Thumbnail Buttons", None))
        self.label_4.setText("")
        self.BodyLabel_20.setText(QCoreApplication.translate("Dialog", u"System Tray App Icon", None))
        self.PrimaryPushButton.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.PushButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

