# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mpy_efont.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(608, 435)
        icon = QIcon()
        icon.addFile(u"appicon.png", QSize(), QIcon.Normal, QIcon.Off)
        #icon = QIcon(QIcon.fromTheme(u"address-book-new"))
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.settingsBox = QGroupBox(self.centralWidget)
        self.settingsBox.setObjectName(u"settingsBox")
        self.settingsBox.setFlat(False)
        self.settingsBox.setCheckable(False)
        self.gridLayout_3 = QGridLayout(self.settingsBox)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.baudBox = QComboBox(self.settingsBox)
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.addItem("")
        self.baudBox.setObjectName(u"baudBox")
        self.baudBox.setEditable(True)
        self.baudBox.setMaxVisibleItems(8)

        self.gridLayout_3.addWidget(self.baudBox, 1, 1, 1, 1)

        self.portBox = QComboBox(self.settingsBox)
        self.portBox.setObjectName(u"portBox")

        self.gridLayout_3.addWidget(self.portBox, 0, 1, 1, 1)

        self.labelVFS = QLabel(self.settingsBox)
        self.labelVFS.setObjectName(u"labelVFS")

        self.gridLayout_3.addWidget(self.labelVFS, 3, 0, 1, 1)

        self.btnSelVFS = QPushButton(self.settingsBox)
        self.btnSelVFS.setObjectName(u"btnSelVFS")

        self.gridLayout_3.addWidget(self.btnSelVFS, 3, 2, 1, 1)

        self.reloadBtn = QPushButton(self.settingsBox)
        self.reloadBtn.setObjectName(u"reloadBtn")

        self.gridLayout_3.addWidget(self.reloadBtn, 0, 2, 1, 1)

        self.labelPort = QLabel(self.settingsBox)
        self.labelPort.setObjectName(u"labelPort")

        self.gridLayout_3.addWidget(self.labelPort, 0, 0, 1, 1)

        self.baudrateLabel = QLabel(self.settingsBox)
        self.baudrateLabel.setObjectName(u"baudrateLabel")

        self.gridLayout_3.addWidget(self.baudrateLabel, 1, 0, 1, 1)

        self.textFS = QLineEdit(self.settingsBox)
        self.textFS.setObjectName(u"textFS")

        self.gridLayout_3.addWidget(self.textFS, 3, 1, 1, 1)

        self.labelFW = QLabel(self.settingsBox)
        self.labelFW.setObjectName(u"labelFW")

        self.gridLayout_3.addWidget(self.labelFW, 2, 0, 1, 1)

        self.textFW = QLineEdit(self.settingsBox)
        self.textFW.setObjectName(u"textFW")

        self.gridLayout_3.addWidget(self.textFW, 2, 1, 1, 1)

        self.btnSelFW = QPushButton(self.settingsBox)
        self.btnSelFW.setObjectName(u"btnSelFW")

        self.gridLayout_3.addWidget(self.btnSelFW, 2, 2, 1, 1)

        self.labelPort.raise_()
        self.portBox.raise_()
        self.reloadBtn.raise_()
        self.baudrateLabel.raise_()
        self.baudBox.raise_()
        self.labelVFS.raise_()
        self.btnSelVFS.raise_()
        self.textFS.raise_()
        self.labelFW.raise_()
        self.textFW.raise_()
        self.btnSelFW.raise_()

        self.verticalLayout.addWidget(self.settingsBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnFSUpd = QPushButton(self.centralWidget)
        self.btnFSUpd.setObjectName(u"btnFSUpd")
        icon1 = QIcon()
        icon1.addFile(u"vfs.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnFSUpd.setIcon(icon1)
        self.btnFSUpd.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnFSUpd)

        self.btnFWUpd = QPushButton(self.centralWidget)
        self.btnFWUpd.setObjectName(u"btnFWUpd")
        icon2 = QIcon()
        icon2.addFile(u"firmware.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnFWUpd.setIcon(icon2)
        self.btnFWUpd.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btnFWUpd)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(self.centralWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textLog = QPlainTextEdit(self.groupBox)
        self.textLog.setObjectName(u"textLog")

        self.verticalLayout_2.addWidget(self.textLog)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.clearTextBtn = QPushButton(self.groupBox)
        self.clearTextBtn.setObjectName(u"clearTextBtn")

        self.horizontalLayout_2.addWidget(self.clearTextBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.groupBox)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 608, 26))
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        self.clearTextBtn.clicked.connect(self.textLog.clear)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"eFontTool", None))
        self.settingsBox.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.baudBox.setItemText(0, QCoreApplication.translate("MainWindow", u"4800", None))
        self.baudBox.setItemText(1, QCoreApplication.translate("MainWindow", u"9600", None))
        self.baudBox.setItemText(2, QCoreApplication.translate("MainWindow", u"19200", None))
        self.baudBox.setItemText(3, QCoreApplication.translate("MainWindow", u"38400", None))
        self.baudBox.setItemText(4, QCoreApplication.translate("MainWindow", u"57600", None))
        self.baudBox.setItemText(5, QCoreApplication.translate("MainWindow", u"74880", None))
        self.baudBox.setItemText(6, QCoreApplication.translate("MainWindow", u"115200", None))
        self.baudBox.setItemText(7, QCoreApplication.translate("MainWindow", u"230400", None))
        self.baudBox.setItemText(8, QCoreApplication.translate("MainWindow", u"250000", None))
        self.baudBox.setItemText(9, QCoreApplication.translate("MainWindow", u"460800", None))
        self.baudBox.setItemText(10, QCoreApplication.translate("MainWindow", u"921600", None))

        self.baudBox.setCurrentText(QCoreApplication.translate("MainWindow", u"921600", None))
        self.labelVFS.setText(QCoreApplication.translate("MainWindow", u"FileSystem:", None))
        self.btnSelVFS.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.reloadBtn.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.labelPort.setText(QCoreApplication.translate("MainWindow", u"COM Port:", None))
        self.baudrateLabel.setText(QCoreApplication.translate("MainWindow", u"Baudrate:", None))
        self.labelFW.setText(QCoreApplication.translate("MainWindow", u"Firmware:", None))
        self.btnSelFW.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.btnFSUpd.setText(QCoreApplication.translate("MainWindow", u"Upload FS", None))
        self.btnFWUpd.setText(QCoreApplication.translate("MainWindow", u"Upload FW", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
        self.clearTextBtn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
    # retranslateUi

