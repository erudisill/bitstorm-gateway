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
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')
    logger = logging.getLogger(None)
    logger.setLevel(logging.DEBUG)
    logging.info('Log started')
   
    # Main serial service
    serialService = CpSerial()

    # Init Qt and the main window
    app = QtGui.QApplication(sys.argv)
    console = ConsoleCtl(serialService)

    # Now create the ConsoleLogger bridge and connect
    x = ConsoleLogger()
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    x.setFormatter(formatter)
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