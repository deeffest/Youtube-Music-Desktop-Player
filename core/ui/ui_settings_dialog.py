# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(530, 340)
        SettingsDialog.setMinimumSize(QtCore.QSize(530, 340))
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(SettingsDialog)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.SideBar = QtWidgets.QFrame(SettingsDialog)
        self.SideBar.setObjectName("SideBar")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.SideBar)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PillPushButton = PillPushButton(self.SideBar)
        self.PillPushButton.setChecked(False)
        self.PillPushButton.setAutoExclusive(True)
        self.PillPushButton.setObjectName("PillPushButton")
        self.verticalLayout.addWidget(self.PillPushButton)
        self.PillPushButton_2 = PillPushButton(self.SideBar)
        self.PillPushButton_2.setAutoExclusive(True)
        self.PillPushButton_2.setDefault(False)
        self.PillPushButton_2.setObjectName("PillPushButton_2")
        self.verticalLayout.addWidget(self.PillPushButton_2)
        self.PillPushButton_3 = PillPushButton(self.SideBar)
        self.PillPushButton_3.setAutoExclusive(True)
        self.PillPushButton_3.setObjectName("PillPushButton_3")
        self.verticalLayout.addWidget(self.PillPushButton_3)
        self.HorizontalSeparator = HorizontalSeparator(self.SideBar)
        self.HorizontalSeparator.setObjectName("HorizontalSeparator")
        self.verticalLayout.addWidget(self.HorizontalSeparator)
        self.PillPushButton_4 = PillPushButton(self.SideBar)
        self.PillPushButton_4.setAutoExclusive(True)
        self.PillPushButton_4.setProperty("hasIcon", True)
        self.PillPushButton_4.setObjectName("PillPushButton_4")
        self.verticalLayout.addWidget(self.PillPushButton_4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_4.addWidget(self.SideBar)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ScrollArea = ScrollArea(SettingsDialog)
        self.ScrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setObjectName("ScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -703, 394, 964))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_29.setContentsMargins(0, 0, 16, 0)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.SettingBox = QtWidgets.QFrame(self.frame)
        self.SettingBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox.setObjectName("SettingBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.SettingBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.BodyLabel = BodyLabel(self.SettingBox)
        self.BodyLabel.setObjectName("BodyLabel")
        self.horizontalLayout.addWidget(self.BodyLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.SwitchButton = SwitchButton(self.SettingBox)
        self.SwitchButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton.setProperty("checked", False)
        self.SwitchButton.setObjectName("SwitchButton")
        self.horizontalLayout.addWidget(self.SwitchButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.BodyLabel_4 = BodyLabel(self.SettingBox)
        self.BodyLabel_4.setWordWrap(True)
        self.BodyLabel_4.setObjectName("BodyLabel_4")
        self.verticalLayout_2.addWidget(self.BodyLabel_4)
        self.verticalLayout_29.addWidget(self.SettingBox)
        self.SettingBox2 = QtWidgets.QFrame(self.frame)
        self.SettingBox2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox2.setObjectName("SettingBox2")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.SettingBox2)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.BodyLabel_7 = BodyLabel(self.SettingBox2)
        self.BodyLabel_7.setObjectName("BodyLabel_7")
        self.horizontalLayout_6.addWidget(self.BodyLabel_7)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.SwitchButton_4 = SwitchButton(self.SettingBox2)
        self.SwitchButton_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_4.setProperty("checked", False)
        self.SwitchButton_4.setObjectName("SwitchButton_4")
        self.horizontalLayout_6.addWidget(self.SwitchButton_4)
        self.verticalLayout_14.addLayout(self.horizontalLayout_6)
        self.BodyLabel_8 = BodyLabel(self.SettingBox2)
        self.BodyLabel_8.setWordWrap(True)
        self.BodyLabel_8.setObjectName("BodyLabel_8")
        self.verticalLayout_14.addWidget(self.BodyLabel_8)
        self.verticalLayout_29.addWidget(self.SettingBox2)
        self.SettingBox11 = QtWidgets.QFrame(self.frame)
        self.SettingBox11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox11.setObjectName("SettingBox11")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.SettingBox11)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.BodyLabel_5 = BodyLabel(self.SettingBox11)
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.horizontalLayout_11.addWidget(self.BodyLabel_5)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.ComboBox = ComboBox(self.SettingBox11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox.sizePolicy().hasHeightForWidth())
        self.ComboBox.setSizePolicy(sizePolicy)
        self.ComboBox.setObjectName("ComboBox")
        self.horizontalLayout_11.addWidget(self.ComboBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.BodyLabel_10 = BodyLabel(self.SettingBox11)
        self.BodyLabel_10.setEnabled(True)
        self.BodyLabel_10.setObjectName("BodyLabel_10")
        self.horizontalLayout_12.addWidget(self.BodyLabel_10)
        self.LineEdit = LineEdit(self.SettingBox11)
        self.LineEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit.sizePolicy().hasHeightForWidth())
        self.LineEdit.setSizePolicy(sizePolicy)
        self.LineEdit.setMinimumSize(QtCore.QSize(0, 33))
        self.LineEdit.setMaximumSize(QtCore.QSize(16777215, 33))
        self.LineEdit.setClearButtonEnabled(False)
        self.LineEdit.setObjectName("LineEdit")
        self.horizontalLayout_12.addWidget(self.LineEdit)
        self.BodyLabel_14 = BodyLabel(self.SettingBox11)
        self.BodyLabel_14.setEnabled(True)
        self.BodyLabel_14.setObjectName("BodyLabel_14")
        self.horizontalLayout_12.addWidget(self.BodyLabel_14)
        self.LineEdit_2 = LineEdit(self.SettingBox11)
        self.LineEdit_2.setEnabled(True)
        self.LineEdit_2.setMinimumSize(QtCore.QSize(0, 33))
        self.LineEdit_2.setMaximumSize(QtCore.QSize(16777215, 33))
        self.LineEdit_2.setClearButtonEnabled(False)
        self.LineEdit_2.setObjectName("LineEdit_2")
        self.horizontalLayout_12.addWidget(self.LineEdit_2)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.BodyLabel_16 = BodyLabel(self.SettingBox11)
        self.BodyLabel_16.setEnabled(True)
        self.BodyLabel_16.setObjectName("BodyLabel_16")
        self.horizontalLayout_16.addWidget(self.BodyLabel_16)
        self.LineEdit_3 = LineEdit(self.SettingBox11)
        self.LineEdit_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LineEdit_3.sizePolicy().hasHeightForWidth())
        self.LineEdit_3.setSizePolicy(sizePolicy)
        self.LineEdit_3.setMinimumSize(QtCore.QSize(0, 33))
        self.LineEdit_3.setMaximumSize(QtCore.QSize(16777215, 33))
        self.LineEdit_3.setObjectName("LineEdit_3")
        self.horizontalLayout_16.addWidget(self.LineEdit_3)
        self.BodyLabel_17 = BodyLabel(self.SettingBox11)
        self.BodyLabel_17.setEnabled(True)
        self.BodyLabel_17.setObjectName("BodyLabel_17")
        self.horizontalLayout_16.addWidget(self.BodyLabel_17)
        self.PasswordLineEdit = PasswordLineEdit(self.SettingBox11)
        self.PasswordLineEdit.setEnabled(True)
        self.PasswordLineEdit.setMinimumSize(QtCore.QSize(0, 33))
        self.PasswordLineEdit.setMaximumSize(QtCore.QSize(16777215, 33))
        self.PasswordLineEdit.setObjectName("PasswordLineEdit")
        self.horizontalLayout_16.addWidget(self.PasswordLineEdit)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)
        self.BodyLabel_15 = BodyLabel(self.SettingBox11)
        self.BodyLabel_15.setWordWrap(True)
        self.BodyLabel_15.setObjectName("BodyLabel_15")
        self.verticalLayout_8.addWidget(self.BodyLabel_15)
        self.verticalLayout_29.addWidget(self.SettingBox11)
        self.SettingBox15 = QtWidgets.QFrame(self.frame)
        self.SettingBox15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox15.setObjectName("SettingBox15")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.SettingBox15)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.BodyLabel_36 = BodyLabel(self.SettingBox15)
        self.BodyLabel_36.setObjectName("BodyLabel_36")
        self.horizontalLayout_24.addWidget(self.BodyLabel_36)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_24.addItem(spacerItem4)
        self.ComboBox_3 = ComboBox(self.SettingBox15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox_3.sizePolicy().hasHeightForWidth())
        self.ComboBox_3.setSizePolicy(sizePolicy)
        self.ComboBox_3.setObjectName("ComboBox_3")
        self.horizontalLayout_24.addWidget(self.ComboBox_3)
        self.verticalLayout_28.addLayout(self.horizontalLayout_24)
        self.BodyLabel_42 = BodyLabel(self.SettingBox15)
        self.BodyLabel_42.setWordWrap(True)
        self.BodyLabel_42.setObjectName("BodyLabel_42")
        self.verticalLayout_28.addWidget(self.BodyLabel_42)
        self.verticalLayout_29.addWidget(self.SettingBox15)
        self.verticalLayout_21.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.SettingBox3 = QtWidgets.QFrame(self.frame_2)
        self.SettingBox3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox3.setObjectName("SettingBox3")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.SettingBox3)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.BodyLabel_9 = BodyLabel(self.SettingBox3)
        self.BodyLabel_9.setObjectName("BodyLabel_9")
        self.horizontalLayout_7.addWidget(self.BodyLabel_9)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.SwitchButton_5 = SwitchButton(self.SettingBox3)
        self.SwitchButton_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_5.setProperty("checked", False)
        self.SwitchButton_5.setObjectName("SwitchButton_5")
        self.horizontalLayout_7.addWidget(self.SwitchButton_5)
        self.verticalLayout_13.addLayout(self.horizontalLayout_7)
        self.verticalLayout_12.addWidget(self.SettingBox3)
        self.SettingBox4 = QtWidgets.QFrame(self.frame_2)
        self.SettingBox4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox4.setObjectName("SettingBox4")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.SettingBox4)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.BodyLabel_11 = BodyLabel(self.SettingBox4)
        self.BodyLabel_11.setObjectName("BodyLabel_11")
        self.horizontalLayout_8.addWidget(self.BodyLabel_11)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.SwitchButton_6 = SwitchButton(self.SettingBox4)
        self.SwitchButton_6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_6.setObjectName("SwitchButton_6")
        self.horizontalLayout_8.addWidget(self.SwitchButton_6)
        self.verticalLayout_11.addLayout(self.horizontalLayout_8)
        self.verticalLayout_12.addWidget(self.SettingBox4)
        self.SettingBox8 = QtWidgets.QFrame(self.frame_2)
        self.SettingBox8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox8.setObjectName("SettingBox8")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.SettingBox8)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.BodyLabel_13 = BodyLabel(self.SettingBox8)
        self.BodyLabel_13.setObjectName("BodyLabel_13")
        self.horizontalLayout_10.addWidget(self.BodyLabel_13)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.SwitchButton_8 = SwitchButton(self.SettingBox8)
        self.SwitchButton_8.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_8.setObjectName("SwitchButton_8")
        self.horizontalLayout_10.addWidget(self.SwitchButton_8)
        self.verticalLayout_17.addLayout(self.horizontalLayout_10)
        self.BodyLabel_22 = BodyLabel(self.SettingBox8)
        self.BodyLabel_22.setWordWrap(True)
        self.BodyLabel_22.setObjectName("BodyLabel_22")
        self.verticalLayout_17.addWidget(self.BodyLabel_22)
        self.verticalLayout_12.addWidget(self.SettingBox8)
        self.verticalLayout_21.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.SettingBox5 = QtWidgets.QFrame(self.frame_3)
        self.SettingBox5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox5.setObjectName("SettingBox5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.SettingBox5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.BodyLabel_2 = BodyLabel(self.SettingBox5)
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.horizontalLayout_2.addWidget(self.BodyLabel_2)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.SwitchButton_2 = SwitchButton(self.SettingBox5)
        self.SwitchButton_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_2.setObjectName("SwitchButton_2")
        self.horizontalLayout_2.addWidget(self.SwitchButton_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.BodyLabel_3 = BodyLabel(self.SettingBox5)
        self.BodyLabel_3.setWordWrap(True)
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.verticalLayout_3.addWidget(self.BodyLabel_3)
        self.verticalLayout_15.addWidget(self.SettingBox5)
        self.verticalLayout_21.addWidget(self.frame_3)
        self.frame_5 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.verticalLayout_21.addWidget(self.frame_5)
        self.frame_4 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_16.setContentsMargins(0, 0, 16, 0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.SettingBox6 = QtWidgets.QFrame(self.frame_4)
        self.SettingBox6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox6.setObjectName("SettingBox6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.SettingBox6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.SettingBox6)
        self.label.setMinimumSize(QtCore.QSize(22, 22))
        self.label.setMaximumSize(QtCore.QSize(22, 22))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.BodyLabel_6 = BodyLabel(self.SettingBox6)
        self.BodyLabel_6.setObjectName("BodyLabel_6")
        self.horizontalLayout_3.addWidget(self.BodyLabel_6)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.SwitchButton_3 = SwitchButton(self.SettingBox6)
        self.SwitchButton_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_3.setObjectName("SwitchButton_3")
        self.horizontalLayout_3.addWidget(self.SwitchButton_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_16.addWidget(self.SettingBox6)
        self.SettingBox7 = QtWidgets.QFrame(self.frame_4)
        self.SettingBox7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox7.setObjectName("SettingBox7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.SettingBox7)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_2 = QtWidgets.QLabel(self.SettingBox7)
        self.label_2.setMinimumSize(QtCore.QSize(22, 22))
        self.label_2.setMaximumSize(QtCore.QSize(22, 22))
        self.label_2.setText("")
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_9.addWidget(self.label_2)
        self.BodyLabel_12 = BodyLabel(self.SettingBox7)
        self.BodyLabel_12.setObjectName("BodyLabel_12")
        self.horizontalLayout_9.addWidget(self.BodyLabel_12)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem10)
        self.SwitchButton_7 = SwitchButton(self.SettingBox7)
        self.SwitchButton_7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_7.setObjectName("SwitchButton_7")
        self.horizontalLayout_9.addWidget(self.SwitchButton_7)
        self.verticalLayout_9.addLayout(self.horizontalLayout_9)
        self.verticalLayout_16.addWidget(self.SettingBox7)
        self.SettingBox9 = QtWidgets.QFrame(self.frame_4)
        self.SettingBox9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox9.setObjectName("SettingBox9")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.SettingBox9)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_3 = QtWidgets.QLabel(self.SettingBox9)
        self.label_3.setMinimumSize(QtCore.QSize(22, 22))
        self.label_3.setMaximumSize(QtCore.QSize(22, 22))
        self.label_3.setText("")
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_13.addWidget(self.label_3)
        self.BodyLabel_18 = BodyLabel(self.SettingBox9)
        self.BodyLabel_18.setObjectName("BodyLabel_18")
        self.horizontalLayout_13.addWidget(self.BodyLabel_18)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem11)
        self.SwitchButton_11 = SwitchButton(self.SettingBox9)
        self.SwitchButton_11.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_11.setObjectName("SwitchButton_11")
        self.horizontalLayout_13.addWidget(self.SwitchButton_11)
        self.verticalLayout_20.addLayout(self.horizontalLayout_13)
        self.verticalLayout_16.addWidget(self.SettingBox9)
        self.SettingBox10 = QtWidgets.QFrame(self.frame_4)
        self.SettingBox10.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox10.setObjectName("SettingBox10")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.SettingBox10)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_4 = QtWidgets.QLabel(self.SettingBox10)
        self.label_4.setMinimumSize(QtCore.QSize(22, 22))
        self.label_4.setMaximumSize(QtCore.QSize(22, 22))
        self.label_4.setText("")
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_14.addWidget(self.label_4)
        self.BodyLabel_20 = BodyLabel(self.SettingBox10)
        self.BodyLabel_20.setObjectName("BodyLabel_20")
        self.horizontalLayout_14.addWidget(self.BodyLabel_20)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem12)
        self.SwitchButton_12 = SwitchButton(self.SettingBox10)
        self.SwitchButton_12.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_12.setObjectName("SwitchButton_12")
        self.horizontalLayout_14.addWidget(self.SwitchButton_12)
        self.verticalLayout_22.addLayout(self.horizontalLayout_14)
        self.verticalLayout_16.addWidget(self.SettingBox10)
        self.SettingBox12 = QtWidgets.QFrame(self.frame_4)
        self.SettingBox12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox12.setObjectName("SettingBox12")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.SettingBox12)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_5 = QtWidgets.QLabel(self.SettingBox12)
        self.label_5.setMinimumSize(QtCore.QSize(22, 22))
        self.label_5.setMaximumSize(QtCore.QSize(22, 22))
        self.label_5.setText("")
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_15.addWidget(self.label_5)
        self.BodyLabel_21 = BodyLabel(self.SettingBox12)
        self.BodyLabel_21.setObjectName("BodyLabel_21")
        self.horizontalLayout_15.addWidget(self.BodyLabel_21)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem13)
        self.SwitchButton_13 = SwitchButton(self.SettingBox12)
        self.SwitchButton_13.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_13.setObjectName("SwitchButton_13")
        self.horizontalLayout_15.addWidget(self.SwitchButton_13)
        self.verticalLayout_23.addLayout(self.horizontalLayout_15)
        self.verticalLayout_16.addWidget(self.SettingBox12)
        self.SettingBox13 = QtWidgets.QFrame(self.frame_4)
        self.SettingBox13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox13.setObjectName("SettingBox13")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.SettingBox13)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_7 = QtWidgets.QLabel(self.SettingBox13)
        self.label_7.setMinimumSize(QtCore.QSize(22, 22))
        self.label_7.setMaximumSize(QtCore.QSize(22, 22))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_17.addWidget(self.label_7)
        self.BodyLabel_23 = BodyLabel(self.SettingBox13)
        self.BodyLabel_23.setObjectName("BodyLabel_23")
        self.horizontalLayout_17.addWidget(self.BodyLabel_23)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem14)
        self.SwitchButton_14 = SwitchButton(self.SettingBox13)
        self.SwitchButton_14.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_14.setObjectName("SwitchButton_14")
        self.horizontalLayout_17.addWidget(self.SwitchButton_14)
        self.verticalLayout_24.addLayout(self.horizontalLayout_17)
        self.verticalLayout_16.addWidget(self.SettingBox13)
        self.SettingBox14 = QtWidgets.QFrame(self.frame_4)
        self.SettingBox14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingBox14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingBox14.setObjectName("SettingBox14")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.SettingBox14)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_9 = QtWidgets.QLabel(self.SettingBox14)
        self.label_9.setMinimumSize(QtCore.QSize(22, 22))
        self.label_9.setMaximumSize(QtCore.QSize(22, 22))
        self.label_9.setText("")
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_18.addWidget(self.label_9)
        self.BodyLabel_24 = BodyLabel(self.SettingBox14)
        self.BodyLabel_24.setObjectName("BodyLabel_24")
        self.horizontalLayout_18.addWidget(self.BodyLabel_24)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem15)
        self.SwitchButton_15 = SwitchButton(self.SettingBox14)
        self.SwitchButton_15.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.SwitchButton_15.setObjectName("SwitchButton_15")
        self.horizontalLayout_18.addWidget(self.SwitchButton_15)
        self.verticalLayout_25.addLayout(self.horizontalLayout_18)
        self.verticalLayout_16.addWidget(self.SettingBox14)
        self.verticalLayout_21.addWidget(self.frame_4)
        spacerItem16 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_21.addItem(spacerItem16)
        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.ScrollArea)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.ButtonBox = QtWidgets.QFrame(SettingsDialog)
        self.ButtonBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonBox.setObjectName("ButtonBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.ButtonBox)
        self.verticalLayout_7.setContentsMargins(12, 16, 12, 16)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.PushButton_2 = PushButton(self.ButtonBox)
        self.PushButton_2.setObjectName("PushButton_2")
        self.horizontalLayout_5.addWidget(self.PushButton_2)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem17)
        self.PrimaryPushButton = PrimaryPushButton(self.ButtonBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton.setSizePolicy(sizePolicy)
        self.PrimaryPushButton.setMinimumSize(QtCore.QSize(160, 0))
        self.PrimaryPushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.horizontalLayout_5.addWidget(self.PrimaryPushButton)
        self.PushButton = PushButton(self.ButtonBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PushButton.sizePolicy().hasHeightForWidth())
        self.PushButton.setSizePolicy(sizePolicy)
        self.PushButton.setMinimumSize(QtCore.QSize(160, 0))
        self.PushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.PushButton.setObjectName("PushButton")
        self.horizontalLayout_5.addWidget(self.PushButton)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.verticalLayout_6.addWidget(self.ButtonBox)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.PillPushButton.setText(_translate("SettingsDialog", "Main"))
        self.PillPushButton_2.setText(_translate("SettingsDialog", "Web Engine"))
        self.PillPushButton_3.setText(_translate("SettingsDialog", "Mini-Player"))
        self.PillPushButton_4.setText(_translate("SettingsDialog", "Plugins"))
        self.BodyLabel.setText(_translate("SettingsDialog", "Save and restore window geometry"))
        self.BodyLabel_4.setText(_translate("SettingsDialog", "<html><head/><body><p><span style=\" color:#808080;\">When enabled, the application remembers the window geometry for your next session.</span></p></body></html>"))
        self.BodyLabel_7.setText(_translate("SettingsDialog", "Save and restore last URL"))
        self.BodyLabel_8.setText(_translate("SettingsDialog", "<html><head/><body><p><span style=\" color:#808080;\">When enabled, the application remembers the last URL for your next session.</span></p></body></html>"))
        self.BodyLabel_5.setText(_translate("SettingsDialog", "Proxy Server Configuration"))
        self.BodyLabel_10.setText(_translate("SettingsDialog", "Host"))
        self.LineEdit.setPlaceholderText(_translate("SettingsDialog", "192.168.1.1"))
        self.BodyLabel_14.setText(_translate("SettingsDialog", "Port"))
        self.LineEdit_2.setPlaceholderText(_translate("SettingsDialog", "8080"))
        self.BodyLabel_16.setText(_translate("SettingsDialog", "Login"))
        self.LineEdit_3.setPlaceholderText(_translate("SettingsDialog", "user123"))
        self.BodyLabel_17.setText(_translate("SettingsDialog", "Password"))
        self.PasswordLineEdit.setPlaceholderText(_translate("SettingsDialog", "pass123"))
        self.BodyLabel_15.setText(_translate("SettingsDialog", "<html><head/><body><p><span style=\" color:#808080;\">Using a proxy server helps when YouTube Music is unavailable in your country.</span></p></body></html>"))
        self.BodyLabel_36.setText(_translate("SettingsDialog", "QT OpenGL environment"))
        self.BodyLabel_42.setText(_translate("SettingsDialog", "<html><head/><body><p><span style=\" color:#808080;\">Select Angle or Software to fix invisible menus or tooltips in the full screen.</span></p></body></html>"))
        self.BodyLabel_9.setText(_translate("SettingsDialog", "Full screen mode support"))
        self.BodyLabel_11.setText(_translate("SettingsDialog", "Animated scrolling support"))
        self.BodyLabel_13.setText(_translate("SettingsDialog", "Save and restore zoom factor"))
        self.BodyLabel_22.setText(_translate("SettingsDialog", "<html><head/><body><p><span style=\" color:#808080;\">When enabled, the application remembers the last zoom factor for your next session.</span></p></body></html>"))
        self.BodyLabel_2.setText(_translate("SettingsDialog", "Save and restore mini-player position"))
        self.BodyLabel_3.setText(_translate("SettingsDialog", "<html><head/><body><p><span style=\" color:#808080;\">When enabled, the mini-player will open at the last position it was moved to.</span></p></body></html>"))
        self.BodyLabel_6.setText(_translate("SettingsDialog", "Ad Blocker (Skipper)"))
        self.BodyLabel_12.setText(_translate("SettingsDialog", "Discord Rich Presence"))
        self.BodyLabel_18.setText(_translate("SettingsDialog", "Windows Thumbnail Buttons"))
        self.BodyLabel_20.setText(_translate("SettingsDialog", "System Tray App Icon"))
        self.BodyLabel_21.setText(_translate("SettingsDialog", "Track Change Notificator"))
        self.BodyLabel_23.setText(_translate("SettingsDialog", "Hotkey Playback Control"))
        self.BodyLabel_24.setText(_translate("SettingsDialog", "Only Audio Mode"))
        self.PushButton_2.setText(_translate("SettingsDialog", "Restart"))
        self.PrimaryPushButton.setText(_translate("SettingsDialog", "Save"))
        self.PushButton.setText(_translate("SettingsDialog", "Cancel"))
from qfluentwidgets import BodyLabel, ComboBox, HorizontalSeparator, LineEdit, PasswordLineEdit, PillPushButton, PrimaryPushButton, PushButton, ScrollArea, SwitchButton
