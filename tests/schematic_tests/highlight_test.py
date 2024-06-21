import unittest
from ModelNetlist import *

class TestHighlight(unittest.TestCase):

    netlist = ModelNetlist('top')

    @classmethod
    def setUpClass(cls):
        print('Running schematic highlight tests...')
        netlist = cls.netlist
        netlist.addPort('in', 'c0')
        netlist.addPort('in', 'b0')
        netlist.addPort('in', 'a0')

        netlist.addPort('out', 's0')
        netlist.addPort('out', 'c1')

        xor0 = XOR2(netlist)
        xor1 = XOR2(netlist)

        and0 = AND2(netlist)
        and1 = AND2(netlist)

        or0 = OR2(netlist)
        or1 = OR2(netlist)

        net0 = Net(netlist)
        net0.addDriver(netlist.getPort('c0'))
        net0.addLoad(xor0.input(0))
        net0.addLoad(or0.input(0))
        net0.addLoad(and1.input(0))

        net1 = Net(netlist)
        net1.addDriver(netlist.getPort('b0'))
        net1.addLoad(xor0.input(1))
        net1.addLoad(and0.input(0))

        net2 = Net(netlist)
        net2.addDriver(netlist.getPort('a0'))
        net2.addLoad(xor1.input(0))
        net2.addLoad(or0.input(1))
        net2.addLoad(and1.input(1))

        net3 = Net(netlist)
        net3.addDriver(xor0.output(0))
        net3.addLoad(xor1.input(1))

        net4 = Net(netlist)
        net4.addDriver(xor1.output(0))
        net4.addLoad(netlist.getPort('s0'))

        net8 = Net(netlist)
        net8.addDriver(or0.output(0))
        net8.addLoad(and0.input(1))

        net11 = Net(netlist)
        net11.addDriver(and0.output(0))
        net11.addLoad(or1.input(0))

        net12 = Net(netlist)
        net12.addDriver(and1.output(0))
        net12.addLoad(or1.input(1))

        net13 = Net(netlist)
        net13.addDriver(or1.output(0))
        net13.addLoad(netlist.getPort('c1'))

    @classmethod
    def tearDownClass(cls):
        cls.netlist.build()
        schematic = Schematic(cls.netlist)
        schematic.wire_color = 'gray'
        drawNetlist(schematic,'highlight_test.png')
        print('Completed highlighting tests. Please check highlight_test.png for results.')

    def testInputToOutput(self):
        a0 = self.netlist.getPort('a0')
        s0 = self.netlist.getPort('s0')

        dfs_stack = [ a0 ]
        dfs_parent = { a0: None }
        path_found = False
        while len(dfs_stack) > 0 and not path_found:
            node = dfs_stack.pop()
            if node.getType() == 'PIN':
                if node is s0:
                    shout('INFO','Path found from a0 -> s0')
                    path_found = True
                else:
                    parent = node.getParent()
                    if parent.getType() == 'CELL':
                        if node in parent.getOutputs():
                            net = node.getConnectedNet()
                            if not net is None and not net in dfs_parent:
                                dfs_parent[net] = node
                                dfs_stack.append(net)
                        else:
                            if not parent in dfs_parent:
                                dfs_parent[parent] = node
                                dfs_stack.append(parent)
                    else:
                        net = node.getConnectedNet()
                        if not net is None and not net in dfs_parent:
                            dfs_parent[net] = node
                            dfs_stack.append(net)

            if node.getType() == 'NET':
                for load in node.getLoads():
                    if not load in dfs_parent:
                        dfs_parent[load] = node
                        dfs_stack.append(load)

            if node.getType() == 'CELL':
                for o in node.getOutputs():
                    if not o in dfs_parent:
                        dfs_parent[o] = node
                        dfs_stack.append(o)

        if path_found :
            parent = dfs_parent[s0]
            while not parent is None:
                if parent.getType() == 'NET':
                    parent.setAttribute('color','red')
                parent = dfs_parent[parent]
        else:
            shout('INFO','NO path found')

if __name__ == '__main__':
    unittest.main()
