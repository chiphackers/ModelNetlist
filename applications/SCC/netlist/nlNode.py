##############################################################################
# Base Class
##############################################################################
from .nlUtils import *
from enum import Enum
class nlNode:
    def __init__(self, type, name, parent):
        self._type = type
        self._name = name
        self._parent = parent
        self._attribute = {}

    def __str__(self):
        return '%s.%s' % (self._parent, self._name)

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getParent(self):
        return self._parent

    def getAttribute(self, attrib):
        try:
            return self._attribute[attrib]
        except:
            return None

    def setType(self, type):
        self._type = type

    def setName(self, name):
        self._name = name

    def setParent(self, parent):
        self._parent = parent

    def setAttribute(self, attrib, value):
        self._attributes[attrib] = value
    def getNeighbours(self):
        try:            
            if (self._parent._type == 'GATE'):            
                return nx.all_neighbors(self._parent._parent._graph,self)
        except:
            
            return nx.all_neighbors(self._parent._graph,self)
