from find_path import *

def is_a_path(netlist, clock, node):
    for oPin in clock.outputs:
        paths = find_path(netlist, oPin, node) #check if no path            
        if paths != []:
            return True
    else:
        return False

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



def find_skewness(netlist, clock, gate1, gate2):
    if (is_a_path(netlist,clock,gate1) and is_a_path(netlist,clock,gate2)):
        delay_path1 = find_delay_max(netlist, clock, gate1)
        delay_path2 = find_delay_max(netlist, clock, gate2)
        return abs(delay_path1 - delay_path2)
    else:
        return None
