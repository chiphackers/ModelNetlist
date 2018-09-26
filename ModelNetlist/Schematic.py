from .nlUtils import *

class Schematic:
    """This class object stores properties of Schematic"""
    def __init__(self,netlist):
        self.netlist  = netlist
        self.gateList = []
        self.pinList  = []
        self.netList  = []
        self.labels        = {}
        self._gateLoop()

        # Graphics properties
        self.figure_height     = 20
        self.figure_width      = 20
        self.figure_dpi        = 80
        self.figure_margin     = 10
        self.cell_seperation_x = 8
        self.cell_seperation_y = 8
        self.cell_to_pin       = 1
        self.pin_seperation    = 0.5
        self.pin_to_wire       = 4
        self.wire_width        = 1
        self.wire_seperation   = 0.5
        self.wire_color        = 'auto'
        self.port_seperation   = 4
        self.auto_scale        = True

    def _gateLoop(self):
        # GATE Loop
        for node in self.netlist._graph.nodes():
            if node.getType() == 'PIN':
                pin = node
                self.pinList.append(pin)
                self.labels[pin] = pin.getName()
            elif node.getType() == 'NET':
                net = node
                self.netList.append(net)
                self.labels[net] = net.getName()
            elif node.getType() == 'CELL':
                gate = node
                self.gateList.append(gate)
                self.labels[gate] = gate.getName()

