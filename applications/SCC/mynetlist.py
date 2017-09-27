from SimpleNetlist import *
from commons import *

__name__ = '__main2__'

### NET LIST ####
if __name__ == '__main2__':
    netlist = SimpleNetlist('top')
    
    AND_1=AND2(netlist)
    AND_2=AND2(netlist)
    OR_1=OR2(netlist)
    OR_2=OR2(netlist)
    XOR_1=XOR2(netlist)
    XOR_2=XOR2(netlist)

    netlist.addCell(AND_1)
    netlist.addCell(AND_2)
    netlist.addCell(OR_1)
    netlist.addCell(OR_2)
    netlist.addCell(XOR_1)
    netlist.addCell(XOR_2)

    net0 = Net(netlist)
    net0.addLoad(XOR_1.input(0))
    net0.addLoad(AND_1.input(0))
    net0.addDriver(OR_2.output(0))
    netlist.addNet(net0)

    net1 = Net(netlist)
    net1.addDriver(AND_1.output(0))
    net1.addLoad(OR_1.input(0))
    netlist.addNet(net1)

    net2 = Net(netlist)
    net2.addDriver(OR_1.output(0))
    net2.addLoad(XOR_2.input(0))
    netlist.addNet(net2)

    net3 = Net(netlist)
    net3.addDriver(XOR_1.output(0))
    net3.addLoad(AND_2.input(0))
    netlist.addNet(net3)

    net4 = Net(netlist)
    net4.addDriver(AND_2.output(0))
    net4.addLoad(OR_2.input(0))
    netlist.addNet(net4)

    net5 = Net(netlist)
    net5.addLoad(AND_2.input(1))
    netlist.addNet(net5)

    net6 = Net(netlist)
    net6.addLoad(OR_2.input(1))
    netlist.addNet(net6)

    net7 = Net(netlist)
    net7.addDriver(XOR_2.output(0))
    net7.addLoad(AND_1.input(1))
    netlist.addNet(net7)

    net8 = Net(netlist)
    net8.addLoad(OR_1.input(1))
    netlist.addNet(net8)

    net9 = Net(netlist)
    net9.addLoad(XOR_1.input(1))
    netlist.addNet(net9)

    net10 = Net(netlist)
    net10.addLoad(XOR_2.input(1))
    netlist.addNet(net10)

    drawNetlist(netlist,'test.png')

