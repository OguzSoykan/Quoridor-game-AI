# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(489, 287)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.player1Label = QLabel(self.centralwidget)
        self.player1Label.setObjectName(u"player1Label")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        self.player1Label.setFont(font)

        self.gridLayout.addWidget(self.player1Label, 0, 2, 1, 1)

        self.player2Image = QLabel(self.centralwidget)
        self.player2Image.setObjectName(u"player2Image")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player2Image.sizePolicy().hasHeightForWidth())
        self.player2Image.setSizePolicy(sizePolicy)
        self.player2Image.setMinimumSize(QSize(100, 100))
        self.player2Image.setMaximumSize(QSize(100, 100))
        self.player2Image.setScaledContents(True)
        self.player2Image.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.player2Image, 1, 1, 1, 1)

        self.player1Image = QLabel(self.centralwidget)
        self.player1Image.setObjectName(u"player1Image")
        sizePolicy.setHeightForWidth(self.player1Image.sizePolicy().hasHeightForWidth())
        self.player1Image.setSizePolicy(sizePolicy)
        self.player1Image.setMinimumSize(QSize(100, 100))
        self.player1Image.setMaximumSize(QSize(100, 100))
        self.player1Image.setScaledContents(True)
        self.player1Image.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.player1Image, 0, 1, 1, 1)

        self.player2Box = QComboBox(self.centralwidget)
        icon = QIcon(QIcon.fromTheme(u"face-smile"))
        self.player2Box.addItem(icon, "")
        icon1 = QIcon(QIcon.fromTheme(u"applications-games"))
        self.player2Box.addItem(icon1, "")
        self.player2Box.setObjectName(u"player2Box")

        self.gridLayout.addWidget(self.player2Box, 1, 3, 1, 1)

        self.player2Label = QLabel(self.centralwidget)
        self.player2Label.setObjectName(u"player2Label")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(False)
        self.player2Label.setFont(font1)

        self.gridLayout.addWidget(self.player2Label, 1, 2, 1, 1)

        self.botImage1 = QLabel(self.centralwidget)
        self.botImage1.setObjectName(u"botImage1")
        sizePolicy.setHeightForWidth(self.botImage1.sizePolicy().hasHeightForWidth())
        self.botImage1.setSizePolicy(sizePolicy)
        self.botImage1.setMinimumSize(QSize(50, 50))
        self.botImage1.setMaximumSize(QSize(50, 50))
        self.botImage1.setScaledContents(True)
        self.botImage1.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.botImage1, 0, 4, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setStyleSheet(u"QPushButton {font-weight: bold; font-size: 10pt; border-style: outset; border-width: 2px; border-radius: 6px; background-color: lavenderblush; border-color: rgb(0, 123, 255)}\n"
"QPushButton:pressed {font-weight: bold; font-size: 8pt; border-style: inset; border-width: 3px; background-color: lavenderblush; border-color: rgb(255, 193, 7);}")

        self.horizontalLayout.addWidget(self.startButton)

        self.exitButton = QPushButton(self.centralwidget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setStyleSheet(u"QPushButton {font-weight: bold; font-size: 10pt; border-style: outset; border-width: 2px; border-radius: 6px; background-color: lavenderblush; border-color: rgb(0, 123, 255)}\n"
"QPushButton:pressed {font-weight: bold; font-size: 8pt; border-style: inset; border-width: 3px; background-color: lavenderblush; border-color: red;}")

        self.horizontalLayout.addWidget(self.exitButton)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 3)

        self.botImage2 = QLabel(self.centralwidget)
        self.botImage2.setObjectName(u"botImage2")
        sizePolicy.setHeightForWidth(self.botImage2.sizePolicy().hasHeightForWidth())
        self.botImage2.setSizePolicy(sizePolicy)
        self.botImage2.setMinimumSize(QSize(50, 50))
        self.botImage2.setMaximumSize(QSize(50, 50))
        self.botImage2.setScaledContents(True)
        self.botImage2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.botImage2, 1, 4, 1, 1)

        self.player1Box = QComboBox(self.centralwidget)
        self.player1Box.addItem(icon, "")
        self.player1Box.addItem(icon1, "")
        self.player1Box.setObjectName(u"player1Box")
        self.player1Box.setEnabled(True)

        self.gridLayout.addWidget(self.player1Box, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(46, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Quoridor Game", None))
        self.player1Label.setText(QCoreApplication.translate("MainWindow", u"Player 1", None))
        self.player2Image.setText(QCoreApplication.translate("MainWindow", u"Player2Image", None))
        self.player1Image.setText(QCoreApplication.translate("MainWindow", u"Player1Image", None))
        self.player2Box.setItemText(0, QCoreApplication.translate("MainWindow", u"Human", None))
        self.player2Box.setItemText(1, QCoreApplication.translate("MainWindow", u"Bot", None))

        self.player2Label.setText(QCoreApplication.translate("MainWindow", u"Player 2", None))
        self.botImage1.setText("")
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.botImage2.setText("")
        self.player1Box.setItemText(0, QCoreApplication.translate("MainWindow", u"Human", None))
        self.player1Box.setItemText(1, QCoreApplication.translate("MainWindow", u"Bot", None))

    # retranslateUi

