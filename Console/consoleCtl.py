'''
Created on Dec 2, 2014

@author: ericrudisill
'''
import logging
import binascii
from PyQt4 import QtGui
from Console.consoleView import Ui_ConsoleView

class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):

    def __init__(self, serial):
        QtGui.QMainWindow.__init__(self)
        self.logger = logging.getLogger('console')
        self.setupUi(self)
        
        # Connect CpSerialService to ourselves
        self.serial = serial
        self.serial.received.connect(self.serialReceived)
        
        self.setupComboPorts()
        
        # Wire the signals/slots
        self.buttonOpenPort.clicked.connect(self.openPort)
        self.buttonSend.clicked.connect(self.sendData)
        
        # Setup unique application commands/buttons
        self.setupCommands()

    def show(self, *args, **kwargs):
        self.serial.start()
        return QtGui.QMainWindow.show(self, *args, **kwargs)
    
    def logRecord(self, record):
        self.textLog.append(record.message)   

    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.comboPorts.addItem(port[0])
                
    def openPort(self):
        self.serial.openPort(self.comboPorts.currentText())
       
    def sendData(self):
        if self.checkHex.isChecked():
            data = binascii.unhexlify(str(self.lineData.text()).replace(' ', ''))
        else:
            data = bytearray(str(self.lineData.text()))
        self.serial.send(data)
      
####################################################################
# Add custom logic for protocol commands (buttons) here.
####################################################################
    
    def setupCommands(self):
        self.buttonGetMAC.clicked.connect(self.getMac)
    
    def serialReceived(self, data):
        # Do nothing for now. Logging happens via logger
        pass

    def getMac(self):
        cmd = bytearray([ 0x02, 0x04, 0xff ])
        self.serial.send(cmd)

        
        
        
        
        
        