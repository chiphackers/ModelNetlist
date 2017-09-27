import sys
from SimpleNetlist import * 
def Gen
if __name__ == '__main__':
    netlist = SimpleNetlist('top')
    and1 = AND2(netlist)
    or1 = OR2(netlist)
    inv1 = INV(netlist)
    net1 = Net(netlist)
    net2 = Net(netlist)
    net3 = Net(netlist)
    
    netlist.addCell(and1)
    netlist.addCell(or1)
    netlist.addCell(inv1)

    net1.addDriver(and1.output(0))
    net1.addLoad(or1.input(0))
    netlist.addNet(net1)

    net2.addDriver(or1.output(0))
    net2.addLoad(inv1.input(0))
    netlist.addNet(net2)

    or1.input(0)

    netlist.saveGraph('test.png')
    return netlist

