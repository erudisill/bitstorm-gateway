'''
Created on Dec 2, 2014

@author: ericrudisill
'''
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSignal
from serial.tools import list_ports
import logging
from binascii import hexlify

class CpSerialBytes(bytearray):
    def __str__(self, *args, **kwargs):
        hexline = hexlify(self)
        n = 2
        pairs = [hexline[i:i+n] for i in range(0, len(hexline), n)]
        final = ("[{0:03}] ".format(len(self)) + " ".join(pairs)).upper()
        return final

class CpSerial(QtCore.QThread):
    
    received = pyqtSignal(bytearray)

    def __init__(self):
        QtCore.QThread.__init__(self)       
        self.sig_stop = False
        self.logger = logging.getLogger('console')
                
    def run(self):        
        self.logger.info('CpSerial starting...')
        while self.sig_stop == False:
            self.sleep(1)
            self.received.emit(CpSerialBytes([ 'h', 'e', 'l', 'l', 'o', 0xab, 0xcd ]))
        self.logger.info('CpSerial stopping...')
        
    def quit(self):
        super(CpSerial, self).quit()
        self.sig_stop = True
        
    def getPorts(self):
        return list(list_ports.comports())
    
    def openPort(self, portName):
        self.logger.info('Opening port: %s' % portName)
