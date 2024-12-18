from .nlNode import *
from .Pin import Pin

class Port(nlNode):
    """
    A port is a group of pins
    """
    def __init__(self, name, parent, lsb=0, msb=1):
        super().__init__('PORT', name, parent)
        self._lsb = lsb
        self._msb = msb
        self._connectedBus = None
        self._pins = self.getWidth()*[None]
        for i in range(0, self.getWidth()):
            self._pins[i] = Pin('[{}]'.format(i), self)

    def getParentPort(self):
        return None

    def getLSB(self):
        return self._lsb

    def getMSB(self):
        return self._msb

    def getWidth(self):
        return (self._msb+1-self._lsb)

    def getPin(self, index):
        if index < self._lsb or index > self._msb:
            shout('ERROR', 'Index out of range')
        return self._pins[index-self._lsb]

    def getPinIndex(self, pin):
        try:
            return self._pins.index(pin)
        except:
            return -1

    def setPin(self, index, pin):
        if pin.getType() != 'PIN':
            shout('WARN', '{} is not a pin'.format(pin.getName()))
        if self.getPin(index) != None:
            shout('WARN', 'An old pin is replaced by {}'.format(pin.getName()))
        self._pins[index-self._lsb] = pin

    # connectBus and disconnectBus APIs will be called by a BUS object when a load or a driver is added
    # avoid direclty calling these APIs since they do not add/remove the load and driver from the connected Bus

    def connectBus(self, bus):
        if bus.getType() != 'BUS' :
            shout('ERROR', '{} is not a BUS'.format(bus.getName()))
        if self.getWidth() != bus.getWidth():
            # We only support connecting a single bus to a port at this point
            shout('WARN', 'Width mismatch between port {} and bus {}'.format(self.getName(), bus.getName()))
        self._connectedBus = bus

    def disconnectBus(self):
        self._connectedBus = None

    def getConnectedBus(self):
        return self._connectedBus

    def getConnectedNet(self, index=0):
        return self._pins[index].getConnectedNet()
