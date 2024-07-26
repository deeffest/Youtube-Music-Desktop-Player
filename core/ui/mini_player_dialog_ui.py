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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(360, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(360, 150))
        Dialog.setMaximumSize(QSize(360, 150))
        Dialog.setMouseTracking(True)
        Dialog.setStyleSheet(u"QDialog {\n"
"	background-color: rgb(39,39,39);\n"
"}")
        self.verticalLayout = QVBoxLayout(Dialog)
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

        self.StrongBodyLabel = StrongBodyLabel(Dialog)
        self.StrongBodyLabel.setObjectName(u"StrongBodyLabel")

        self.verticalLayout_2.addWidget(self.StrongBodyLabel)

        self.BodyLabel_2 = BodyLabel(Dialog)
        self.BodyLabel_2.setObjectName(u"BodyLabel_2")
        self.BodyLabel_2.setStyleSheet(u"QLabel {\n"
"	color: lightgray;\n"
"	font-size: 13px;\n"
"}")

        self.verticalLayout_2.addWidget(self.BodyLabel_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 60))
        self.label.setMaximumSize(QSize(60, 60))
        self.label.setScaledContents(False)

        self.horizontalLayout_2.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(30)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 3, 4, 18)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.TransparentToolButton = TransparentToolButton(Dialog)
        self.TransparentToolButton.setObjectName(u"TransparentToolButton")
        self.TransparentToolButton.setMinimumSize(QSize(40, 40))
        self.TransparentToolButton.setMaximumSize(QSize(40, 40))
        self.TransparentToolButton.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.TransparentToolButton)

        self.TransparentToolButton_2 = TransparentToolButton(Dialog)
        self.TransparentToolButton_2.setObjectName(u"TransparentToolButton_2")
        self.TransparentToolButton_2.setMinimumSize(QSize(40, 40))
        self.TransparentToolButton_2.setMaximumSize(QSize(40, 40))
        self.TransparentToolButton_2.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.TransparentToolButton_2)

        self.TransparentToolButton_3 = TransparentToolButton(Dialog)
        self.TransparentToolButton_3.setObjectName(u"TransparentToolButton_3")
        self.TransparentToolButton_3.setMinimumSize(QSize(40, 40))
        self.TransparentToolButton_3.setMaximumSize(QSize(40, 40))
        self.TransparentToolButton_3.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.TransparentToolButton_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.StrongBodyLabel.setText("")
        self.BodyLabel_2.setText("")
        self.label.setText("")
#if QT_CONFIG(shortcut)
        self.TransparentToolButton.setShortcut(QCoreApplication.translate("Dialog", u"Left", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(shortcut)
        self.TransparentToolButton_2.setShortcut(QCoreApplication.translate("Dialog", u"Space", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(shortcut)
        self.TransparentToolButton_3.setShortcut(QCoreApplication.translate("Dialog", u"Right", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

