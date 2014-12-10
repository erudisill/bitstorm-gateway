# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Console/consoleView.ui'
#
# Created: Wed Dec 10 12:51:23 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ConsoleView(object):
    def setupUi(self, ConsoleView):
        ConsoleView.setObjectName(_fromUtf8("ConsoleView"))
        ConsoleView.resize(947, 703)
        self.centralwidget = QtGui.QWidget(ConsoleView)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboPorts = QtGui.QComboBox(self.groupBox)
        self.comboPorts.setObjectName(_fromUtf8("comboPorts"))
        self.horizontalLayout_2.addWidget(self.comboPorts)
        self.buttonOpenPort = QtGui.QPushButton(self.groupBox)
        self.buttonOpenPort.setObjectName(_fromUtf8("buttonOpenPort"))
        self.horizontalLayout_2.addWidget(self.buttonOpenPort)
        self.buttonClosePort = QtGui.QPushButton(self.groupBox)
        self.buttonClosePort.setObjectName(_fromUtf8("buttonClosePort"))
        self.horizontalLayout_2.addWidget(self.buttonClosePort)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonGetMAC = QtGui.QPushButton(self.groupBox_2)
        self.buttonGetMAC.setObjectName(_fromUtf8("buttonGetMAC"))
        self.horizontalLayout.addWidget(self.buttonGetMAC)
        self.buttonTest = QtGui.QPushButton(self.groupBox_2)
        self.buttonTest.setObjectName(_fromUtf8("buttonTest"))
        self.horizontalLayout.addWidget(self.buttonTest)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lineData = QtGui.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(12)
        self.lineData.setFont(font)
        self.lineData.setObjectName(_fromUtf8("lineData"))
        self.horizontalLayout_5.addWidget(self.lineData)
        self.buttonSend = QtGui.QPushButton(self.centralwidget)
        self.buttonSend.setObjectName(_fromUtf8("buttonSend"))
        self.horizontalLayout_5.addWidget(self.buttonSend)
        self.checkHex = QtGui.QCheckBox(self.centralwidget)
        self.checkHex.setObjectName(_fromUtf8("checkHex"))
        self.horizontalLayout_5.addWidget(self.checkHex)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.textLog = QtGui.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monaco"))
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.textLog.setFont(font)
        self.textLog.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textLog.setReadOnly(True)
        self.textLog.setTabStopWidth(60)
        self.textLog.setObjectName(_fromUtf8("textLog"))
        self.verticalLayout.addWidget(self.textLog)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.checkPaused = QtGui.QCheckBox(self.centralwidget)
        self.checkPaused.setObjectName(_fromUtf8("checkPaused"))
        self.horizontalLayout_3.addWidget(self.checkPaused)
        self.checkBleAscii = QtGui.QCheckBox(self.centralwidget)
        self.checkBleAscii.setObjectName(_fromUtf8("checkBleAscii"))
        self.horizontalLayout_3.addWidget(self.checkBleAscii)
        self.checkDecodeCobs = QtGui.QCheckBox(self.centralwidget)
        self.checkDecodeCobs.setObjectName(_fromUtf8("checkDecodeCobs"))
        self.horizontalLayout_3.addWidget(self.checkDecodeCobs)
        self.checkHideBytes = QtGui.QCheckBox(self.centralwidget)
        self.checkHideBytes.setObjectName(_fromUtf8("checkHideBytes"))
        self.horizontalLayout_3.addWidget(self.checkHideBytes)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.buttonClear = QtGui.QPushButton(self.centralwidget)
        self.buttonClear.setObjectName(_fromUtf8("buttonClear"))
        self.horizontalLayout_3.addWidget(self.buttonClear)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        ConsoleView.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(ConsoleView)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ConsoleView.setStatusBar(self.statusbar)

        self.retranslateUi(ConsoleView)
        QtCore.QMetaObject.connectSlotsByName(ConsoleView)

    def retranslateUi(self, ConsoleView):
        ConsoleView.setWindowTitle(_translate("ConsoleView", "MainWindow", None))
        self.groupBox.setTitle(_translate("ConsoleView", "Serial", None))
        self.buttonOpenPort.setText(_translate("ConsoleView", "Open", None))
        self.buttonClosePort.setText(_translate("ConsoleView", "Close", None))
        self.groupBox_2.setTitle(_translate("ConsoleView", "Commands", None))
        self.buttonGetMAC.setText(_translate("ConsoleView", "Get MAC", None))
        self.buttonTest.setText(_translate("ConsoleView", "Test", None))
        self.buttonSend.setText(_translate("ConsoleView", "Send", None))
        self.checkHex.setText(_translate("ConsoleView", "as hex", None))
        self.checkPaused.setText(_translate("ConsoleView", "Paused", None))
        self.checkBleAscii.setText(_translate("ConsoleView", "BLE ASCII", None))
        self.checkDecodeCobs.setText(_translate("ConsoleView", "Decode COBS", None))
        self.checkHideBytes.setText(_translate("ConsoleView", "Hide Bytes", None))
        self.buttonClear.setText(_translate("ConsoleView", "Clear", None))

