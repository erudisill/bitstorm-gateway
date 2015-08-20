'''
Created on Dec 2, 2014

@author: ericrudisill
'''
import logging
import binascii
import time
from cobs import cobs
from PyQt4 import QtGui
from PyQt4.Qt import Qt, pyqtSignal, QString
from Console.consoleView import Ui_ConsoleView
from appMessage import AppMessage
from cpSerial import CpSerialBytes
from Console.consoleLogger import ConsoleLogger
from Devices.deviceTable import DeviceTable
from statusMessage import StatusMessage

class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):

    ble_ascii_received = pyqtSignal(bytearray)

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
        self.buttonClear.clicked.connect(self.clearLog)
        
        # Setup unique application commands/buttons
        self.setupCommands()
        
        self.file = None
               

    def show(self, *args, **kwargs):
        self.serial.start()
        return QtGui.QMainWindow.show(self, *args, **kwargs)
    
    def logRecord(self, record):
        if self.checkPaused.isChecked():
            if record.levelno < logging.WARNING:
                return
        
        if record.levelno == ConsoleLogger.SERIAL_SEND or \
           record.levelno == ConsoleLogger.SERIAL_RECEIVE:
            if self.checkHideBytes.isChecked():
                return
            
        # Apply filter
        if str(self.lineFilter.text()) not in record.message:
        	return;
        
        color = 'gray'
        if record.levelno == ConsoleLogger.SERIAL_SEND:
            color = 'black'
        elif record.levelno == ConsoleLogger.SERIAL_RECEIVE:
            color = 'black'
        elif record.levelno == logging.ERROR:
            color = 'red'
            
        self.textLog.append('<font color="' + color + '">' + record.message + '</font>') 
        if self.file:  
	        self.file.write(record.message + "\n");

    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.comboPorts.addItem(port[0])
                
    def openPort(self):
        self.filename = time.strftime("%Y%m%d-%H%M%S") + ".log"
        self.file = open(self.filename, 'w')
        self.serial.openPort(self.comboPorts.currentText())
        
    def closePort(self):
        self.serial.closePort()
        self.file = open(self.filename, 'w')
       
    def sendData(self):
        if self.checkHex.isChecked():
            data = binascii.unhexlify(str(self.lineData.text()).replace(' ', ''))
        else:
            data = bytearray(str(self.lineData.text()))
        self.serial.send(data)
        
    def clearLog(self):
        self.textLog.setText("")
      
####################################################################
# Add custom logic for protocol commands (buttons) here.
####################################################################
    
    def setupCommands(self):
        self.buttonGetMAC.clicked.connect(self.getMac)
        self.buttonRSSI.clicked.connect(self.openDeviceTable)
    
    def serialReceived(self, data):
        if self.checkDecodeCobs.isChecked():
            # Collect bytes till we see a \0, then decode the COBS frame
            for b in data:
                if b == 0:
                    try:
                        decoded = bytearray(cobs.decode(buffer(self.serial_buffer)))
                        #self.logger.info('[COB] ' + str(CpSerialBytes(decoded)))
                        self.parseCobsRecord(decoded)
                    except Exception, e:
                        self.logger.error(str(e))
                        self.logger.error(str(CpSerialBytes(self.serial_buffer)))
                    del self.serial_buffer[:]
                else:
                    self.serial_buffer.append(b)
        elif self.checkBleAscii.isChecked():
            for b in data:
                if b==0x0A:
                    self.parseBleAsciiRecord(self.serial_buffer)
                    del self.serial_buffer[:]
                else:
                    self.serial_buffer.append(b)

    def getMac(self):
        cmd = bytearray([ 0x02, 0x04, 0xff ])
        self.serial.send(cmd)

    def openDeviceTable(self):
        try:
            self.devicesTable.show()
        except:
            self.devicesTable = DeviceTable(self)
            self.devicesTable.show()

    
    def parseCobsRecord(self, data):
        if data[0] == 0xAB and data[1] == 0xAB:
            msg = StatusMessage(data)
            self.logger.info(str(msg))
        elif data[0] == 0x01:
            msg = AppMessage(data)
            self.logger.info(str(msg))
        
    def parseBleAsciiRecord(self, data):
        f = str(self.lineFilter.text()).strip()
        if len(f) > 0:
            if not f in str(data):
                return
        self.ble_ascii_received.emit(data)
        self.logger.info(str(data))
        
        