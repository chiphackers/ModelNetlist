import sys
import random
import collections
import matplotlib

from matplotlib import pylab

import networkx as nx
import matplotlib.pyplot as plt

from .Utils import *

def plotColor(color):
    if not color == 'auto':
        return color
    else:
        return'#%02X%02X%02X' % (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def drawNetlist(schematic,file_name):

    schematic.gateLoop()

    netlist = schematic.netlist

    #initialze Figure
    plt.figure(num=None, figsize=(schematic.figure_width, schematic.figure_height), dpi=schematic.figure_dpi)
    plt.axis('off')
    fig = plt.figure(1, figsize=(schematic.figure_width,schematic.figure_height))

    diagWidth = schematic.figure_width
    pos = nx.spring_layout(netlist._graph)

    # Below maps are storing data on vertical wires
    v_wire_map = {}   # keep track of vertical wire id between clusters
    v_wire_names_map = {} # { {net} : {cluster_id : (wire_map[cluster_id], max, min)} }
    h_wire_map = {}   # keep track of horizontal wires between v_wires
    h_wire_names_map = {} # { {net} : {cluster_height} : (wire_map[cluster_height], max, min)} }}
    last_cluster = 0

    # Placing input ports as a column at the left end
    portIndex = 1
    v_wire_map[0] = 0
    for iPort in netlist.getInputPorts():
        loc = pos[iPort]
        loc[0] = schematic.figure_margin
        loc[1] = schematic.port_seperation * portIndex
        portIndex += 1

        net = iPort.getConnectedNet()
        if not net is None:
            # draw wire to vertical wire
            v_wire_map[0] += 1
            v_wire_names_map[net] = { 0 : (v_wire_map[0], loc[1], loc[1]) }

            if net.getAttribute('color') is None:
                net_color = plotColor(schematic.wire_color)
                net.setAttribute('color',net_color)

            vw_x = ( schematic.figure_margin
                    + schematic.cell_seperation_x * schematic.wire_split
                    + schematic.wire_seperation * v_wire_names_map[net][0][0])
            plt.plot([loc[0],vw_x],[loc[1],loc[1]],net.getAttribute('color'))

            for load in net.getLoads():
                load.setAttribute('port_driven',True)

    # Do a DFS to find feedback path and mark them for ignoring in topological sort
    for gate in schematic.gateList :

        if not gate.getAttribute('fb_search') is None:
            continue

        gate.setAttribute('fb_search',1)
        dfs_stack = [gate]
        dfs_parent = { gate : None }
        while len(dfs_stack) > 0:
            cell = dfs_stack.pop()
            if not cell is None:
                for out in cell.getOutputs():
                    cNet = out.getConnectedNet()
                    if cNet is not None:
                        for cLoad in cNet.getLoads():
                            nCell = cLoad.getParent()
                            if nCell is None or nCell.getType() != 'CELL':
                                continue

                            if not nCell in dfs_parent:
                                # if nCell already has fb_search it has been been searched for loops before
                                if not nCell.getAttribute('fb_search') is None:
                                    continue
                                else:
                                    gate.setAttribute('fb_search',1)

                                dfs_parent[nCell] = cell
                                dfs_stack.append(nCell)
                            else:
                                # already discvored cell. check whether cyclic
                                is_cyclic = False
                                backtrace = cell
                                while backtrace != None:
                                    if backtrace == nCell:
                                        is_cyclic = True
                                        break
                                    else:
                                        backtrace = dfs_parent[backtrace]

                                if is_cyclic :
                                    cLoad.setAttribute('feedback_net', str(cNet))

    # Create cell edges
    incomming_edges = {}
    outgoing_edges = {}
    all_gates  = []
    gates_without_incomming = []
    for gate in schematic.gateList :
        all_gates.append(gate)
        incomming_edges[gate] = []

        inputs = gate.getInputs()
        has_incomming = False
        for i in inputs:
            # feedbacks are ignored for topological sorting
            if i.getAttribute('feedback_net') != None:
                shout('INFO','feedback net found %s' % i.getConnectedNet())
                continue
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
            if last_cluster < cluster_id:
                last_cluster = cluster_id

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
                if last_cluster < (cluster_id+1):
                    last_cluster = (cluster_id+1)

    # incomming_edges and outgoing_edges are not empty then there are loops in circuit
    # it will not matter for sorting

    # when a gate is placed cluster height increases
    clusterHeight = {}
    # Bringing cell pins close to cell node
    for gate in schematic.gateList :
        cluster_id = gate.getAttribute('cluster_id')
        if cluster_id == None:
            cluster_id = 1

        if not cluster_id in clusterHeight:
            clusterHeight[cluster_id] = 1
        else:
            clusterHeight[cluster_id] += 1

        gate.setAttribute('cluster_height', clusterHeight[cluster_id])
        gate_pos_ = pos[gate]

        # x position
        gate_pos_[0] = schematic.figure_margin + cluster_id * schematic.cell_seperation_x
        diagWidth = max(diagWidth, gate_pos_[0])

        # y position
        gate_pos_[1] = clusterHeight[cluster_id] * schematic.cell_seperation_y

        inList = gate.getInputs()
        inCount = len(inList)
        inMid = float(inCount+1)/2
        for index in range(0, inCount):
            pin = inList[index]

            pin_pos_ = pos[pin]
            pin_pos_[0] = gate_pos_[0] - schematic.cell_to_pin
            pin_pos_[1] = gate_pos_[1] + schematic.pin_seperation * ((index+1) - inMid)

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
            pin_pos_[0] = gate_pos_[0] + schematic.cell_to_pin
            pin_pos_[1] = gate_pos_[1] + schematic.pin_seperation * ((index+1) - outMid)

            connectedNet = pin.getConnectedNet()
            if not connectedNet :
                continue

            net_pos_ = pos[connectedNet]
            net_pos_[0] = (pin_pos_[0] + net_pos_[0])/2
            net_pos_[1] = (pin_pos_[1] + net_pos_[1])/2

    # placing output ports as a column in righ hand end
    diagWidth = diagWidth + schematic.cell_seperation_x
    if diagWidth > schematic.figure_width :
        if schematic.auto_scale :
            shout('INFO','Rescaling schematic width')
            schematic.figure_width = diagWidth
        else:
            shout('WARN','schematic is wider than specified. Increase schematic.figure_width or use schematic.auto_scale')

    portIndex = 1
    for oPort in netlist.getOutputPorts():
        loc = pos[oPort]
        loc[0] = diagWidth
        loc[1] = schematic.port_seperation * portIndex
        portIndex += 1

        net = oPort.getConnectedNet()
        if not net is None:
            # draw wire to vertical wire
            if not last_cluster in v_wire_map:
                v_wire_map[last_cluster] = 1
            else:
                v_wire_map[last_cluster] += 1

            if not net in v_wire_names_map:
                v_wire_names_map[net] = { last_cluster : (v_wire_map[last_cluster], loc[1], loc[1]) }
            elif not last_cluster in v_wire_names_map[net]:
                v_wire_names_map[net][last_cluster] = (v_wire_map[last_cluster], loc[1], loc[1])
            else:
                vwire = v_wire_names_map[net][last_cluster]
                vmax = max(loc[1], vwire[1])
                vmin = min(loc[1], vwire[2])
                v_wire_names_map[net] = { last_cluster : (v_wire_map[last_cluster], vmax, vmin) }


            if net.getAttribute('color') is None:
                net_color = plotColor(schematic.wire_color)
                net.setAttribute('color',net_color)

            vw_x = ( schematic.figure_margin
                    + schematic.cell_seperation_x * last_cluster
                    + schematic.cell_seperation_x * schematic.wire_split
                    + schematic.wire_seperation * v_wire_names_map[net][last_cluster][0])
            plt.plot([vw_x, loc[0]],[loc[1],loc[1]],net.getAttribute('color'))

    for oPort in netlist.getOutputPorts():
        if not oPort.getAttribute('port_driven') is None:
            # input is directly connected to output. h_wire and v_wire need to be drawn
            net = oPort.getConnectedNet()
            if net.getAttribute('color') is None:
                net_color = plotColor(schematic.wire_color)
                net.setAttribute('color',net_color)

            height = -1
            hw_max = -1
            hw_min = -1

            if not net in h_wire_names_map:
                if not 0 in h_wire_map:
                    h_wire_map[0] = 1
                else:
                    h_wire_map[0] += 1
                h_wire_names_map[net] = { 0 : (h_wire_map[0], hw_max, hw_min) }
            else:
                hw_descript = h_wire_names_map[net][0]
                hw_max = hw_descript[1]
                hw_min = hw_descript[2]

            hw_y = (schematic.wire_split * schematic.cell_seperation_y
                    + schematic.wire_seperation * h_wire_map[0] )

            v_wire = v_wire_names_map[net]
            for cid, vw_descript in v_wire.items():
                vw_x = ( schematic.figure_margin
                        + schematic.cell_seperation_x * cid
                        + schematic.cell_seperation_x * schematic.wire_split
                        + schematic.wire_seperation * vw_descript[0])
                # draw vertical wire
                if vw_descript[2] > hw_y:
                    plt.plot([vw_x, vw_x], [vw_descript[1], hw_y], net.getAttribute('color'))
                else:
                    plt.plot([vw_x, vw_x], [vw_descript[1], vw_descript[2]], net.getAttribute('color'))

                if vw_x > hw_max:
                    hw_max = vw_x
                if vw_x < hw_min or hw_min < 0:
                    hw_min = vw_x

            # draw horizontal wire
            plt.plot([hw_min, hw_max], [hw_y, hw_y], net.getAttribute('color'))
            h_wire_names_map[net][0] = (h_wire_map[0], hw_max, hw_min)


    # placing nets
    ######## Model Description using v_wire and h_wire ##################
    #                                                                   #
    #      cluster_1      cluster_2       cluster_3                     #
    #                                                                   #
    #  >    ------           ------          ------     >               #
    #      | cell |-----max | cell |   -----| cell |          height 1  #
    #       ------     |     ------    |     ------                     #
    #               min|----------------max                             #
    #  >       v_wire->|         ^-h_wire               >               #
    #       ------     |      ------         ------                     #
    #      | cell | min-----| cell |       | cell |           height 0  #
    #  >    ------            ------         ------     >               #
    #                                                                   #
    #####################################################################
    for net in schematic.netList:

        net_color = net.getAttribute('color')
        if net_color is None:
            net_color = plotColor(schematic.wire_color)
            net.setAttribute('color',net_color)

        net_pos_ = pos[net]
        net_pos_[0] = 0
        net_pos_[1] = 0

        for driver in net.getDrivers():
            if driver.getType() == 'PIN':
                pCell = driver.getParent()
                if pCell != None and pCell.getType() == 'CELL':

                    cluster_id = pCell.getAttribute('cluster_id')
                    cluster_height = pCell.getAttribute('cluster_height')

                    d_x = pos[driver][0]
                    d_y = pos[driver][1]

                    if not net in v_wire_names_map:
                        if cluster_id in v_wire_map:
                            v_wire_map[cluster_id] += 1
                        else:
                            v_wire_map[cluster_id] = 1

                        v_wire_names_map[net] = {cluster_id : (v_wire_map[cluster_id], d_y, d_y)}
                        # draw wire to vertical wire
                        vw_x = ( schematic.figure_margin
                                + schematic.cell_seperation_x * schematic.wire_split
                                + schematic.cell_seperation_x * cluster_id
                                + schematic.wire_seperation * v_wire_names_map[net][cluster_id][0])
                        plt.plot([d_x,vw_x],[d_y,d_y],net_color)
                    else:
                        if not cluster_id in v_wire_names_map[net]:
                            if cluster_id in v_wire_map:
                                v_wire_map[cluster_id] += 1
                            else:
                                v_wire_map[cluster_id] = 1

                            v_wire_names_map[net][cluster_id] = (v_wire_map[cluster_id], d_y, d_y)
                            # draw wire to vertical wire
                            vw_x = ( schematic.figure_margin
                                    + schematic.cell_seperation_x * schematic.wire_split
                                    + schematic.cell_seperation_x * cluster_id
                                    + schematic.wire_seperation * v_wire_names_map[net][cluster_id][0])
                            plt.plot([d_x,vw_x],[d_y,d_y],net_color)
                        else:
                            vw = v_wire_names_map[net][cluster_id]
                            vw_max = max(vw[1],d_y)
                            vw_min = min(vw[2],d_y)

                            v_wire_names_map[net][cluster_id] = (vw[0], vw_max, vw_min)
                            # draw wire to vertical wire
                            vw_x = ( schematic.figure_margin
                                    + schematic.cell_seperation_x * schematic.wire_split
                                    + schematic.cell_seperation_x * cluster_id
                                    + schematic.wire_seperation * v_wire_names_map[net][cluster_id][0])
                            plt.plot([d_x,vw_x],[d_y,d_y],net_color)

            else:
                shout('ERROR', '%s net is driven by %s which is not type PIN' % (net, driver))
            net_pos_[0] += pos[driver][0]
            net_pos_[1] += pos[driver][1]

        for load in net.getLoads():
            net_pos_[0] += pos[load][0]
            net_pos_[1] += pos[load][1]

            if load.getType() == 'PIN':
                pCell = load.getParent()
                if pCell != None and pCell.getType() == 'CELL':
                    # load cell connect to wire cluster before the cell
                    cluster_id = pCell.getAttribute('cluster_id') - 1
                    cluster_height = pCell.getAttribute('cluster_height')

                    l_x = pos[load][0]
                    l_y = pos[load][1]

                    if not net in v_wire_names_map:
                        if cluster_id in v_wire_map:
                            v_wire_map[cluster_id] += 1
                        else:
                            v_wire_map[cluster_id] = 1

                        v_wire_names_map[net] = {cluster_id : (v_wire_map[cluster_id], l_y, l_y)}
                        # draw wire to vertical wire
                        vw_x = ( schematic.figure_margin
                                + schematic.cell_seperation_x * schematic.wire_split
                                + schematic.cell_seperation_x * cluster_id
                                + schematic.wire_seperation * v_wire_names_map[net][cluster_id][0])
                        plt.plot([vw_x,l_x],[l_y,l_y],net_color)
                    else:
                        if not cluster_id in v_wire_names_map[net]:
                            if cluster_id in v_wire_map:
                                v_wire_map[cluster_id] += 1
                            else:
                                v_wire_map[cluster_id] = 1

                            v_wire_names_map[net][cluster_id] = (v_wire_map[cluster_id], l_y, l_y)
                            # draw wire to vertical wire
                            vw_x = ( schematic.figure_margin
                                    + schematic.cell_seperation_x * schematic.wire_split
                                    + schematic.cell_seperation_x * cluster_id
                                    + schematic.wire_seperation * v_wire_names_map[net][cluster_id][0])
                            plt.plot([vw_x,l_x],[l_y,l_y],net_color)
                        else:
                            vw = v_wire_names_map[net][cluster_id]
                            vw_max = max(vw[1],l_y)
                            vw_min = min(vw[2],l_y)

                            v_wire_names_map[net][cluster_id] = (vw[0], vw_max, vw_min)
                            # draw wire to vertical wire
                            vw_x = ( schematic.figure_margin
                                    + schematic.cell_seperation_x * schematic.wire_split
                                    + schematic.cell_seperation_x * cluster_id
                                    + schematic.wire_seperation * v_wire_names_map[net][cluster_id][0])
                            plt.plot([vw_x,l_x],[l_y,l_y],net_color)

            else:
                shout('ERROR', '%s net is driving %s which is not type PIN' % (net, load))

        net_pos_[0] = net_pos_[0]/(len(net.getDrivers()) + len(net.getLoads()))
        net_pos_[1] = net_pos_[1]/(len(net.getDrivers()) + len(net.getLoads()))

    # draw vertical wires
    for net,vwires in v_wire_names_map.items():

        # multiple v_wires need to be connected with h_wire
        vwire_count=0
        prev_cluster=0
        prev_c_y_max=0
        prev_c_y_min=0
        prev_c_x   =0

        ordered_vwires = collections.OrderedDict(sorted(vwires.items()))

        for cluster_id,vw_descript in ordered_vwires.items():

            c_x = ( schematic.figure_margin
                    + schematic.cell_seperation_x * schematic.wire_split
                    + schematic.cell_seperation_x * (cluster_id)
                    + schematic.wire_seperation * (vw_descript[0]) )
            c_y_max = vw_descript[1]
            c_y_min = vw_descript[2]

            vwire_count += 1
            # draw h_wire if needed
            if vwire_count > 1:
                if net in h_wire_names_map:
                    for hc_height, hw_descript in h_wire_names_map[net].items():
                        hw_x_max = hw_descript[1]
                        hw_x_min = hw_descript[2]
                        hw_y     = (hc_height * schematic.cell_seperation_y
                                    + schematic.wire_split * schematic.cell_seperation_y
                                    + schematic.wire_seperation * hw_descript[0])
                        h_wire_names_map[net][hc_height] = (hw_descript[0], hw_x_min, c_x)
                        plt.plot([hw_x_max, c_x],[hw_y, hw_y],net.getAttribute('color'))

                        # IMPORTANT: below changes are not stored in dicitonary
                        if hw_y > c_y_max:
                            c_y_max = hw_y
                        elif hw_y < c_y_min:
                            c_y_min = hw_y

                else:
                    # check min_max to see common y for two vwires
                    sup_min = min(c_y_max, prev_c_y_max)
                    sup_max = max(c_y_min, prev_c_y_min)
                    if prev_c_y_min > c_y_max :
                        hw_cluster_height = int(prev_c_y_min / schematic.cell_seperation_y)
                        if hw_cluster_height in h_wire_map:
                            h_wire_map[hw_cluster_height] += 1
                        else:
                            h_wire_map[hw_cluster_height] = 1

                        hw_y = (hw_cluster_height * schematic.cell_seperation_y
                                + schematic.wire_split * schematic.cell_seperation_y
                                + schematic.wire_seperation * h_wire_map[hw_cluster_height] )

                        hw_x_min = prev_c_x
                        hw_x_max = c_x
                        h_wire_names_map[net] = { hw_cluster_height : (h_wire_map[hw_cluster_height], hw_x_max, hw_x_min) }
                        # plot horizontal wire
                        plt.plot([hw_x_min, hw_x_max],[hw_y, hw_y], net.getAttribute('color'))
                        # feedback check: if not prev_c_y_max >= hw_y >= prev_c_y_min need to extend prev_vwire
                        if prev_c_y_max < hw_y:
                            plt.plot([prev_c_x, prev_c_x], [prev_c_y_max, hw_y], net.getAttribute('color'))
                            prev_c_y_max = hw_y
                        elif prev_c_y_min > hw_y:
                            plt.plot([prev_c_x, prev_c_x], [prev_c_y_min, hw_y], net.getAttribute('color'))
                            prev_c_y_min = hw_y

                        # IMPORTANT: below extension is not stored in dictionary
                        c_y_max = hw_y

                    elif prev_c_y_max < c_y_min :
                        hw_cluster_height = int(prev_c_y_min / schematic.cell_seperation_y)
                        if hw_cluster_height in h_wire_map:
                            h_wire_map[hw_cluster_height] += 1
                        else:
                            h_wire_map[hw_cluster_height] = 1

                        hw_y = (hw_cluster_height * schematic.cell_seperation_y
                                + schematic.wire_split * schematic.cell_seperation_y
                                + schematic.wire_seperation * h_wire_map[hw_cluster_height] )
                        hw_x_min = prev_c_x
                        hw_x_max = c_x
                        h_wire_names_map[net] = { hw_cluster_height : (h_wire_map[hw_cluster_height], hw_x_max, hw_x_min) }
                        # plot horizontal wire
                        plt.plot([hw_x_min, hw_x_max],[hw_y, hw_y], net.getAttribute('color'))
                        # feedback check: if not prev_c_y_max >= hw_y >= prev_c_y_min need to extend prev_vwire
                        if prev_c_y_max < hw_y:
                            plt.plot([prev_c_x, prev_c_x], [prev_c_y_max, hw_y], net.getAttribute('color'))
                            prev_c_y_max = hw_y
                        elif prev_c_y_min > hw_y:
                            plt.plot([prev_c_x, prev_c_x], [prev_c_y_min, hw_y], net.getAttribute('color'))
                            prev_c_y_min = hw_y

                        # IMPORTANT: below extension is not stored in dictionary
                        c_y_min = hw_y

                    else:
                        cluster_height_up   = int(prev_c_y_max / schematic.cell_seperation_y)
                        cluster_height_down = int(prev_c_y_min / schematic.cell_seperation_y)
                        if cluster_height_up == cluster_height_down:
                            shout('WARN', 'h wire cluster %d' % cluster_height_up)
                            shout('WARN', 'Not implemented yet')
                        else:
                            hw_cluster_height = int((cluster_height_down + cluster_height_up)/2)
                            if hw_cluster_height in h_wire_map:
                                h_wire_map[hw_cluster_height] += 1
                            else:
                                h_wire_map[hw_cluster_height] = 1

                            hw_y = (hw_cluster_height * schematic.cell_seperation_y
                                    + schematic.wire_split * schematic.cell_seperation_y
                                    + schematic.wire_seperation * h_wire_map[hw_cluster_height] )
                            hw_x_min = prev_c_x
                            hw_x_max = c_x

                            h_wire_names_map[net] = { hw_cluster_height : (h_wire_map[hw_cluster_height], hw_x_max, hw_x_min) }

                            # extend vwire if needed IMPORTANT: new change is not stored in dictionary
                            if hw_y > c_y_max:
                                c_y_max = hw_y
                            elif hw_y < c_y_min:
                                c_y_min = hw_y
                            # plot horizontal wire
                            plt.plot([hw_x_min, hw_x_max],[hw_y, hw_y], net.getAttribute('color'))
                            # feedback check: if not prev_c_y_max >= hw_y >= prev_c_y_min need to extend prev_vwire
                            if prev_c_y_max < hw_y:
                                plt.plot([prev_c_x, prev_c_x], [prev_c_y_max, hw_y], net.getAttribute('color'))
                                prev_c_y_max = hw_y
                            elif prev_c_y_min > hw_y:
                                plt.plot([prev_c_x, prev_c_x], [prev_c_y_min, hw_y], net.getAttribute('color'))
                                prev_c_y_min = hw_y


            # update prev_cluster
            prev_cluster = cluster_id
            prev_c_y_max = c_y_max
            prev_c_y_min = c_y_min
            prev_c_x     = c_x

            # plot vertical wire
            plt.plot([c_x,c_x],[c_y_max,c_y_min],net.getAttribute('color'))

    # draw pins
    nx.draw_networkx_nodes(netlist._graph, pos, node_shape='>', node_size=schematic.pin_size, node_color='c', nodelist=schematic.pinList)
    # draw cells
    nx.draw_networkx_nodes(netlist._graph, pos, node_shape='s', node_size=schematic.cell_size, node_color='y', nodelist=schematic.gateList)
    # draw nets
    nx.draw_networkx_nodes(netlist._graph, pos, node_shape='d', node_size=1, node_color='m', nodelist=schematic.netList)

    #Stop drawing edges because we want to display routes
    #nx.draw_networkx_edges(netlist._graph,pos)
    nx.draw_networkx_labels(netlist._graph,pos, labels=schematic.labels)


    plt.axis('equal')
    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig
