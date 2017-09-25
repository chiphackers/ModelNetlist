from random import randint

from .nlUtils import *
from .Cell import *
##############################################################
# Main Class : NetList
##############################################################
class SimpleNetlist:

    def __init__(self, name):
        self._name = name
        self._graph = nx.Graph()
        self._ports = { 'in' : [], 'out' : [], 'bi' : [] }

    def __str__(self):
        return self._name

    def getName(self):
        return self._name

    #########################################
    ### APIs to add instances to netlist  ###
    #########################################
    def addCell(self, inst):
        cellGraph = inst.populateCellGraph()
        self._graph = nx.compose(cellGraph, self._graph)

    def addNet(self, inst):
        netGraph = inst.populateNetGraph()
        self._graph = nx.compose(netGraph, self._graph)
        
    def addPort(self, direction, name):
        port = Pin(name, self)
        if not direction in self._ports.keys():
            shout('ERROR', 'invalid direction. Allowed directions are %s' % self._ports.keys())

        self._ports[direction].append(port)
        port.setAttribute('port', direction)
        self._graph.add_node(port)

    #########################################
    ### APIs to access netlist items      ###
    #########################################
    def getConnectedNet(self, pin):
        if pin.getType() != 'PIN':
            shout('ERROR', '%s is not a PIN object')
            return None

        else:
            neighborList = self._graph.neighbors(pin)
            for neighbor in neighborList:
                if neighbor.getType() == 'NET':
                    return neighbor
            return None
            
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
        
    def getNeighbours(self, node):
        return self._graph.neighbors(node)

    ##########################################
    ### move this out
    ##########################################
    def saveGraph(self,file_name):
        #initialze Figure
        plt.figure(num=None, figsize=(20, 20), dpi=80)
        plt.axis('off')
        fig = plt.figure(1, figsize=(100,100))

        pos = nx.spring_layout(self._graph)

        # GATE Loop
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
            elif node.getType() == 'GATE':
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

                    connectedNet = self.getConnectedNet(pin)
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

                    connectedNet = self.getConnectedNet(pin)
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

