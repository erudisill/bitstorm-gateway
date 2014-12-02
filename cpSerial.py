'''
Created on Dec 2, 2014

@author: ericrudisill
'''
from PyQt4 import QtCore
from PyQt4.Qt import pyqtSignal, QString
from serial.tools import list_ports

class CpSerial(QtCore.QThread):
    
    received = pyqtSignal(QString)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.sig_stop = False
        
    def run(self):
        print 'CpSerial starting...'
        while self.sig_stop == False:
            self.sleep(1)
            self.received.emit('hello')
        print 'CpSerial stopping...'
        
    def quit(self):
        super(CpSerial, self).quit()
        self.sig_stop = True
        
    def getPorts(self):
        return list(list_ports.comports())
    
    def openPort(self, portName):
        self.received.emit('Opening port: %s' % portName)
