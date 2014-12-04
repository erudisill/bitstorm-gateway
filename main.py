'''
Created on Dec 2, 2014

@author: ericrudisill
'''
from PyQt4  import QtGui
from Console.consoleCtl import ConsoleCtl
from cpSerial import CpSerial
import logging
from Console.consoleLogger import ConsoleLogger
        
if __name__ == '__main__':
    import sys

    # Init logging system early
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(None)
    logging.info('Log started')
   
    # Main serial service
    serialService = CpSerial()

    # Init Qt and the main window
    app = QtGui.QApplication(sys.argv)
    console = ConsoleCtl(serialService)

    # Now create the ConsoleLogger bridge and connect
    x = ConsoleLogger()
    logger.addHandler(x)
    x.log.connect(console.logRecord)

    # Let the show begin!
    console.show()

    # Spin...
    app.exec_()
    
    # All done, shut the serial service down
    serialService.quit()
    serialService.wait(5000)
    
    # Good bye
    sys.exit()