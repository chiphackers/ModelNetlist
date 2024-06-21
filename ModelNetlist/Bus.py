from .nlNode import *
from .Net import Net

@static_vars(inst=0)
class Bus(nlNode):
    """
    A bus is a group of nets
    """
    def __init__(self, name, parent, lsb=0, msb=1):
        super().__init__('BUS', name, parent)
        self._lsb = lsb
        self._msb = msb
        self._nets = self.getWidth()*[Net(self)]
        Bus.inst += 1
        for i in range(0, self.getWidth()):
            self._nets[i] = Net(self)
            self._nets[i].setName('[{}]'.format(i))
        parent._netList.append(self)

    def getLSB(self):
        return self._lsb

    def getMSB(self):
        return self._msb

    def getWidth(self):
        return (self._msb+1-self._lsb)

    def getNet(self, index):
        if index < self._lsb or index > self._msb:
            shout('ERROR', 'Index out of range')
        return self._nets[index-self._lsb]

    def setNet(self, index, net):
        if net.getType() != 'NET':
            shout('WARN', '{} is not a net'.format(net.getName()))
        if self.getnet(index) != None:
            shout('WARN', 'An old net is replaced by {}'.format(net.getName()))
        self._nets[index-self._lsb] = net

    def addLoad(self, load, bus_lsb=0, bus_msb=-1):
        if load.getType() == 'PORT':
            if bus_msb < 0:
                bus_msb = self._msb
            lindex = load.getLSB()
            for i in range(bus_lsb, bus_msb+1):
                self.getNet(i).addLoad(load.getPin(lindex))
                lindex += 1
            load.connectBus(self)

        # Allow connecting a single net to a pin
        elif bus_msb < 0 and load.getType() == 'PIN':
            self.getNet(bus_lsb).addLoad(load)
        else:
            shout('ERROR', 'No idea how to connect {} and {}'.format(self, load))

    def removeLoad(self, load):
        if load.getType() == 'PORT':
            port_lsb = load.getLSB()
            port_msb = load.getMSB()
            for i in range(port_lsb, port_msb+1):
                net = load.getPin(i).getConnectedNet()
                if net is not None:
                    if net.getParentBus() == self:
                        net.removeLoad(load.getPin(i))

            load.disconnectBus()
        elif load.getType() == 'PIN':
            for i in range(self._lsb, self._msb+1):
                net = self.getNet(i)
                if load in net.getLoads():
                    net.removeLoad(load)

    def getLoads(self, index=-1):
        if index <0 :
            loads = set()
            for net in self._nets:
                loads.update(net.getLoads())
            return loads
        else:
            return self.getNet(index).getLoads()

    def addDriver(self, driver, bus_lsb=0, bus_msb=-1):
        if driver.getType() == 'PORT':
            if bus_msb < 0:
                bus_msb = self._msb
            lindex = driver.getLSB()
            for i in range(bus_lsb, bus_msb+1):
                self.getNet(i).addDriver(driver.getPin(lindex))
                lindex += 1
            driver.connectBus(self)

        # Allow connecting a single net to a pin
        elif bus_msb < 0 and driver.getType() == 'PIN':
            self.getNet(bus_lsb).addDriver(driver)
        else:
            shout('ERROR', 'No idea how to connect {} and {}'.format(self, load))

    def removeDriver(self, driver):
        if load.getType() == 'PORT':
            port_lsb = load.getLSB()
            port_msb = load.getMSB()
            for i in range(port_lsb, port_msb+1):
                net = driver.getPin(i).getConnectedNet()
                if net is not None:
                    if net.getParentBus() == self:
                        net.removeLoad(driver.getPin(i))

            driver.disconnectBus()
        elif driver.getType() == 'PIN':
            for i in range(self._lsb, self._msb+1):
                net = self.getNet(i)
                if driver in net.getDrivers():
                    net.removeDriver(driver)

    def getDrivers(self, index=-1):
        if index < 0:
            drivers = set()
            for net in self._nets:
                drivers.update(net.getDrivers())
            return drivers
        else:
            return self.getNets(index).getDrivers()

    # Below API name must match the same name of the corresponding NET API
    def populateNetGraph(self):
        netGraph = nx.DiGraph()

        for i in range(self._lsb, self._msb):
            net = self.getNet(i)
            for load in net.getLoads():
                netGraph.add_edge(self, load)

            for driver in net.getDrivers():
                netGraph.add_edge(driver, self)

        return netGraph

