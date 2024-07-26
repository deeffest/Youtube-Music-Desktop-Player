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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (LineEdit, ToolButton, VerticalSeparator)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(563, 369)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"	background-color: rgb(39,39,39);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalFrame = QFrame(self.centralwidget)
        self.horizontalFrame.setObjectName(u"horizontalFrame")
        self.horizontalFrame.setStyleSheet(u"QFrame {\n"
"	background: rgb(33,33,33);\n"
"}")
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.ToolButton = ToolButton(self.horizontalFrame)
        self.ToolButton.setObjectName(u"ToolButton")
        icon = QIcon()
        icon.addFile(u"../../resources/icons/left.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ToolButton.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.ToolButton)

        self.ToolButton_2 = ToolButton(self.horizontalFrame)
        self.ToolButton_2.setObjectName(u"ToolButton_2")
        icon1 = QIcon()
        icon1.addFile(u"../../resources/icons/right.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ToolButton_2.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.ToolButton_2)

        self.ToolButton_3 = ToolButton(self.horizontalFrame)
        self.ToolButton_3.setObjectName(u"ToolButton_3")
        icon2 = QIcon()
        icon2.addFile(u"../../resources/icons/home.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ToolButton_3.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.ToolButton_3)

        self.ToolButton_4 = ToolButton(self.horizontalFrame)
        self.ToolButton_4.setObjectName(u"ToolButton_4")
        icon3 = QIcon()
        icon3.addFile(u"../../resources/icons/sync.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ToolButton_4.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.ToolButton_4)

        self.VerticalSeparator_2 = VerticalSeparator(self.horizontalFrame)
        self.VerticalSeparator_2.setObjectName(u"VerticalSeparator_2")

        self.horizontalLayout_3.addWidget(self.VerticalSeparator_2)

        self.LineEdit = LineEdit(self.horizontalFrame)
        self.LineEdit.setObjectName(u"LineEdit")
        self.LineEdit.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.LineEdit)

        self.VerticalSeparator_3 = VerticalSeparator(self.horizontalFrame)
        self.VerticalSeparator_3.setObjectName(u"VerticalSeparator_3")

        self.horizontalLayout_3.addWidget(self.VerticalSeparator_3)

        self.ToolButton_5 = ToolButton(self.horizontalFrame)
        self.ToolButton_5.setObjectName(u"ToolButton_5")
        icon4 = QIcon()
        icon4.addFile(u"../../resources/icons/download.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ToolButton_5.setIcon(icon4)

        self.horizontalLayout_3.addWidget(self.ToolButton_5)

        self.ToolButton_6 = ToolButton(self.horizontalFrame)
        self.ToolButton_6.setObjectName(u"ToolButton_6")
        icon5 = QIcon()
        icon5.addFile(u"../../resources/icons/picture_in_picture.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ToolButton_6.setIcon(icon5)

        self.horizontalLayout_3.addWidget(self.ToolButton_6)

        self.VerticalSeparator = VerticalSeparator(self.horizontalFrame)
        self.VerticalSeparator.setObjectName(u"VerticalSeparator")

        self.horizontalLayout_3.addWidget(self.VerticalSeparator)

        self.ToolButton_7 = ToolButton(self.horizontalFrame)
        self.ToolButton_7.setObjectName(u"ToolButton_7")
        icon6 = QIcon()
        icon6.addFile(u"../../resources/icons/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ToolButton_7.setIcon(icon6)

        self.horizontalLayout_3.addWidget(self.ToolButton_7)


        self.verticalLayout.addWidget(self.horizontalFrame)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalSpacer = QSpacerItem(0, 37, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout.addItem(self.verticalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(0,0,0);\n"
"	color: white;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(5, 0))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        self.label.setFont(font)
        self.label.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.label.setStyleSheet(u"QLabel {\n"
"	color: lightgray;\n"
"}\n"
"QLabel::hover {\n"
"	color: white;\n"
"}")
        self.label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        self.horizontalLayout_2.addWidget(self.label)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(30, 7, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 15))
        self.label_3.setMaximumSize(QSize(16777215, 15))
        self.label_3.setPixmap(QPixmap(u"../../resources/icons/download.svg"))
        self.label_3.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"QLabel {\n"
"    font-weight: bold;\n"
"}")

        self.verticalLayout_2.addWidget(self.label_2)


        self.horizontalLayout_4.addWidget(self.frame)


        self.verticalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.ToolButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_4.setToolTip(QCoreApplication.translate("MainWindow", u"Reload", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_6.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.ToolButton_7.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label.setText("")
        self.label_3.setText("")
        self.label_2.setText("")
    # retranslateUi

