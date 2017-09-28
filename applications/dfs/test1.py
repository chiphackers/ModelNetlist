import sys
from mynetlist import *

def find_path(netlist, start, end): #In signal flow direction
    #start is a node
    s = [(start,[start])]
    paths = []
    fanOutPins = []

    while (s):
        (node,path) = s.pop()
        neighbours = netlist.getNeighbours(node)
        fanOutPins.clear()
        
        if (type(node) == "GATE"):
            for i in neighbours:
                if i in node.getInputs():
                    fanOutPins.append(i)          

        for child in set(neighbours) - set(path) - set(fanOutPins):
            if child == end :
                paths.append(path + [child])
            else:
                s.append((child,path + [child]))
                
    return paths

def find_skewness(netlist, clock, gate1, gate2):
    if (is_a_path(netlist,clock,gate1) and is_a_path(netlist,clock,gate2)):
        delay_path1 = find_delay_max(netlist, clock, gate1)
        delay_path2 = find_delay_max(netlist, clock, gate2)
        return abs(delay_path1 - delay_path2)
    else:
        return None
    
def find_delay_max(netlist, clock, gate):
    delayMax = 0
    for oPin in clock.outputs:
        paths = find_path(netlist, oPin, gate) #check if no path            
        for path in paths:
            delayPath = 0
            for i in range(0,len(path)-1):
                if path[i].getAttribute('delay')!=None:
                    delayPath += path[i].getAttribute('delay')
            if delayPath > delayMax:
                delayMax =  delayPath
    return delayMax

def is_a_path(netlist, clock, node):
    for oPin in clock.outputs:
        paths = find_path(netlist, oPin, node) #check if no path            
        if paths != []:
            return True
    else:
        return False
    
    
def find_skewed_gates(netlist, clock, delayNode,*gates):
    gateSet = set()
    for gate in gates: 
        if find_delay_max(netlist, clock, gate) == delayNode:
            gateSet.add(gate)
    
    return gateSet

def find_convergence(netlist, clock1,clock2,gate):
    inputPins =  gate.getInputs()
    clock_paths = (is_a_path(netlist, clock1, inputPins[0]) , is_a_path(netlist, clock2, inputPins[0]))
    if clock_paths == (True,True):
        return False

    elif clock_paths == (True,False):
        for i in range(1,len(inputPins)):
            if is_a_path(netlist, clock1, inputPins[i])==False:
                return False
        else:
            return True

    elif clock_path == (False,True):
        for i in range( 1, len(inputPins)):
            if is_a_path(netlist, clock2, inputPins[i])==False:
                return False
        else:
            return True
    else:
        return True

            

if __name__ == '__main__':

    path = find_path(netlist, net1, net4)

    for i in path:
        print("new path ")
        for j in i:
            #for z in j:
            print(j)

     
    print('\nskewness') 
    print(find_skewness(netlist, clk1, and2, and1))
     
    print('\ngates with same skewness')
    #for node in find_skewed_gates(netlist, inv1.input(0),8,inv1,or1,and1,inv2,or2):
    for node in find_skewed_gates(netlist, clk1,6,inv1,and2,or1,and1,inv2,or2):
        print(node)
    
    
    print('\nfind convergence')
    print(find_convergence(netlist, clk1,clk2,and2))
    #print(find_convergence(clock1,clock2,and1))
    
