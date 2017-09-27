import sys
#from SimpleNetlist import *
from Netlist import *

######################################################################
#Topological Sorting
######################################################################

def visit(node):
    if  (graphNodes[node] == 'permanently_marked'):
    	return 
    elif (graphNodes[node]== 'temporary_marked'): 
    	print ("[ERROR] : Topological sort cannot be applied to DAGs. (Directed Acyclic Graphs)")
    	global SortedList_Var
    	SortedList_Var =False
    	return 
    elif ( graphNodes[node] == 'unmarked'):
    	graphNodes[node] = 'temporary_marked'
    	for adjcentNode in adjecncyList[node]:
    		visit(adjcentNode)
    	graphNodes[node] = 'permanently_marked'
    	SortedNodes_List.insert(0,node)
 
######################################################################
    elements=netlist.getNodes()
    gates=[]
    nets=[]
    for i in elements:
        if i.getType() == 'CELL':
            gates.append(i)
        elif i.getType() == 'NET':
            nets.append(i)
            print(i)
    
    adjecncyList={}
    for g in gates:
        name=g.getName()
        inputs=[]
        outputs=[]
        inputs=g.getInputs()
        outputs=g.getOutputs()

        for i in inputs:
            output_names=[]
            for o in outputs:
                if len(netlist.getNeighbours(o))==0 :
                    print("Fetching single neighbours : %s --> %s" % (o, str(netlist.getNeighbours(o))))
                    adjecncyList[str(o)]=[]
                output_names.append(str(o))
            adjecncyList[str(i)]=output_names
    for n in nets:
        out_nets=[]
        net_in=n.getDrivers()
        net_out=n.getLoads()
        for i in net_in:
            for o in net_out:
                if len(netlist.getNeighbours(o))==0 :
                    adjecncyList[str(o)]=[]
                out_nets.append(str(o))
            adjecncyList[str(i)]=out_nets

    keysList=adjecncyList.keys()
    graphNodes={}
    for k in keysList:
        graphNodes[k]='unmarked'
    print("Adjacency List of the Created Graph: ")
    print(adjecncyList)

    SortedNodes_List = []
    SortedList_Var= True
    print("Sorted List Of the Created Graph : ")
    for key in  keysList:
        if (graphNodes[key]) == 'unmarked':
	        node = key
	        visit(node)
    if (SortedList_Var):
        print (SortedNodes_List)
    else:
    	print ("[INFO]  : No Topological Node list genrated.Please enter Acyclic Directed Circuit (A Circuit with no feedbacks)")

#############################################################################################
