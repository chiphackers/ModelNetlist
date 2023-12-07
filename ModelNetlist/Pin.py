from .nlNode import *

class Pin(nlNode):
    """
    Generic Pin Class
    """
    def __init__(self, name, parent):
        super().__init__('PIN', name, parent)
        self._connectedNet = None

    def connectNet(self, net):
        if net.getType() != 'NET' :
            shout('WARN', 'Connecting object of type not NET')
        self._connectedNet = net

    def disconnectNet(self):
        self._connectedNet = None

    def getConnectedNet(self):
        return self._connectedNet
