from .nlNode import *

@static_vars(inst=0)
class Net(nlNode):
    """
    Generic Wire class
    """
    def __init__(self, parent):
        name = 'NET_%d' % Net.inst
        super().__init__('NET', name, parent)
        self._drivers = []
        self._loads = []
        Net.inst += 1
        parent._netList.append(self)

    def addLoad(self, load):
        self._loads.append(load)
        if load.getType() == 'PIN':
            load.connectNet(self)

    def getLoads(self):
        return self._loads

    def addDriver(self, driver):
        self._drivers.append(driver)
        if driver.getType() == 'PIN':
            driver.connectNet(self)

    def getDrivers(self):
        return self._drivers

    def populateNetGraph(self):
        netGraph = nx.DiGraph()

        for load in self._loads:
            netGraph.add_edge(self, load)

        for driver in self._drivers:
            netGraph.add_edge(driver, self)

        return netGraph

