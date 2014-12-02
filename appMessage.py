'''
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct AppMessage
    {
        public byte messageType;
        public byte nodeType;
        public UInt64 extAddr;
        public UInt16 shortAddr;
        public UInt64 routerAddr;
        //public UInt32 softVersion;
        //public UInt32 channelMask;
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

class AppMessage:
   def __init__(self, raw):
      fmt = '<ccdHdHcHcbcIIc'
      self.messageType, self.nodeType, self.extAddr, self.shortAddr,           \
      self.routerAddr, self.panId, self.workingChannel, self.parentShortAddr,  \
      self.lqi, self.rssi, self.ackByte,                                       \
      self.battery, self.temperature,                                          \
      self.cs = struct.unpack_from(fmt, test)
    
   

test = '\0x01\0x02\0x80\0x70\0x60\0x50\0x40\0x30\0x20\0x10\0x00\0xf0\0x0e\0x80\0x70\0x60\0x50\0x40\0x30\0x20\0x10\0x00\0xf0\0x0e\0xa\0xf0\0x0e\x0b\0x0c\0x0d\0x04\0x03\0x02\0x01\0x04\0x03\0x02\0x01\0xff'
msg = AppMessage(test)