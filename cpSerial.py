import logging
import serial
from serial.tools import list_ports
from binascii import hexlify
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSignal, QString
from Console.consoleLogger import ConsoleLogger

class CpSerialBytes(bytearray):
    def __str__(self, *args, **kwargs):
        hexline = hexlify(self)
        n = 2
        pairs = [hexline[i:i+n] for i in range(0, len(hexline), n)]
        final = ("[{0:03}] ".format(len(self)) + " ".join(pairs)).upper()
        return final

class CpSerialService(QtCore.QThread):
    
    received = pyqtSignal(bytearray)
    portStateChanged = pyqtSignal(QString)
    portErrorOccured = pyqtSignal(QString)
    
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)
        self.logger = logging.getLogger('console')
        self.exiting = False
        self.sig_stop = False
        self.sig_portchange = False
        self.sig_portclose = False
        self.port_name = ''
        self.initSerial()
        self.running = False
        
    def __del__(self):
        self.sig_stop = True
        self.exiting = True
        self.wait()
        
    def initSerial(self):
        self.ser = serial.Serial()
        self.ser.timeout = 0
        self.ser.port = ""
        self.ser.baudrate = 38400
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        self.ser.bytesize = 8
        self.ser.xonxoff = 0
        self.ser.rtscts = 0
        
    
    def getPorts(self): 
        return list(list_ports.comports())
    
    def openPort(self, port):
        self.port_name = str(port)
        self.sig_portchange = True
        
    def closePort(self):
        self.sig_portclose = True
        
    def send(self, data):
        if self.ser.isOpen():
            self.logger.log(ConsoleLogger.SERIAL_SEND, CpSerialBytes(data))
            self.ser.write(data)
        
    def handle_close_port(self):
        # reset the flag
        self.sig_portclose = False
        try:
            if(self.ser.isOpen()):
                p = self.ser.port
                self.ser.close()
                self.logger.info('closed port ' + p)
                self.portStateChanged.emit('port closed') 
        except serial.SerialException, se:
            self.logger.error(str(se))
            self.portErrorOccured.emit(str(se)) 
        except serial.SerialTimeoutException, sto:
            self.logger.error(str(sto))
            self.portErrorOccured.emit(str(sto)) 
        except Exception, e:
            self.logger.error(str(e))
            self.portErrorOccured.emit(str(e))
        
        
    def handle_set_port(self):
        # reset the flag
        self.sig_portchange = False

        try:
            # sanity check here
            if(self.ser.isOpen()):
                self.ser.close()
                # allow port to settle
                self.msleep(100)
            # change the port and reopen
            self.ser.port = self.port_name
            self.ser.open()
            self.logger.info('opened port ' + self.port_name)
            self.portStateChanged.emit(self.port_name)
        except serial.SerialException, se:
            self.logger.error(str(se))
            self.portErrorOccured.emit(str(se)) 
        except serial.SerialTimeoutException, sto:
            self.logger.error(str(sto))
            self.portErrorOccured.emit(str(sto)) 
        except Exception, e:
            self.logger.error(str(e))
            self.portErrorOccured.emit(str(e)) 

    def start_service(self):
        
        self.running = True
        self.logger.info('starting CpSerialService...')
        
        data = CpSerialBytes()
        
        while self.sig_stop == False:

            # handle changing of port
            if(self.sig_portchange):
                self.logger.debug('sig_portchange')
                self.handle_set_port()
            
            # handle closing of port
            if(self.sig_portclose):
                self.logger.debug('sig_portclose')
                self.handle_close_port()
                
            # wait for user to signal to open port
            if (self.ser.isOpen() == False):
                self.msleep(500)
                continue
            
            # handle incoming data
            del data[:]
            while (self.ser.inWaiting() > 0):
                data.extend(self.ser.read(1))
    
            if len(data) > 0:
                # log and signal data received
                self.logger.log(ConsoleLogger.SERIAL_RECEIVE, data)
                self.received.emit(data)
            
            self.msleep(5)
        
        # shutdown the serial port
        self.handle_close_port()   
        # set flag 
        self.running = False
        
        self.logger.info('CpSerialService stopped!')

    def stop_service(self):
        self.sig_stop = True
        
    def run(self):
        self.start_service()
        
        

