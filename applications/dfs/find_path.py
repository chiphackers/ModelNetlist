def find_path(netlist, start, end): #In signal flow direction
    #start is a node
    s = [(start,[start])]
    paths = []
    fanOutPins = []

    while (s):
        (node,path) = s.pop()
        neighbours = netlist.getNeighbours(node)
        fanOutPins.clear()
        
        if (type(node) == "CELL"):
            for i in neighbours:
                if i in node.getInputs():
                    fanOutPins.append(i)          

        for child in set(neighbours) - set(path) - set(fanOutPins):
            if child == end :
                paths.append(path + [child])
            else:
                s.append((child,path + [child]))
                
    return paths
