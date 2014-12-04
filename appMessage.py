'''
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct AppMessage
    {
        public byte messageType;
        public byte nodeType;
        public UInt64 extAddr;
        public UInt16 shortAddr;
        public UInt64 routerAddr;
        public UInt16 panId;
        public byte workingChannel;
        public UInt16 parentShortAddr;
        public byte lqi;
        public sbyte rssi;
        public byte ackByte;

        public UInt32 battery;
        public UInt32 temperature;

        public byte cs;     
    }
'''

import struct 
from cobs import cobs

class AppMessage:

    def __repr__(self):
        return  'messageType: {0:#04x}, '    \
                'nodeType: {1:#04x}, '          \
                'extAddr: {2:#018x}, '           \
                'shortAddr: {3:#06x}, '           \
                'routerAddr: {4:#018x}, '           \
                'panId: {5:#06x}, '           \
                'workingChannel: {6:#04x}, '           \
                'parentShortAddr: {7:#06x}, '           \
                'lqi: {8:#04x}, '           \
                'rssi: {9:#04x}, '           \
                'ackByte: {10:#04x}, '           \
                'battery: {11:#010x}, '           \
                'temperature: {12:#010x}, '           \
                'cs: {13:#04x} '           \
                .format(self.messageType, self.nodeType, self.extAddr, self.shortAddr,  \
                        self.routerAddr, self.panId, self.workingChannel, self.parentShortAddr, \
                        self.lqi, self.rssi, self.ackByte, self.battery, self.temperature, self.cs)
    
   

    def decode(self, data):
        fmt = '<BBQHQHBHBbBIIB'
        x = struct.unpack_from(fmt, data)
        self.messageType = x[0]
        self.nodeType = x[1]
        self.extAddr = x[2]
        self.shortAddr = x[3]
        self.routerAddr = x[4]
        self.panId = x[5]
        self.workingChannel = x[6]
        self.parentShortAddr = x[7]
        self.lqi = x[8]
        self.rssi = x[9]
        self.ackByte = x[10]
        self.battery = x[11]
        self.temperature = x[12]
        self.cs = x[13]        
        
    def decode_cobs(self, cobs_input):
        data = cobs.decode(buffer(cobs_input))
        self.decode(data)
        
    def test(self):
        test = bytearray([ 0x01,0x02,0x80,0x70,0x60,0x50,0x40,0x30,0x20,0x10,0x00,0xf0,0x0e,0x80,0x70,0x60,0x50,0x40,0x30,0x20,0x10,0x00,0xf0,0x0e,0xa,0xf0,0x0e,0x0b,0x0c,0x0d,0x04,0x03,0x02,0x01,0x04,0x03,0x02,0x01,0xff ])
        cobs_data = cobs.encode(buffer(test))
        self.decode_cobs(bytearray(cobs_data))
        print self
