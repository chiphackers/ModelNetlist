from find_path import *

def is_a_path(netlist, clock, node):
    for oPin in clock.outputs:
        paths = find_path(netlist, oPin, node) #check if no path            
        if paths != []:
            return True
    else:
        return False

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

