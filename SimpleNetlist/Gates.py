from .nlUtils import *
from .nlNode import *
from .Pins import *

class Gate(nlNode):
    """
    Generic Gate class
    """
    def __init__(self, name, parent, function, inputs, outputs):
        super().__init__('GATE', name, parent)
        self._function = function
        if len(inputs) > 0 :
            self._inputs = inputs
        else:
            shout('ERROR','inputs list should contain at least one element')

        if len(outputs) > 0 :
            self._outputs = outputs
        else:
            shout('ERROR','outputs list should contain at least one element')

    def getInputs(self):
        return self._inputs

    def input(self, index):
        if index >= len(self._inputs):
            shout('ERROR', 'gate input index out of bound')
            return None
        else:
            return self._inputs[index]

    def getOutputs(self):
        return self._outputs

    def output(self, index):
        if index >= len(self._outputs):
            shout('ERROR', 'gate input index out of bound')
            return None
        else:
            return self._outputs[index]

    def populateCellGraph(self, inputDelay=0, outputDelay=0):
        cellGraph = nx.DiGraph()

        for input in self._inputs:
            cellGraph.add_edge(input, self)

        for output in self._outputs:
            cellGraph.add_edge(self, output)

        return cellGraph

#############################################################
# Classes with base class Gate
#############################################################
@static_vars(inst=0)
class AND2(Gate):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        in2 = Pin('IN2', self)
        out = Pin('OUT', self)
        name = 'AND2_%d' % AND2.inst
        AND2.inst += 1
        Gate.__init__(self, name, parent, lambda x, y: x & y, [in1, in2], [out])

@static_vars(inst=0)
class OR2(Gate):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        in2 = Pin('IN2', self)
        out = Pin('OUT', self)
        name = 'OR2_%d' % OR2.inst
        OR2.inst += 1
        Gate.__init__(self, name, parent, lambda x, y: x | y, [in1, in2], [out])

@static_vars(inst=0)
class XOR2(Gate):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        in2 = Pin('IN2', self)
        out = Pin('OUT', self)
        name = 'XOR2_%d' % OR2.inst
        OR2.inst += 1
        Gate.__init__(self, name, parent, lambda x, y: x ^ y, [in1, in2], [out])

@static_vars(inst=0)
class INV(Gate):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        out = Pin('OUT', self)
        name = 'INV_%d' % INV.inst
        INV.inst += 1
        Gate.__init__(self, name, parent, lambda x: ~x, [in1], [out])

