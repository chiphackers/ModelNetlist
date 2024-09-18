from ModelNetlist import *

import unittest

class TestVerilogNetlists(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Reading liberty file')
        cls.library = readLiberty('../gscl45nm.lib')
        print('Running verilog tests')

    @classmethod
    def tearDownClass(cls):
        print('Completed verilog tests')

    def test_read_liberty(self):
        self.assertIsNotNone(self.library)

    def test_lib_content(self):
        if not self.library:
            print('Reading liberty file has failed!')
            assert False
        else:
            assert len(self.library.listCells()) > 0

    def test_getCell_from_lib(self):
        if not self.library:
            print('Reading liberty file has failed!')
            assert False
        else:
            cell = self.library.getCell('AND2X2')
            if cell is None:
                assert False
            else:
                print(type(cell))

    def test_simple_comb(self):
        if not self.library:
            print('Reading liberty file has failed!')
            assert False
        else:
            netlist = readVerilogNetlist('simple.v', [self.library])
            gateCount = len(netlist.getCells())
            wireCount = len(netlist.getNets())
            print('Netlist has %d gates and %d nets.' % (gateCount, wireCount))



if __name__ == '__main__':
    unittest.main()
