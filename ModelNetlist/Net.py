from .nlNode import *

@static_vars(inst=0)
class Net(nlNode):
    """
    Generic Wire class
    """
    def __init__(self, parent):
        name = 'NET_%d' % Net.inst
        super().__init__('NET', name, parent)
        self._drivers = set()
        self._loads = set()
        self._bus = None
        Net.inst += 1
        if parent.getType() == 'BUS':
            self._bus = parent
        while parent.getType() != 'NETLIST':
            parent = parent.getParent()
            if parent is None:
                shout('ERROR', '{} net does not belongs to a netlist'.format(name))

        self._netlist = parent
        self._netlist._netList.append(self)

    def addLoad(self, load):
        self._loads.add(load)
        if load.getType() == 'PIN':
            load.connectNet(self)
        else:
            shout('WARN', 'Attempt to add load {} failed'.format(load))

    def removeLoad(self, load):
        if load in self._loads:
            self._loads.remove(load)
            if load.getType() == 'PIN':
                load.disconnectNet()

    def getLoads(self):
        return self._loads

    def addDriver(self, driver):
        self._drivers.add(driver)
        if driver.getType() == 'PIN':
            driver.connectNet(self)
        else:
            shout('WARN', 'Attempt to add driver {} failed'.format(driver))

    def removeDriver(self, driver):
        if driver in self._drivers:
            self._drivers.remove(driver)
            if driver.getType() == 'PIN':
                driver.disconnectNet()

    def getDrivers(self):
        return self._drivers

    def getParentBus(self):
        return self._bus

    def populateNetGraph(self):
        netGraph = nx.DiGraph()

        for load in self._loads:
            netGraph.add_edge(self, load)

        for driver in self._drivers:
            netGraph.add_edge(driver, self)

        return netGraph

