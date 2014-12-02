'''
Created on Dec 2, 2014

@author: ericrudisill
'''
from PyQt4  import QtGui
from Console.consoleCtl import ConsoleCtl
from cpSerial import CpSerial
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    serialThread = CpSerial()
    serialThread.start()
    
    console = ConsoleCtl(serialThread)
    console.show()

    app.exec_()
    
    serialThread.quit()
    serialThread.wait(5000)
    
    sys.exit()