# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Program Files\Projects\Youtube-Music-Desktop-Player-main\core\ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(563, 369)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: rgb(39,39,39);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalFrame = QtWidgets.QFrame(self.centralwidget)
        self.horizontalFrame.setStyleSheet("QFrame {\n"
"    background: rgb(33,33,33);\n"
"}")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ToolButton = ToolButton(self.horizontalFrame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/arrow_back_white_24dp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton.setIcon(icon)
        self.ToolButton.setObjectName("ToolButton")
        self.horizontalLayout_3.addWidget(self.ToolButton)
        self.ToolButton_2 = ToolButton(self.horizontalFrame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/arrow_forward_white_24dp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_2.setIcon(icon1)
        self.ToolButton_2.setObjectName("ToolButton_2")
        self.horizontalLayout_3.addWidget(self.ToolButton_2)
        self.ToolButton_3 = ToolButton(self.horizontalFrame)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/home_white_24dp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_3.setIcon(icon2)
        self.ToolButton_3.setObjectName("ToolButton_3")
        self.horizontalLayout_3.addWidget(self.ToolButton_3)
        self.ToolButton_4 = ToolButton(self.horizontalFrame)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/refresh_white_24dp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_4.setIcon(icon3)
        self.ToolButton_4.setObjectName("ToolButton_4")
        self.horizontalLayout_3.addWidget(self.ToolButton_4)
        self.VerticalSeparator_2 = VerticalSeparator(self.horizontalFrame)
        self.VerticalSeparator_2.setObjectName("VerticalSeparator_2")
        self.horizontalLayout_3.addWidget(self.VerticalSeparator_2)
        self.LineEdit = LineEdit(self.horizontalFrame)
        self.LineEdit.setReadOnly(True)
        self.LineEdit.setObjectName("LineEdit")
        self.horizontalLayout_3.addWidget(self.LineEdit)
        self.VerticalSeparator_3 = VerticalSeparator(self.horizontalFrame)
        self.VerticalSeparator_3.setObjectName("VerticalSeparator_3")
        self.horizontalLayout_3.addWidget(self.VerticalSeparator_3)
        self.ToolButton_5 = ToolButton(self.horizontalFrame)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/file_download_white_24dp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_5.setIcon(icon4)
        self.ToolButton_5.setObjectName("ToolButton_5")
        self.horizontalLayout_3.addWidget(self.ToolButton_5)
        self.ToolButton_6 = ToolButton(self.horizontalFrame)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/picture_in_picture_white_24dp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_6.setIcon(icon5)
        self.ToolButton_6.setObjectName("ToolButton_6")
        self.horizontalLayout_3.addWidget(self.ToolButton_6)
        self.VerticalSeparator = VerticalSeparator(self.horizontalFrame)
        self.VerticalSeparator.setObjectName("VerticalSeparator")
        self.horizontalLayout_3.addWidget(self.VerticalSeparator)
        self.ToolButton_7 = ToolButton(self.horizontalFrame)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/settings_white_24dp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ToolButton_7.setIcon(icon6)
        self.ToolButton_7.setObjectName("ToolButton_7")
        self.horizontalLayout_3.addWidget(self.ToolButton_7)
        self.verticalLayout.addWidget(self.horizontalFrame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(0, 37, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setStyleSheet("QFrame {\n"
"    background-color: rgb(0,0,0);\n"
"    color: white;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setContentsMargins(6, 4, 6, 4)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setMinimumSize(QtCore.QSize(5, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setStyleSheet("QLabel {\n"
"    color: lightgray;\n"
"}\n"
"QLabel::hover {\n"
"    color: white;\n"
"}")
        self.label.setText("")
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(30, 7, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setMinimumSize(QtCore.QSize(0, 15))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("d:\\Program Files\\Projects\\Youtube-Music-Desktop-Player-main\\core\\ui\\../../resources/icons/file_download_white_24dp.svg"))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.frame = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setStyleSheet("QLabel {\n"
"    font-weight: bold;\n"
"}")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_4.addWidget(self.frame)
        self.verticalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ToolButton.setToolTip(_translate("MainWindow", "Back"))
        self.ToolButton_2.setToolTip(_translate("MainWindow", "Forward"))
        self.ToolButton_3.setToolTip(_translate("MainWindow", "Home"))
        self.ToolButton_4.setToolTip(_translate("MainWindow", "Reload"))
        self.ToolButton_5.setToolTip(_translate("MainWindow", "Download Track/Playlist"))
        self.ToolButton_6.setToolTip(_translate("MainWindow", "Open Mini-Player"))
        self.ToolButton_7.setToolTip(_translate("MainWindow", "Open Settings"))
from qfluentwidgets import LineEdit, ToolButton, VerticalSeparator
