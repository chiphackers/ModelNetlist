from commons import *
##############################################################################
# Base Class
##############################################################################
class nlNode:
    def __init__(self, obj_type, name, parent):
        self._type = obj_type
        self._name = name
        self._parent = parent
        self._attributes = {}

    def __str__(self):
        return self.getFullName()

    def getType(self):
        return self._type

    def getName(self):
        if self._parent is not None:
            if self._parent.getType() == 'PORT' or self._parent.getType() == 'BUS':
                return '%s%s' % (self._parent.getName(), self._name)
            else:
                return self._name
        else:
            return self._name

    def getFullName(self):
        if self._parent is not None:
            if self._parent.getType() == 'PORT' or self._parent.getType() == 'BUS':
                return '%s%s' % (self._parent.getFullName(), self._name)
            else:
                return '%s.%s' % (self._parent.getFullName(), self._name)
        else:
            return '%s' % (self._name)

    def getParent(self):
        return self._parent

    def getAttribute(self, attrib):
        if attrib in self._attributes:
            return self._attributes[attrib]
        else:
            return None

    def setType(self, type):
        self._type = type

    def setName(self, name):
        self._name = name

    def setParent(self, parent):
        self._parent = parent

    def setAttribute(self, attrib, value):
        self._attributes[attrib] = value
