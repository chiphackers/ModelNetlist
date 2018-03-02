from .nlNode import *
from .Pin import *

class Cell(nlNode):
    """
    Generic Gate class
    """
    def __init__(self, name, parent, function, inputs, outputs):
        super().__init__('CELL', name, parent)
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
class AND2(Cell):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        in2 = Pin('IN2', self)
        out = Pin('OUT', self)
        name = 'AND2_%d' % AND2.inst
        AND2.inst += 1
        Cell.__init__(self, name, parent, lambda x, y: x & y, [in1, in2], [out])

@static_vars(inst=0)
class OR2(Cell):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        in2 = Pin('IN2', self)
        out = Pin('OUT', self)
        name = 'OR2_%d' % OR2.inst
        OR2.inst += 1
        Cell.__init__(self, name, parent, lambda x, y: x | y, [in1, in2], [out])

@static_vars(inst=0)
class XOR2(Cell):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        in2 = Pin('IN2', self)
        out = Pin('OUT', self)
        name = 'XOR2_%d' % OR2.inst
        OR2.inst += 1
        Cell.__init__(self, name, parent, lambda x, y: x ^ y, [in1, in2], [out])

@static_vars(inst=0)
class INV(Cell):
    def __init__(self, parent):
        in1 = Pin('IN1', self)
        out = Pin('OUT', self)
        name = 'INV_%d' % INV.inst
        INV.inst += 1
        Cell.__init__(self, name, parent, lambda x: ~x, [in1], [out])

@static_vars(inst=0)
class FLOP(Cell):
    def __init__(self, parent):
        d = Pin('D', self)
        q = Pin('Q', self)
        clk = Pin('CLK', self)
        name = 'FLOP_%d' % FLOP.inst
        FLOP.inst += 1
        Cell.__init__(self, name, parent, lambda d, c, q: d, [d, clk], [q])
