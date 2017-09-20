from netlist import *

netlist = NetList('top1')
and1 = AND2(netlist)
or1 = OR2(netlist)
inv1 = INV(netlist)
and2= AND2(netlist)
   
netlist.addGate(and1)
netlist.addGate(or1)
netlist.addGate(inv1)
netlist.addGate(and2)

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
net3.addDriver(and1.input(1))
net3.addLoad(and2.input(1))
net3.addLoad(or1.input(1))
netlist.addNet(net3)

netlist.saveGraph('test1.png')

