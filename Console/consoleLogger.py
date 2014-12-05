'''
Created on Dec 3, 2014

@author: ericrudisill

Used as a bridge between the Python logging service and a Qt widget/window/object.

'''

import logging
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSignal

class ConsoleLoggerFormatter(logging.Formatter):
    
    standardDateFmt = '%H:%M:%S'
    standardFmt = '%(asctime)s %(message)s'
    serialSendFmt = '%(asctime)s [SND] %(message)s'
    serialReceiveFmt = '%(asctime)s [RCV] %(message)s'
    
    def __init__(self):
        logging.Formatter.__init__(self)
    
    def format(self, record):
        self.datefmt = self.standardDateFmt    

        if record.levelno == ConsoleLogger.SERIAL_SEND:
            self._fmt = self.serialSendFmt    
        elif record.levelno == ConsoleLogger.SERIAL_RECEIVE:
            self._fmt = self.serialReceiveFmt
        else:
            self._fmt = self.standardFmt
            
        return super(ConsoleLoggerFormatter, self).format(record)
            

class ConsoleLogger(logging.Handler, QtCore.QObject):
    
    SERIAL_SEND = 25
    SERIAL_RECEIVE = 26
    
    log = pyqtSignal(logging.LogRecord)
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        logging.Handler.__init__(self)
        fmt = ConsoleLoggerFormatter()
        self.setFormatter(fmt)
        
    def emit(self, record):
        record.message = self.format(record)
        self.log.emit(record)
        
