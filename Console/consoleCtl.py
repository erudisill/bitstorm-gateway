'''
Created on Dec 2, 2014

@author: ericrudisill
'''
import logging
import binascii
from cobs import cobs
from PyQt4 import QtGui
from PyQt4.Qt import Qt
from Console.consoleView import Ui_ConsoleView
from appMessage import AppMessage
from cpSerial import CpSerialBytes
from Console.consoleLogger import ConsoleLogger

class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):

    def __init__(self, serial):
        QtGui.QMainWindow.__init__(self)
        self.logger = logging.getLogger('console')
        self.setupUi(self)
        
        # Connect CpSerialService to ourselves
        # Explicitly set Qt.QueuedConnection to ensure the separate thread
        # emits its signal into a Qt queue for processing
        self.serial = serial
        self.serial_buffer = bytearray()
        self.serial.received.connect(self.serialReceived, Qt.QueuedConnection)
        
        self.setupComboPorts()
        
        # Wire the signals/slots
        self.buttonOpenPort.clicked.connect(self.openPort)
        self.buttonClosePort.clicked.connect(self.closePort)
        self.buttonSend.clicked.connect(self.sendData)
        
        # Setup unique application commands/buttons
        self.setupCommands()
               

    def show(self, *args, **kwargs):
        self.serial.start()
        return QtGui.QMainWindow.show(self, *args, **kwargs)
    
    def logRecord(self, record):
        color = 'gray'
        if record.levelno == ConsoleLogger.SERIAL_SEND:
            color = 'black'
        elif record.levelno == ConsoleLogger.SERIAL_RECEIVE:
            color = 'black'
        elif record.levelno == logging.ERROR:
            color = 'red'
        self.textLog.append('<font color="' + color + '">' + record.message + '</font>')   

    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.comboPorts.addItem(port[0])
                
    def openPort(self):
        self.serial.openPort(self.comboPorts.currentText())
        
    def closePort(self):
        self.serial.closePort()
       
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
        self.buttonTest.clicked.connect(self.testCobs)
    
    def serialReceived(self, data):
        # Collect bytes till we see a \0 .. All data should be COBS encoded
        for b in data:
            if b == 0:
                try:
                    decoded = bytearray(cobs.decode(buffer(self.serial_buffer)))
                    self.logger.info('[COB] ' + str(CpSerialBytes(decoded)))
                    self.parseRecord(decoded)
                except Exception, e:
                    self.logger.error(str(e))
                    self.logger.error(str(CpSerialBytes(self.serial_buffer)))
                del self.serial_buffer[:]
            else:
                self.serial_buffer.append(b)

    def getMac(self):
        cmd = bytearray([ 0x02, 0x04, 0xff ])
        self.serial.send(cmd)

    def testCobs(self):
        del self.serial_buffer[:]
        # We recieve a bytearray from serial
        test = bytearray([ 0x01,0x02,0x80,0x70,0x60,0x50,0x40,0x30,0x20,0x10,0x00,0xf0,0x0e,0x80,0x70,0x60,0x50,0x40,0x30,0x20,0x10,0x00,0xf0,0x0e,0xa,0xf0,0x0e,0x0b,0x0c,0x0d,0x04,0x03,0x02,0x01,0x04,0x03,0x02,0x01,0xff ])
        # cobs wants a buffer instead, plus a \0 at the end
        cobs_test = cobs.encode(buffer(test))
        # now back to a bytearray for serialReceived
        data = bytearray(cobs_test)
        data.extend([0x00])
        self.serialReceived(data)
        
    def parseRecord(self, data):
        if data[0] == 0x01:
            msg = AppMessage(data)
            self.logger.info(str(msg))
        
        
        