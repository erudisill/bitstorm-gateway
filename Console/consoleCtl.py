'''
Created on Dec 2, 2014

@author: ericrudisill
'''
from PyQt4 import QtGui
from Console.consoleView import Ui_ConsoleView
from appMessage import AppMessage

class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):

    def __init__(self, serial):
        QtGui.QMainWindow.__init__(self)
        
        self.setupUi(self)
        
        self.serial = serial
        self.serial.received.connect(self.logText)
        
        self.setupComboPorts()
        
        self.buttonOpenPort.clicked.connect(self.openPort)
        self.pushButton.clicked.connect(self.testMessage)

    def show(self, *args, **kwargs):
        self.serial.start()
        return QtGui.QMainWindow.show(self, *args, **kwargs)
    
    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.comboPorts.addItem(port[0])
                
    def openPort(self):
        self.serial.openPort(self.comboPorts.currentText())
        
    def testMessage(self):
        test = bytearray([ 0x01,0x02,0x80,0x70,0x60,0x50,0x40,0x30,0x20,0x10,0x00,0xf0,0x0e,0x80,0x70,0x60,0x50,0x40,0x30,0x20,0x10,0x00,0xf0,0x0e,0xa,0xf0,0x0e,0x0b,0x0c,0x0d,0x04,0x03,0x02,0x01,0x04,0x03,0x02,0x01,0xff ])
        msg = AppMessage(test) 
        self.logText(str(msg))
        
    def logText(self, text):
        self.textLog.append(text)   
     
    def logRecord(self, record):
        self.logText(record.getMessage())