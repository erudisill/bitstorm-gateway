'''
Created on Dec 10, 2014

@author: ericrudisill
'''
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QTableWidget, QTableWidgetItem, QLabel, QSlider, QStatusBar,\
    QSpinBox, QPushButton
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import binascii
import struct
import math
import time
import logging
import os
import random

class BleRecord():
    def __init__(self, data):
        self.data = data
        self.parts = str(data).split(" ")
        self.mac = self.parts[0].replace("*","")
        self.rssi_hex = self.parts[1]
        self.rssi_dec = struct.unpack('b', binascii.unhexlify(self.rssi_hex))[0]
        self.battery = self.parts[3]
        self.timestamp = time.time()
        
    def distance(self, A, n, rssi=None):
        # http://stupidembeddedblog.blogspot.com/2014/05/estimating-distance-from-rssi-values.html
        if rssi == None:
            rssi = self.rssi_dec
        return math.pow(10.0, ((A + (-rssi))/(10.0*n)))
    
    def __str__(self, *args, **kwargs):
        return str(self.timestamp) + "\t" +         \
                str(self.data) + "\t" +             \
                str(self.mac) + "\t" +              \
                str(self.rssi_hex) + "\t" +         \
                str(self.rssi_dec) + "\t" +         \
                str(self.battery)
    
class BleRecordSummary():
    def __init__(self, record):
        self.last_record = record
        self.mac = record.mac
        self.rssi_feedback = record.rssi_dec
        self.count = 1
        self.feedback_v = 0.65
        
    def update(self, record):
        self.last_record = record
        self.count = self.count + 1
        self._update_filters(record.rssi_dec)
        
    def _update_filters(self, rssi_dec):
        # Update feedback filter
        self.rssi_feedback = (self.feedback_v * self.rssi_feedback) + ((1-self.feedback_v) * rssi_dec)
        

class DeviceTable(QtGui.QDialog):

    def __init__(self, parent=None):
        super(DeviceTable, self).__init__(parent)

        self.logger = logging.getLogger('console')
        
        self.records = {}
        
        self.resize(800,800)
        
        self.label_a = QLabel()
        self.label_a.setText("A: ")
        self.spinbox_a = QSpinBox()
        self.spinbox_a.setRange(-103,-38)
        self.spinbox_a.setValue(-41)
        self.spinbox_a.valueChanged.connect(self.spinboxChanged)
        self.spinboxChanged(self.spinbox_a.value())
        
        self.slider_label = QLabel()
        self.slider_label.setText("   n:")
        self.slider = QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 40)
        self.slider.setValue(22)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.sliderChanged)
        self.sliderChanged(self.slider.value())
        
        self.button_reset = QPushButton()
        self.button_reset.setText("Reset")
        self.button_reset.clicked.connect(self.reset)
        
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.addWidget(self.label_a)
        self.horizontalLayout.addWidget(self.spinbox_a)
        self.horizontalLayout.addWidget(self.slider_label)
        self.horizontalLayout.addWidget(self.slider)
        self.horizontalLayout.addWidget(self.button_reset)
        
        self.table = QTableWidget()  
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['MAC','Count','RSSI','RSSI','Distance','RSSI_F', 'DIST_F','Battery'])
        
        # matplotlib stuff
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.buttonPlot = QPushButton('Plot')
        self.buttonPlot.clicked.connect(self.plot)
        self.plot_layout = QtGui.QVBoxLayout()
        self.plot_layout.addWidget(self.toolbar)
        self.plot_layout.addWidget(self.canvas)
        self.plot_layout.addWidget(self.buttonPlot)
        self.ax = self.figure.add_subplot(111)
        self.ax.hold(False)

                
        self.statusbar = QStatusBar()
        self.statusbar.showMessage('Opening log file')
        
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.addWidget(self.table)
        self.verticalLayout.addLayout(self.plot_layout)
        self.verticalLayout.addWidget(self.statusbar)
        
        self.mainLayout = QtGui.QVBoxLayout(self)
        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addLayout(self.verticalLayout)
        
        self.is_recording = False
        self.data = [-50]
        self.data_f = [-50]
        self.data_y = [0]

    def showEvent(self, *args, **kwargs):
        self.parent().ble_ascii_received.connect(self.bleAsciiReceived)
        return QtGui.QDialog.showEvent(self, *args, **kwargs)
    
    def closeEvent(self, *args, **kwargs):
        self.reset()
        self.parent().ble_ascii_received.disconnect(self.bleAsciiReceived)
        return QtGui.QDialog.closeEvent(self, *args, **kwargs)
    
    def spinboxChanged(self, value):
        self.distance_A = value;
    
    def sliderChanged(self, value):
        self.distance_n = value / 10.0;
        self.slider_label.setText("n [{0:.1f}]: ".format(self.distance_n))
    
    def reset(self):
        self.table.setRowCount(0)
        self.records = {}
        try:
            self.file.close()
        except Exception:
            pass
        self.file = None
        self.is_recording = False
     
    def plot(self):
        data = [random.random() for i in range(10)]
        self.ax = self.figure.add_subplot(111)
        self.ax.hold(False)
        self.ax.plot(data, '*-')
        self.canvas.draw()
                
    def startRecording(self):
        self.filename = "./logs/" + time.strftime("%y%m%d-%H%M%S") + ".txt"
        try:
            if not os.path.exists("./logs"):
                os.makedirs("./logs")
            self.file = open(self.filename, "w")
            self.statusbar.showMessage("Recording to " + self.filename)
            self.is_recording = True
        except Exception, e:
            self.file = None
            self.is_recording = True
            self.logger.error(e)
            self.statusbar.showMessage("NOT RECORDING - check console log for errors")
           
    def writeRecord(self, record):
        try:
            if not self.is_recording:
                self.startRecording()
            self.file.write(str(record) + "\n")
        except Exception, e:
            self.logger.error(e)
            self.file = None
            self.statusbar.showMessage("NOT RECORDING - check console log for errors")
                 
    def updateSummary(self, record):            
        try:
            summary = self.records[record.mac]
            summary.update(record)
        except Exception:
            summary = BleRecordSummary(record)
            self.records.update({record.mac: summary})
        return summary
                        
    def bleAsciiReceived(self, data):
        record = BleRecord(data)
        summary = self.updateSummary(record)
        
        self.writeRecord(record)
        
        self.data.append(record.rssi_dec)
        self.data_f.append(summary.rssi_feedback)
        self.data_y.append(summary.count)
        self.ax.plot(self.data_y, self.data, "*-", self.data_y, self.data_f, "*--")
        self.canvas.draw()
        
        distance = record.distance(self.distance_A, self.distance_n)
        distance_feedback = record.distance(self.distance_A, self.distance_n, summary.rssi_feedback)
        
        items = self.table.findItems(record.mac, QtCore.Qt.MatchExactly)
        if len(items) > 0:
            row = items[0].row()
        else:
            self.table.setRowCount(self.table.rowCount() + 1)
            row = self.table.rowCount() - 1
            self.table.setItem(row, 0, QTableWidgetItem(record.mac))
            
        self.table.setItem(row, 1, QTableWidgetItem(str(summary.count)))
        self.table.setItem(row, 2, QTableWidgetItem(record.rssi_hex))
        self.table.setItem(row, 3, QTableWidgetItem(str(record.rssi_dec)))
        self.table.setItem(row, 4, QTableWidgetItem(str(distance)))
        self.table.setItem(row, 5, QTableWidgetItem(str(summary.rssi_feedback)))
        self.table.setItem(row, 6, QTableWidgetItem(str(distance_feedback)))
        self.table.setItem(row, 7, QTableWidgetItem(record.battery))    

        self.table.sortItems(0)
        