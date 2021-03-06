'''
Created on Dec 2, 2014

@author: ericrudisill
'''
import logging
from PyQt4  import QtGui
from Console.consoleCtl import ConsoleCtl
from cpSerial import CpSerialService
from Console.consoleLogger import ConsoleLogger
        
if __name__ == '__main__':
    import sys

    # Main serial service
    serialService = CpSerialService()

    # Init Qt and the main window
    app = QtGui.QApplication(sys.argv)
    console = ConsoleCtl(serialService)

    # Now create the ConsoleLogger bridge and connect
    logger = logging.getLogger('console')
    logger.setLevel(logging.DEBUG)
    x = ConsoleLogger()
    logger.addHandler(x)
    x.log.connect(console.logRecord)

    # Let the show begin!
    console.show()

    # Spin...
    app.exec_()
    
    # All done, shut the serial service down
    serialService.stop_service()
    serialService.wait(5000)
    
    # Good bye
    sys.exit()