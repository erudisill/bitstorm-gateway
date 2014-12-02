# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Console/consoleView.ui'
#
# Created: Tue Dec  2 14:56:08 2014
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
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.textLog = QtGui.QTextEdit(self.centralwidget)
        self.textLog.setObjectName(_fromUtf8("textLog"))
        self.verticalLayout.addWidget(self.textLog)
        ConsoleView.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(ConsoleView)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ConsoleView.setStatusBar(self.statusbar)

        self.retranslateUi(ConsoleView)
        QtCore.QMetaObject.connectSlotsByName(ConsoleView)

    def retranslateUi(self, ConsoleView):
        ConsoleView.setWindowTitle(_translate("ConsoleView", "MainWindow", None))
        self.groupBox.setTitle(_translate("ConsoleView", "Serial", None))
        self.buttonOpenPort.setText(_translate("ConsoleView", "Open Port", None))
        self.groupBox_2.setTitle(_translate("ConsoleView", "GroupBox", None))
        self.pushButton.setText(_translate("ConsoleView", "PushButton", None))

