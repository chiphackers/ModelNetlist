from SimpleNetlist import *
from commons import *

netlist = SimpleNetlist('top')
AND2_0=AND2(netlist)
AND2_0.setAttribute('delay',3)
AND2_1=AND2(netlist)
AND2_1.setAttribute('delay',3)
AND2_2=AND2(netlist)
AND2_2.setAttribute('delay',3)
AND2_3=AND2(netlist)
AND2_3.setAttribute('delay',3)
INV_0=INV(netlist)
INV_0.setAttribute('delay',2)
INV_1=INV(netlist)
INV_1.setAttribute('delay',2)
INV_2=INV(netlist)
INV_2.setAttribute('delay',20)


netlist.addCell(AND2_0)
netlist.addCell(AND2_1)
netlist.addCell(AND2_2)
netlist.addCell(AND2_3)
netlist.addCell(INV_0)
netlist.addCell(INV_1)
netlist.addCell(INV_2)

net0 = Net(netlist)
net0.addLoad(AND2_0.input(0))
netlist.addNet(net0)

net1=Net(netlist)
net1.addLoad(AND2_0.input(1))
netlist.addNet(net1)

net2 = Net(netlist)
net2.addLoad(AND2_1.input(0))
netlist.addNet(net2)

net3=Net(netlist)
net3.addLoad(AND2_1.input(1))
net3.addLoad(INV_2.input(0))
netlist.addNet(net3)

net4=Net(netlist)
net4.addDriver(AND2_0.output(0))
net4.addLoad(AND2_2.input(0))
netlist.addNet(net4)

net5=Net(netlist)
net5.addDriver(AND2_1.output(0))
net5.addLoad(AND2_2.input(1))
net5.addLoad(INV_0.input(0))
netlist.addNet(net5)

net6=Net(netlist)
net6.addDriver(AND2_2.output(0))
net6.addLoad(INV_1.input(0))
netlist.addNet(net6)

net7=Net(netlist)
net7.addDriver(INV_1.output(0))
net7.addLoad(AND2_3.input(0))
netlist.addNet(net7)

net8=Net(netlist)
net8.addDriver(INV_0.output(0))
net8.addLoad(AND2_3.input(1))
netlist.addNet(net8)

net9=Net(netlist)
net9.addDriver(AND2_3.output(0))
net9.addDriver(INV_2.output(0))
netlist.addNet(net9)

drawNetlist(netlist, 'test.png')
