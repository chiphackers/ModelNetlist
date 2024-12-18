from random import randint

from .nlUtils import *
from .nlNode import *
from .Cell import *
from .Net import *
from .Bus import *
from .Port import *
##############################################################
# Main Class : NetList
##############################################################
class ModelNetlist(nlNode):

    def __init__(self, name):
        super().__init__('NETLIST', name, None)
        self._graph = nx.DiGraph()
        self._ports = { 'in' : [], 'out' : [], 'bi' : [] }
        self._gateList = []
        self._netList  = []

    #########################################
    ### APIs to add instances to netlist  ###
    #########################################
    def addCell(self, inst):
        cellGraph = inst.populateCellGraph()
        self._graph = nx.compose(cellGraph, self._graph)

    def addNet(self, inst):
        netGraph = inst.populateNetGraph()
        self._graph = nx.compose(netGraph, self._graph)

    def addPort(self, direction, name, lsb=0, msb=-1):
        port = Pin(name, self)
        if msb > 0:
            port = Port(name, self, lsb, msb)

        if not direction in self._ports.keys():
            shout('ERROR', 'invalid direction. Allowed directions are %s' % self._ports.keys())

        self._ports[direction].append(port)
        port.setAttribute('port', direction)
        self._graph.add_node(port)

    # Instead of creating Net objects explicitly connect PINs using this API
    def connect(self, driver, load, name=None):
        # Sanity checks to verify the driver and load can be connected
        dtype = driver.getType()
        ltype = load.getType()
        is_connectable = False
        is_bus = False
        is_new_net = False
        con_net = None
        if dtype == 'PIN' and ltype == 'PIN':
            is_connectable = True
            con_net = driver.getConnectedNet()
            if not con_net:
                con_net = load.getConnectedNet()
        elif dtype == 'PORT' and ltyle == 'PORT' and driver.getWidth() == load.getWidth():
            is_connectable = True
            is_bus = True
            con_net = driver.getConnectedBus()
            if not con_net:
                con_net = load.getConnectedBus()

        if not is_connectable:
            shout('ERROR', '{} and {} can not be connected'.format(driver, load))

        # If the driver does not have a connection create a new net
        if not con_net:
            is_new_net = True
            if is_bus:
                if name is not None:
                    con_net = Bus(name, self, driver.getLSB(), driver.getMSB())
                else:
                    con_net = Bus('bus_%d' % Bus.inst, self, driver.getLSB(), driver.getMSB())
            else:
                con_net = Net(self)
                if name is not None:
                    con_net.setName(name)
        con_net.addLoad(load)
        con_net.addDriver(driver)
        if is_new_net:
            self.addNet(con_net)

    # Instead of calling above APIs for each cell/net call below API
    def build(self):
        for gate in self._gateList:
            self.addCell(gate)
        for net in self._netList:
            self.addNet(net)

    # Method to remove a node from the netlist
    def remove(self, inst):
        if inst.getType() == 'CELL':
            for pIn in inst.getInputs():
                self.remove(pIn)
            for pOut in inst.getOutputs():
                self.remove(pOut)
            self._gateList.remove(inst)
        elif inst.getType() == 'NET':
            for d in inst.getDrivers():
                d.disconnectNet()
            for l in inst.getLoads():
                l.disconnectNet()
            self._netList.remove(inst)
        elif inst.getType() == 'PIN':
            conNet = inst.getConnectedNet()
            if conNet is not None:
                if inst in conNet.getDrivers():
                    conNet.removeDriver(inst)
                elif inst in conNet.getLoads():
                    conNet.removeLoad(inst)
            # If the pin is a port of the netlist
            for k in self._ports.keys():
                portList = self._ports[k]
                if inst in portList:
                    portList.remove(inst)
        elif inst.getType() == 'BUS':
            for i in range(inst.getLSB(), inst.getMSB()+1):
                self.remove(inst.getNet(i))
            self._netList.remove(inst)
        elif inst.getType() == 'PORT':
            conBus = inst.getConnectedBus()
            if conBus is not None:
                if inst in conBus.getDrivers():
                    conBus.removeDriver(inst)
                elif inst in conBus.getLoads():
                    conBus.removeLoad(inst)

            for i in range(inst.getLSB(), inst.getMSB()+1):
                self.remove(inst.getPin(i))

            # If the port is input/output of the top design
            for k in self._ports.keys():
                portList = self._ports[k]
                if inst in portList:
                    portList.remove(inst)

        try:
            self._graph.remove_node(inst)
        except:
            pass

    #########################################
    ### APIs to access netlist items      ###
    #########################################
    def getInputPorts(self):
        return self._ports['in']

    def getOutputPorts(self):
        return self._ports['out']

    def getPort(self, name):
        for dir in self._ports.keys():
            for port in self._ports[dir]:
                if port.getName() == name:
                    return port
        return None

    def getCells(self):
        return self._gateList

    def getNets(self):
        return self._netList

    def getNeighbors(self, node):
        return self._graph.neighbors(node)

    ##########################################
    ### move this out : depricated - use drawNetlist instead
    ##########################################
    def saveGraph(self,file_name):
        #initialze Figure
        plt.figure(num=None, figsize=(20, 20), dpi=80)
        plt.axis('off')
        fig = plt.figure(1, figsize=(100,100))

        pos = nx.spring_layout(self._graph)

        # CELL Loop
        gateIndex = 1
        gateList = []
        pinList = []
        netList = []
        labels = {}
        for node in self._graph.nodes():
            if node.getType() == 'PIN':
                pin = node
                pinList.append(pin)
                labels[pin] = pin.getName()
            elif node.getType() == 'NET':
                net = node
                netList.append(net)
                labels[net] = net.getName()
            elif node.getType() == 'CELL':
                gate = node
                gateIndex += 1

                gateList.append(gate)
                labels[gate] = gate.getName()

                gate_pos_ = pos[gate]
                gate_pos_[0] = gateIndex * 5
                gate_pos_[1] = 5

                inList = gate.getInputs()
                inCount = len(inList)
                inMid = float(inCount+1)/2
                for index in range(0, inCount):
                    pin = inList[index]

                    pin_pos_ = pos[pin]
                    pin_pos_[0] = gate_pos_[0] - 1.5
                    pin_pos_[1] = gate_pos_[1] + 0.5 * ((index+1) - inMid)

                    connectedNet = pin.getConnectedNet()
                    if connectedNet != None:
                        net_pos_ = pos[connectedNet]
                        net_pos_[0] = (pin_pos_[0] + net_pos_[0])/2
                        net_pos_[1] = (pin_pos_[1] + net_pos_[1])/2


                outList = gate.getOutputs()
                outCount = len(outList)
                outMid = float(outCount+1)/2
                for index in range(0, outCount):
                    pin = outList[index]

                    pin_pos_ = pos[pin]
                    pin_pos_[0] = gate_pos_[0] + 1.5
                    pin_pos_[1] = gate_pos_[1] + 0.5 * ((index+1) - outMid)

                    connectedNet = pin.getConnectedNet()
                    if connectedNet != None:
                        net_pos_ = pos[connectedNet]
                        net_pos_[0] = (pin_pos_[0] + net_pos_[0])/2
                        net_pos_[1] = (pin_pos_[1] + net_pos_[1])/2

        nx.draw_networkx_nodes(self._graph, pos, node_shape='>', node_size=600, node_color='c', nodelist=pinList)
        nx.draw_networkx_nodes(self._graph, pos, node_shape='s', node_size=2400, node_color='y', nodelist=gateList)
        nx.draw_networkx_nodes(self._graph, pos, node_shape='d', node_size=600, node_color='m', nodelist=netList)

        nx.draw_networkx_edges(self._graph,pos)
        nx.draw_networkx_labels(self._graph,pos, labels=labels)


        plt.savefig(file_name,bbox_inches="tight")
        pylab.close()
        del fig

##############################################################
# Returns a ModelNetlist by reading a gate-level netlist
##############################################################
def readVerilogNetlist(verilogNetlist, cellLibList) -> ModelNetlist:

    try:
        from pyverilog.vparser.parser import parse
        from pyverilog.vparser.ast import ModuleDef, Decl, Input, Output, Width, InstanceList, Instance, Identifier, Pointer, Partselect, PortArg, Wire, IntConst
    except:
        shout('ERROR', 'Pyverilog package is required')
        return None
    else:

        netlist = None
        wireMap = {}
        portMap = {'in':[], 'out':[], 'bi':[]}
        ast, _ = parse([verilogNetlist])
        #ast.show()
        # Loop iterating verilog modules
        for astChild in ast.description.children():
            if isinstance(astChild, ModuleDef):
                # We only consider one top module in a flatten netlist
                topModule = astChild
                netlist = ModelNetlist(topModule.name)
                for modChild in topModule.children():
                    if isinstance(modChild, Decl):
                        # Loop iterating Decleartions (i.e., Input, Output, Wires)
                        for decChild in modChild.children():
                            decName = str(decChild.name)
                            if isinstance(decChild, Input):
                                width = get_LSB_N_MSB(decChild)
                                if width is None:
                                    netlist.addPort('in', decName)
                                    portMap['in'].append(decName)
                                else:
                                    netlist.addPort('in', decName, width[0], width[1])
                                    portMap['in'].append(decName)
                            elif isinstance(decChild, Output):
                                width = get_LSB_N_MSB(decChild)
                                if width is None:
                                    netlist.addPort('out', decName)
                                    portMap['out'].append(decName)
                                else:
                                    netlist.addPort('out', decName, width[0], width[1])
                                    portMap['out'].append(decName)
                            elif isinstance(decChild, Wire):
                                width = get_LSB_N_MSB(decChild)
                                if width is None:
                                    net = Net(netlist)
                                    net.setName(decName)
                                    if decName in portMap['in']:
                                        net.addDriver(netlist.getPort(decName))
                                    elif decName in portMap['out']:
                                        net.addLoad(netlist.getPort(decName))
                                    wireMap[decName] = net
                                else:
                                    bus = Bus(decName, netlist, width[0], width[1])
                                    if decName in portMap['in']:
                                        bus.addDriver(netlist.getPort(decName), width[0], width[1])
                                    elif decName in portMap['out']:
                                        bus.addLoad(netlist.getPort(decName), width[0], width[1])
                                    wireMap[decName] = bus

                    if isinstance(modChild, InstanceList):
                        # Loop iterating instances (i.e., gates)
                        for inst in modChild.children():
                            if isinstance(inst, Instance):
                                for lib in cellLibList:
                                    cell = lib.getCell(inst.module)
                                    if cell:
                                        cellInst = cell(netlist)
                                        cellInst.setName(inst.name)
                                        for port in inst.portlist:
                                            portname = str(port.argname)
                                            pinList = []
                                            indexList = []
                                            net = None
                                            if portname in wireMap:
                                                net = wireMap[portname]
                                            else:
                                                # if the port is a bus need to decode the name from a Pointer object
                                                if isinstance(port.argname, Pointer) or isinstance(port.argname, Partselect):
                                                    busName = str(port.argname.var)
                                                    bus = wireMap[busName]
                                                    for i in port.argname.children():
                                                        if isinstance(i, IntConst):
                                                            indexList.append(int(i.value))
                                                    if len(indexList) == 1:
                                                        net = bus.getNet(indexList[0])
                                                    else:
                                                        # A cell with multi-bits ports: We expect to see this when we have macros (i.e., RAM)
                                                        indexList.sort()
                                                        net = bus

                                            pin = cellInst.getPinByName(str(port.portname))
                                            if net is not None:
                                                if pin.isLoad():
                                                    if net.getType() == 'BUS' and len(indexList) == 2:
                                                        net.addLoad(pin, indexList[0], indexList[1])
                                                    else:
                                                        net.addLoad(pin)
                                                elif pin.isDriver():
                                                    if net.getType() == 'BUS' and len(indexList) == 2:
                                                        net.addDriver(pin, indexList[0], indexList[1])
                                                    else:
                                                        net.addDriver(pin)
                                                else:
                                                    shout('ERROR', 'Pin {} not found in cell {}'.format(pin, cell))
                                            else:
                                                # Implicit nets are not previously declared. Need to add these new nets to the netlist
                                                net = Net(netlist)
                                                net.setName(portname)
                                                if pin.isLoad():
                                                    net.addLoad(pin)
                                                elif pin.isDriver():
                                                    net.addDriver(pin)
                                                netlist.addNet(net)
                                                wireMap[portname] = net

        netlist.build()
        return netlist

# Helper function for readVerilogNetlist
def get_LSB_N_MSB(sub_ast):

    from pyverilog.vparser.ast import Width

    # Onput port can have a width
    for child in sub_ast.children():
        if isinstance(child, Width):
            msb = int(child.msb.value)
            lsb = int(child.lsb.value)
            return (lsb, msb)
    return None

