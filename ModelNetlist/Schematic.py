from .nlUtils import *

class Schematic:
    """This class object stores properties of Schematic"""
    def __init__(self,netlist):
        self.netlist  = netlist
        self.gateList = []
        self.pinList  = []
        self.netList  = []
        self.labels        = {}

        # Graphics properties
        self.figure_height     = 20
        self.figure_width      = 20
        self.figure_dpi        = 80
        self.figure_margin     = 10
        self.cell_seperation_x = 8
        self.cell_seperation_y = 5
        self.cell_to_pin       = 1
        self.cell_size         = 2400
        self.pin_size          = 600
        self.pin_seperation    = 0.5
        self.wire_width        = 1
        self.wire_seperation   = 0.5
        self.wire_split        = 0.2
        self.wire_color        = 'auto'
        self.port_seperation   = 4
        self.auto_scale        = True

        # Show labels
        self.cell_labels = True
        self.pin_labels  = True
        self.port_labels = True
        self.net_labels  = False

    def gateLoop(self):
        # GATE Loop
        for node in self.netlist._graph.nodes():
            if node.getType() == 'PIN':
                pin = node
                self.pinList.append(pin)
                if self.pin_labels:
                    if self.labels.get(pin) is None:
                        # if a custom label is not set, we will use name as default label
                        self.labels[pin] = pin.getName()
            elif node.getType() == 'NET':
                net = node
                self.netList.append(net)
                if self.net_labels:
                    if self.labels.get(net) is None:
                        self.labels[net] = net.getName()
            elif node.getType() == 'CELL':
                gate = node
                self.gateList.append(gate)
                if self.cell_labels:
                    if self.labels.get(gate) is None:
                        self.labels[gate] = gate.getName()

        if not self.pin_labels:
            for pKey,pVal in self.netlist._ports.items():
                for port in pVal:
                    if self.labels.get(port) is None:
                        self.labels[port] = port.getName()

    def setLabel(self, node, label):
        self.labels[node] = label
