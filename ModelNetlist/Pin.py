from .nlNode import *

class Pin(nlNode):
    """
    Generic Pin Class
    """
    def __init__(self, name, parent):
        super().__init__('PIN', name, parent)
        self._connectedNet = None
        self._port = None
        if parent.getType() == 'PORT':
            self._port = parent

    # connectNet and disconnectNet APIs will be called by a NET object when a load or a driver is added
    # avoid directly calling these APIs since they do not add/remove the load and driver from the connected Net
    def connectNet(self, net):
        if net.getType() != 'NET' :
            shout('WARN', 'Connecting object of type not NET')
        self._connectedNet = net

    def disconnectNet(self):
        self._connectedNet = None

    def getConnectedNet(self):
        return self._connectedNet

    def getParentPort(self):
        return self._port

    def setParentPort(self, port):
        if port.getType() == 'PORT':
            self._port = port

    # Below APIs check the parent to decide if the PIN is a driver/load
    # What about bi-directional ports. We are not ready for them yet
    def isDriver(self):
        node = self
        if node.getParentPort() is not None:
            node = node.getParentPort()

        parent = node.getParent()
        if parent.getType() == 'CELL':
            return node in parent.getOutputs()
        elif parent.getType() == 'NETLIST':
            return node in parent.getInputPorts()

        return False

    def isLoad(self):
        node = self
        if node.getParentPort() is not None:
            node = node.getParentPort()

        parent = node.getParent()
        if parent.getType() == 'CELL':
            return node in parent.getInputs()
        elif parent.getType() == 'NETLIST':
            return node in parent.getOutputPorts()

        return False
