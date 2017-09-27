import sys
import matplotlib
matplotlib.use('Agg')

from matplotlib import pylab

import networkx as nx
import matplotlib.pyplot as plt

SILENT = False

def shout(severity, message):
    """
    Print messages to standard output
    """
    if SILENT:
        return

    if severity == 'WARN':
        print('%s[WARN ]: %s %s' % ('\033[93m', message, '\033[0m'))
    elif severity == 'ERROR':
        print('%s[ERROR]: %s %s' % ('\033[91m', message, '\033[0m'))
        sys.exit()
    elif severity == 'INFO':
        print('%s[INFO ]: %s %s' % ('\033[92m', message, '\033[0m'))

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def drawNetlist(netlist,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1, figsize=(100,100))

    pos = nx.spring_layout(netlist._graph)

    # GATE Loop
    gateList = []
    pinList = []
    netList = []
    labels = {}
    for node in netlist._graph.nodes():
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
            gateList.append(gate)
            labels[gate] = gate.getName()

    diagLeftMargin = 10
    diagWidth = diagLeftMargin
    # Placing input ports as a column at the left end
    portIndex = 1
    for iPort in netlist.getInputPorts():
        loc = pos[iPort]
        loc[0] = diagLeftMargin - 5
        loc[1] = 4 * portIndex
        portIndex += 1

    # Create cell edges
    incomming_edges = {}
    outgoing_edges = {}
    all_gates  = []
    gates_without_incomming = []
    for gate in gateList :
        all_gates.append(gate)
        incomming_edges[gate] = []

        inputs = gate.getInputs()
        has_incomming = False
        for i in inputs:
            net = i.getConnectedNet()
            if not net :
                continue

            drivers = net.getDrivers()
            if i in drivers:
                shout('ERROR', '%s is an input but driving a net' % i)
                return

            for driver in drivers :
                if driver.getType() == 'PIN' :
                    driverCell = driver.getParent()
                    if driverCell != None and driverCell.getType() == 'CELL':
                        incomming_edges[gate].append(driverCell)
                        if not driverCell in outgoing_edges:
                            outgoing_edges[driverCell] = []
                        outgoing_edges[driverCell].append(gate)
                        has_incomming = True

        if not has_incomming :
            gates_without_incomming.append(gate)
        
    # topological sorting
    sorted_list = []
    while gates_without_incomming :
        gate = gates_without_incomming.pop()
        
        # set cluster id
        cluster_id = gate.getAttribute('cluster_id')
        if cluster_id == None :
            cluster_id = 1
            gate.setAttribute('cluster_id', cluster_id)

        sorted_list.append(gate)
        
        if not gate in outgoing_edges:
            continue

        while outgoing_edges[gate] :
            loadCell = outgoing_edges[gate].pop()

            incomming_edges[loadCell].remove(gate)
            if not incomming_edges[loadCell]:
                sorted_list.append(loadCell)
                gates_without_incomming.append(loadCell)
                loadCell.setAttribute('cluster_id', cluster_id + 1)

    # incomming_edges and outgoing_edges are not empty then there are loops in circuit
    # it will not matter for sorting
    
    # when a gate is placed cluster depth increases
    clusterDpeths = {}
    # Bringing cell pins close to cell node
    for gate in gateList :
        cluster_id = gate.getAttribute('cluster_id')
        if cluster_id == None:
            cluster_id = 1

        if not cluster_id in clusterDpeths:
            clusterDpeths[cluster_id] = 1
        else:
            clusterDpeths[cluster_id] += 1

        gate_pos_ = pos[gate]
        
        # x position
        gate_pos_[0] = diagLeftMargin + cluster_id * 8
        diagWidth = max(diagWidth, gate_pos_[0])
        
        # y position
        gate_pos_[1] = clusterDpeths[cluster_id] * 5

        inList = gate.getInputs()
        inCount = len(inList)
        inMid = float(inCount+1)/2
        for index in range(0, inCount):
            pin = inList[index]

            pin_pos_ = pos[pin]
            pin_pos_[0] = gate_pos_[0] - 1.5
            pin_pos_[1] = gate_pos_[1] + 0.5 * ((index+1) - inMid)

            connectedNet = pin.getConnectedNet()
            if not connectedNet :
                continue 

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
            if not connectedNet :
                continue 

            net_pos_ = pos[connectedNet]
            net_pos_[0] = (pin_pos_[0] + net_pos_[0])/2
            net_pos_[1] = (pin_pos_[1] + net_pos_[1])/2

    # placging nets
    for net in netList:
        net_pos_ = pos[net]
        net_pos_[0] = 0
        net_pos_[1] = 0

        for driver in net.getDrivers():
            net_pos_[0] += pos[driver][0]
            net_pos_[1] += pos[driver][1]

        for load in net.getLoads():
            net_pos_[0] += pos[load][0]
            net_pos_[1] += pos[load][1]

        net_pos_[0] = net_pos_[0]/(len(net.getDrivers()) + len(net.getLoads()))
        net_pos_[1] = net_pos_[1]/(len(net.getDrivers()) + len(net.getLoads()))

    # placing output ports as a column in righ hand end
    diagWidth = diagWidth + 5
    portIndex = 1
    for oPort in netlist.getOutputPorts():
        loc = pos[oPort]
        loc[0] = diagWidth + 4
        loc[1] = 4 * portIndex
        portIndex += 1



    nx.draw_networkx_nodes(netlist._graph, pos, node_shape='>', node_size=600, node_color='c', nodelist=pinList)
    nx.draw_networkx_nodes(netlist._graph, pos, node_shape='s', node_size=2400, node_color='y', nodelist=gateList)
    nx.draw_networkx_nodes(netlist._graph, pos, node_shape='d', node_size=600, node_color='m', nodelist=netList)

    nx.draw_networkx_edges(netlist._graph,pos)
    nx.draw_networkx_labels(netlist._graph,pos, labels=labels)


    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig



