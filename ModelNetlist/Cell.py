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
        if len(outputs) > 0 :
            self._outputs = outputs
        parent._gateList.append(self)

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

    def getPinByName(self, name):
        for inPin in self._inputs:
            if inPin.getName() == name:
                return inPin
        for outPin in self._outputs:
            if outPin.getName() == name:
                return outPin

    def populateCellGraph(self, inputDelay=0, outputDelay=0):
        cellGraph = nx.DiGraph()

        for input in self._inputs:
            cellGraph.add_edge(input, self)

        for output in self._outputs:
            cellGraph.add_edge(self, output)

        return cellGraph

class CellLibrary(nlNode):
    """
    Library containing a collection of cells
    """
    def __init__(self, name):
        super().__init__('LIBRARY', name, None)
        self._cells = {}

    def addCell(self, cell):
        self._cells[cell.name] =  cell

    def getCell(self, cellName):
        return self._cells.get(cellName)

    def listCellNames(self):
        return list(self._cells.keys())

    def listCells(self):
        return self._cells.values()

##############################################################################
# Populate a library from a liberty file
##############################################################################
def readLiberty(filename) -> CellLibrary:
    """
    Read standard cells from a liberty (.lib) file
    """
    try:
        from liberty.parser import parse_liberty
    except:
        shout('ERROR', 'liberty-parser package is required!')
    else:

        try:
            lib_file = open(filename, 'r')
        except:
            shout('ERROR', 'Could not read the liberty file')
            return None

        with lib_file:

            liberty = parse_liberty(lib_file.read())
            lib_file.close()
            library = CellLibrary(liberty.args[0])

            for cell_group in liberty.get_groups('cell'):
                cell_name = cell_group.args[0]
                cell_pins = {}
                cell_function = None
                for pin_group in cell_group.get_groups('pin'):
                    pin_name = pin_group.args[0]
                    pin_direction = pin_group['direction']
                    if pin_direction in cell_pins:
                        cell_pins[pin_direction].append(pin_name)
                    else:
                        cell_pins[pin_direction] = [pin_name]

                    if pin_group['function'] != None:
                        if cell_function != None:
                            shout('WARN', 'Cells with multiple outputs are not supported yet.')
                            shout('WARN', 'Function of the last output pin will be used for {}'.format(cell_name))
                        cell_function = pin_group['function']

                # Dynamically create the cell
                cellType = type(cell_name, (Cell,), {
                    'name' : cell_name,
                    'pinMap' : cell_pins,
                    '__init__' : protoLibCellInit
                })
                library.addCell(cellType)

            return library

def protoLibCellInit(self, parent):
    objInputs = []
    objOutputs = []
    if not 'input' in self.pinMap.keys():
        shout('WARN', 'No inputs in {}'.format(self.name))
    else:
        for pin in self.pinMap['input']:
            objPin = Pin(pin, self)
            setattr(self, pin, objPin)
            objInputs.append(objPin)

    if not 'output' in self.pinMap.keys():
        shout('WARN', 'No outputsin {}'.format(self.name))
    else:
        for pin in self.pinMap['output']:
            objPin = Pin(pin, self)
            setattr(self, pin, objPin)
            objOutputs.append(objPin)

    Cell.__init__(self, self.name, parent, None, objInputs, objOutputs)

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
