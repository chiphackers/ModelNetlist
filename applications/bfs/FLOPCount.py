from mynetlist import *

def FlopCount(netlist, start):
    explored=[]
    queue=[]+start
    FLOPS=[]
    while queue:
        node = queue.pop(0)
        if node not in explored:
            if type(node)==AND2:
                FLOPS.append(node)
            explored.append(node)
            neighbours = netlist.getNeighbours(node)
        for neighbour in neighbours:
            queue.append(neighbour)
    return FLOPS

def printFLOPS(inputPoints):
    flop=FlopCount(netlist, inputPoints)
    for i in flop:
        print(i)

    print("FlopCount :"+str(len(flop)))    
            
printFLOPS([and1.input(0),net3])
