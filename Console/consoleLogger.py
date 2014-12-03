'''
Created on Dec 3, 2014

@author: ericrudisill

Used as a bridge between the Python logging service and a Qt widget/window/object.

'''

import logging
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSignal

class ConsoleLogger(logging.Handler, QtCore.QObject):

    log = pyqtSignal(logging.LogRecord)
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        logging.Handler.__init__(self)
        fmt = logging.Formatter('%(levelname)s:%(message)s')
        self.setFormatter(fmt)
        
    def emit(self, record):
        self.log.emit(record)
        
