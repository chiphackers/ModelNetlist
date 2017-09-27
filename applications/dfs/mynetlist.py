from SimpleNetlist import *
from commons import *

netlist = SimpleNetlist('test1')

clk1 = Clock('clk1')
#netlist.clockList.append(clk1)
clk2 = Clock('clk2')
#netlist.clockList.append(clk2)

and1 = AND2(netlist)
and2 = AND2(netlist)
or1 = OR2(netlist)
or2 = OR2(netlist)
inv1 = INV(netlist)
inv2 = INV(netlist)

netlist.addCell(and1)
netlist.addCell(and2)
netlist.addCell(or1)
netlist.addCell(or2)
netlist.addCell(inv1)
netlist.addCell(inv2)

net1 = Net(netlist)
net1.addLoad(inv1.input(0))
net1.addLoad(or1.input(0))
netlist.addNet(net1)

net2 = Net(netlist)
net2.addLoad(and1.input(1))
netlist.addNet(net2)

net3 = Net(netlist)
net3.addDriver(inv1.output(0))
net3.addLoad(and1.input(0))
netlist.addNet(net3)

net4 = Net(netlist)
net4.addLoad(or1.input(1))
netlist.addNet(net4)


net5 = Net(netlist)
net5.addLoad(or2.input(1))
net5.addLoad(inv2.input(0))
net5.addDriver(or1.output(0))
netlist.addNet(net5)

net6 = Net(netlist)
net6.addDriver(and1.output(0))
net6.addLoad(and2.input(0))
net6.addLoad(or2.input(0))
netlist.addNet(net6)

net7 = Net(netlist)
net7.addDriver(inv2.output(0))
net7.addLoad(and2.input(1))
netlist.addNet(net7)


#net8 = Net(netlist)
#net8.addDriver(and2.output(0))
#netlist.addNet(net8)

#net9 = Net(netlist)
#net9.addDriver(or2.output(0))
#netlist.addNet(net9) 

netlist.saveGraph('ex.png')

'''
print("all neighbours of and2")
print(and2.getNeighbours())
print("\nneighbours of net5")
print(net5.getNeighbours())
print("\nneighbours of and1.outputs(0)")
print(and1.output(0).getNeighbours())
'''

inv1.input(0).setAttribute('clock',clk1)
or1.input(1).setAttribute('clock',clk1)
or1.input(0).setAttribute('clock',clk1)
and1.input(1).setAttribute('clock',clk1)
clk1.set_outputs(inv1.input(0))
clk1.set_outputs(or1.input(1))
clk1.set_outputs(or1.input(0))
clk1.set_outputs(and1.input(1))

''' 
net10 = Net(netlist)
net10.addDriver(clock1)
net10.addLoad(inv1.input(0))
net10.addLoad(and1.input(1))
netlist.addNet(net10)

net11 = Net(netlist)
net11.addDriver(clock2)
net11.addLoad(or1.input(1))
netlist.addNet(net11)
'''


and1.setAttribute('delay',0)
and2.setAttribute('delay',3)
or1.setAttribute('delay',4)
or2.setAttribute('delay',1)
inv1.setAttribute('delay',2)
inv2.setAttribute('delay',6)


net1.setAttribute('delay',2)
net2.setAttribute('delay',2)
net3.setAttribute('delay',2)
net4.setAttribute('delay',2)
net5.setAttribute('delay',2)
net6.setAttribute('delay',2)
net7.setAttribute('delay',2)

