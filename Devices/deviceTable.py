'''
Created on Dec 10, 2014

@author: ericrudisill
'''
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QTableWidget, QTableWidgetItem

class DeviceTable(QtGui.QDialog):

    def __init__(self, parent=None):
        super(DeviceTable, self).__init__(parent)
        
        self.resize(640,480)
        
        self.table = QTableWidget()  
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['MAC','RSSI','RSSI','Battery'])
        
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.table)
        
        self.parent().ble_ascii_received.connect(self.bleAsciiReceived)
        
    def bleAsciiReceived(self, data):
        parts = str(data).split(" ")
        mac = parts[0].replace("*","")
        rssi = parts[1]
        battery = parts[3]
        items = self.table.findItems(mac, QtCore.Qt.MatchExactly)
        t = lambda x: int(x, 16) - ((int(x, 16) >> 7) * 256)
        if len(items) > 0:
            row = items[0].row()
            self.table.setItem(row, 1, QTableWidgetItem(rssi))
            self.table.setItem(row, 2, QTableWidgetItem(str(t(rssi))))
            self.table.setItem(row, 3, QTableWidgetItem(battery))
        else:
            self.table.setRowCount(self.table.rowCount() + 1)
            row = self.table.rowCount() - 1
            self.table.setItem(row, 0, QTableWidgetItem(mac))
            self.table.setItem(row, 1, QTableWidgetItem(rssi))
            self.table.setItem(row, 2, QTableWidgetItem(str(t(rssi))))
            self.table.setItem(row, 3, QTableWidgetItem(battery))
            self.table.sortItems(0)