import unittest
from ModelNetlist import *

class TestRouting(unittest.TestCase):

    netlist = ModelNetlist('top')

    @classmethod
    def setUpClass(cls):
        print('Running schematic routing tests...')

    @classmethod
    def tearDownClass(cls):
        cls.netlist.build()
        schematic = Schematic(cls.netlist)
        schematic.pin_labels = False
        drawNetlist(schematic,'routing_test.png')
        print('Completed routing tests. Please check routing_test.png for results.')

    def test_direct_wire(self):
        and0 = AND2(self.netlist)
        and1 = AND2(self.netlist)
        net  = Net(self.netlist)

        net.addDriver(and0.output(0))
        net.addLoad(and1.input(0))

    def test_one_to_many(self):
        and0 = AND2(self.netlist)
        and1 = AND2(self.netlist)
        and2 = AND2(self.netlist)
        and3 = AND2(self.netlist)
        net = Net(self.netlist)

        net.addDriver(and0.output(0))
        net.addLoad(and1.input(0))
        net.addLoad(and2.input(0))
        net.addLoad(and3.input(0))

    def test_between_clusters(self):
        and0 = AND2(self.netlist)
        and1 = AND2(self.netlist)
        and2 = AND2(self.netlist)
        inv  = INV(self.netlist)
        net0 = Net(self.netlist)
        net1 = Net(self.netlist)
        net2 = Net(self.netlist)

        net0.addDriver(and0.output(0))
        net0.addLoad(and2.input(0))
        net0.addLoad(and1.input(0))
        net0.addLoad(inv.input(0))
        net1.addDriver(inv.output(0))
        net1.addLoad(and1.input(1))
        net2.addDriver(and1.output(0))
        net2.addLoad(and2.input(1))

    def test_loops(self):
        inv0 = INV(self.netlist)
        inv1 = INV(self.netlist)
        inv2 = INV(self.netlist)
        inv3 = INV(self.netlist)
        and0 = AND2(self.netlist)
        and1 = AND2(self.netlist)
        net0 = Net(self.netlist)
        net1 = Net(self.netlist)
        net2 = Net(self.netlist)
        net3 = Net(self.netlist)
        net4 = Net(self.netlist)
        net5 = Net(self.netlist)

        net0.addDriver(inv0.output(0))
        net0.addLoad(and0.input(0))
        net1.addDriver(and0.output(0))
        net1.addLoad(and0.input(1))
        net1.addLoad(inv1.input(0))
        net2.addDriver(inv1.output(0))
        net2.addLoad(and1.input(0))
        net3.addDriver(and1.output(0))
        net3.addLoad(inv2.input(0))
        net4.addDriver(inv2.output(0))
        net4.addLoad(inv3.input(0))
        net5.addDriver(inv3.output(0))
        net5.addLoad(and1.input(1))

    def test_input_ports(self):
        netlist = self.netlist
        netlist.addPort('in','in0')
        netlist.addPort('in','in1')
        netlist.addPort('in','in2')

        and0 = AND2(netlist)
        and1 = AND2(netlist)
        and2 = AND2(netlist)

        net0 = Net(netlist)
        net0.addDriver(netlist.getPort('in0'))
        net0.addLoad(and0.input(0))

        net1 = Net(netlist)
        net1.addDriver(netlist.getPort('in1'))
        net1.addLoad(and0.input(1))
        net1.addLoad(and1.input(0))

        net2 = Net(netlist)
        net2.addDriver(netlist.getPort('in2'))
        net2.addLoad(and1.input(1))
        net2.addLoad(and2.input(0))

        net3 = Net(netlist)
        net3.addDriver(and1.output(0))
        net3.addLoad(and2.input(1))

    def test_output_ports(self):
        netlist = self.netlist
        netlist.addPort('in','in3')
        netlist.addPort('in','in4')
        netlist.addPort('out','out0')
        netlist.addPort('out','out1')
        netlist.addPort('out','out2')
        netlist.addPort('out','out3')

        and0 = AND2(netlist)
        and1 = AND2(netlist)
        inv0 = INV(netlist)

        net0 = Net(netlist)
        net0.addDriver(and0.output(0))
        net0.addLoad(netlist.getPort('out0'))

        net1 = Net(netlist)
        net1.addDriver(inv0.output(0))
        net1.addLoad(and1.input(0))

        net2 = Net(netlist)
        net2.addDriver(and1.output(0))
        net2.addLoad(netlist.getPort('out1'))

        net3 = Net(netlist)
        net3.addDriver(netlist.getPort('in3'))
        net3.addLoad(netlist.getPort('out2'))

        net4 = Net(netlist)
        net4.addDriver(netlist.getPort('in4'))
        net4.addLoad(netlist.getPort('out3'))

if __name__ == '__main__':
    unittest.main()
