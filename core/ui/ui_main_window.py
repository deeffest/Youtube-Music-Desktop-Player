# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 495)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ToolBar = QtWidgets.QFrame(self.centralwidget)
        self.ToolBar.setObjectName("ToolBar")
        self.toolbar_layout = QtWidgets.QHBoxLayout(self.ToolBar)
        self.toolbar_layout.setContentsMargins(6, 6, 6, 6)
        self.toolbar_layout.setSpacing(6)
        self.toolbar_layout.setObjectName("toolbar_layout")
        self.back_tbutton = ToolButton(self.ToolBar)
        self.back_tbutton.setEnabled(False)
        self.back_tbutton.setObjectName("back_tbutton")
        self.toolbar_layout.addWidget(self.back_tbutton)
        self.forward_tbutton = ToolButton(self.ToolBar)
        self.forward_tbutton.setEnabled(False)
        self.forward_tbutton.setObjectName("forward_tbutton")
        self.toolbar_layout.addWidget(self.forward_tbutton)
        self.home_tbutton = ToolButton(self.ToolBar)
        self.home_tbutton.setObjectName("home_tbutton")
        self.toolbar_layout.addWidget(self.home_tbutton)
        self.reload_tbutton = ToolButton(self.ToolBar)
        self.reload_tbutton.setObjectName("reload_tbutton")
        self.toolbar_layout.addWidget(self.reload_tbutton)
        self.url_line_edit = LineEdit(self.ToolBar)
        self.url_line_edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.url_line_edit.setReadOnly(False)
        self.url_line_edit.setObjectName("url_line_edit")
        self.toolbar_layout.addWidget(self.url_line_edit)
        self.download_ddtbutton = DropDownToolButton(self.ToolBar)
        self.download_ddtbutton.setObjectName("download_ddtbutton")
        self.toolbar_layout.addWidget(self.download_ddtbutton)
        self.mini_player_tbutton = ToolButton(self.ToolBar)
        self.mini_player_tbutton.setObjectName("mini_player_tbutton")
        self.toolbar_layout.addWidget(self.mini_player_tbutton)
        self.settings_tbutton = ToolButton(self.ToolBar)
        self.settings_tbutton.setObjectName("settings_tbutton")
        self.toolbar_layout.addWidget(self.settings_tbutton)
        self.bug_report_tbutton = ToolButton(self.ToolBar)
        self.bug_report_tbutton.setObjectName("bug_report_tbutton")
        self.toolbar_layout.addWidget(self.bug_report_tbutton)
        self.about_tbutton = ToolButton(self.ToolBar)
        self.about_tbutton.setObjectName("about_tbutton")
        self.toolbar_layout.addWidget(self.about_tbutton)
        self.verticalLayout.addWidget(self.ToolBar)
        self.MainLayout = QtWidgets.QHBoxLayout()
        self.MainLayout.setObjectName("MainLayout")
        spacerItem = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.MainLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.MainLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.back_tbutton.setToolTip(_translate("MainWindow", "Back"))
        self.forward_tbutton.setToolTip(_translate("MainWindow", "Forward"))
        self.home_tbutton.setToolTip(_translate("MainWindow", "Home"))
        self.reload_tbutton.setToolTip(_translate("MainWindow", "Reload"))
        self.url_line_edit.setPlaceholderText(_translate("MainWindow", "https://music.youtube.com/"))
        self.download_ddtbutton.setToolTip(_translate("MainWindow", "Get Audio"))
        self.mini_player_tbutton.setToolTip(_translate("MainWindow", "Mini-Player"))
        self.settings_tbutton.setToolTip(_translate("MainWindow", "Settings"))
        self.bug_report_tbutton.setToolTip(_translate("MainWindow", "Bug Report"))
        self.about_tbutton.setToolTip(_translate("MainWindow", "About"))
from qfluentwidgets import DropDownToolButton, LineEdit, ToolButton
