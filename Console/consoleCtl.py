'''
Created on Dec 2, 2014

@author: ericrudisill
'''
from PyQt4 import QtGui
from PyQt4.Qt import pyqtSignal, QString
from Console.consoleView import Ui_ConsoleView

class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):

    openPort = pyqtSignal(QString)

    def __init__(self, serial):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.serial = serial
        self.serial.received.connect(self.logText)
        
        self.setupComboPorts()
        self.buttonOpenPort.clicked.connect(self.handleButton)

    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.comboPorts.addItem(port[0])
                
    def handleButton(self):
        self.serial.openPort(self.comboPorts.currentText())
        
    def logText(self, text):
        self.textLog.append(text)     