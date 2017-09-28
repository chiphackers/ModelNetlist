from mynetlist2 import *
######### Anushka_Siriweera ####### Hasitha_Prashan ##########
def dijkstra_critical_path(netlist,start,end):
        d=0
        vertices=[]
        visited=[]
        predecessor=[]
        tempD=float("inf")
        gateDelay=0
        #setting 3 attributes to each net 
        for node in netlist._graph.nodes():
            if(node.getType()=='NET'):
                node.setAttribute('minDisNeg',float("inf"))
                node.setAttribute('critical_delay',float("inf"))
                node.setAttribute('predecessor',node.getName())
                vertices.append(node)
        #traversing the net according to dijkstra and updating attributes
        while(True):
            for vertex in vertices:
                if(vertex.getName()==start):
                    vertex.setAttribute('minDisNeg',d)
                    for successorPin in vertex._loads:
                        parentCell = successorPin.getParent()
                        for successor in parentCell.getOutputs():
                            for net in netlist.getNeighbours(successor):
                                if(net.getAttribute("minDisNeg") != None):
                                    gateDelay=successorPin.getParent().getAttribute('delay')
                                    if(net.getAttribute("minDisNeg")> d-gateDelay):
                                        net.setAttribute("minDisNeg",d-gateDelay)
                                        net.setAttribute("critical_delay",-1*(d-gateDelay))
                                        net.setAttribute("predecessor",vertex.getName())
                    visited.append(vertex)

            for v in vertices:
                if v not in visited:
                        if((v.getAttribute("minDisNeg"))<=tempD):
                            tempD=float(v.getAttribute("minDisNeg"))
                            start=v.getName()
                d=tempD
            tempD=float("inf")
            if(len(vertices)==len(visited)):break

        #now the attributes(minimum_distance,predecessor) are set
        print("minimum distance and the route")
        #generating a list for the path to follow and printing it out
        traverse_order=[end]
        end_temp=end
        breaker=0
        while (breaker !=1):
            for vertex in vertices:
                if (vertex.getName()==end_temp):
                    if(end_temp==end):
                        print (vertex.getAttribute('critical_delay'))
                    end_temp=(vertex.getAttribute('predecessor'))
                    if(end_temp==vertex.getName()):
                        traverse_order.reverse()
                        print (traverse_order)
                        breaker=1
                        break
                    traverse_order.append(vertex.getAttribute('predecessor'))


dijkstra_critical_path(netlist,"NET_3","NET_9")

