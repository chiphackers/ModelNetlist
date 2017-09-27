from SimpleNetlist import *
from commons import *

netlist = SimpleNetlist('top1')
and1 = AND2(netlist)
or1 = OR2(netlist)
inv1 = INV(netlist)
and2= AND2(netlist)
   
netlist.addCell(and1)
netlist.addCell(or1)
netlist.addCell(inv1)
netlist.addCell(and2)

net1 = Net(netlist)
net1.addDriver(and1.output(0))
net1.addLoad(and2.input(0))
net1.addLoad(or1.input(0))
netlist.addNet(net1)

net2 = Net(netlist)
net2.addDriver(or1.output(0))
net2.addLoad(inv1.input(0))
netlist.addNet(net2)

net3 = Net(netlist)
net3.addDriver(and1.output(0))
net3.addLoad(and2.input(1))
net3.addLoad(or1.input(1))
netlist.addNet(net3)

netlist.addPort('in', 'clk')
netlist.addPort('in', 'in1')
netlist.addPort('out', 'out1')

net4 = Net(netlist)

for port in netlist.getInputPorts():
    print(port)
    net4.addDriver(port)


netlist.addNet(net4)


drawNetlist(netlist,'test1.png')
