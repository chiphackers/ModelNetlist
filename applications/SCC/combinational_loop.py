

from mynetlist import *


######################################################################
# Main Function
######################################################################




##### MY_APIs#######################

def adjNet(net):
    list=[]
    for d in net.listLoads():
        for p in d.getParent().getOutputs():
              for c in p.getNeighbours():
                  if c.getType()=='NET':
                     list.append(c)
    return list
def adjRNet(net):
    list=[]
    for d in net.listDrivers():
        for p in d.getParent().getInputs():
              for c in p.getNeighbours():
                  if c.getType()=='NET':
                     list.append(c)
    return list

   



def trv(net,visited,out):
    print(net.getName(),end='-visited , ')
    visited.add(net)
    adjNodes = set(adjNet(net)) - (set(adjNet(net)) & visited)
    if (len(adjNodes)==0):
        print(net.getName(),end='-cover ')
        out.append(net)
        
    else:
        while(len(adjNodes)!=0):
            n=adjNodes.pop()
            [visited,out]=trv(n,visited,out)
            
        if net not in out:
            print(net.getName(),end='-cover ')
            out.append(net)

    return [visited,out]

def trvR(net,visited,out):
    print(net.getName(),end='-visited , ')
    visited.add(net)
    adjNodes = set(adjRNet(net)) - (set(adjRNet(net)) & visited)
    if (len(adjNodes)==0):
        print(net.getName(),end='-cover ')
        out.append(net)
        
    else:
        while(len(adjNodes)!=0):
            n=adjNodes.pop()
            [visited,out]=trvR(n,visited,out)
            
        if net not in out:
            print(net.getName(),end='-cover ')
            out.append(net)

    return [visited,out]



def DFS(netlist):
    visited=set()
    out=[]
    nets_remain=set(netlist.getNets())
    adjNodes=set()
    while (len(nets_remain)!=0):
        net=list(nets_remain)[0]
        for x in nets_remain:
            if x.getName()=='NET_1':
                net=x

        [visited,out]=trv(net,visited,out)
        nets_remain=set(netlist.getNets())-set(out)
        print()

    return out

def SCC(netlist):
    DFSOut=DFS(netlist)
    print("\n DFS done","\n")
    visited=set()
    sccOut=[]
    while(len(DFSOut)!=0):
        n=DFSOut.pop()
        if n not in visited:
            out=[]
            temp=[]
            visited.add(n)
            [tepm,out]=trvR(n,visited,out)
            for t in temp:
                visited.add(t)
            sccOut.append(out)
        print()

    return sccOut

def CGates(net1,net2):
    set1=set()
    set2=set()
    for x in net1.listLoads():
        set1.add(x.getParent())
    for x in net2.listDrivers():
        set2.add(x.getParent())
    return list(set1 & set2)


#### Main code #################

DFSOut=SCC(netlist)

print("\n Results - SCC Components \n")

for j in DFSOut:
    for c in j: 
        print (c.getName(),end='  ')
    print()

print("\nFinal Combinational Loop Results\n")



loops=[]
for j in DFSOut:
    temp=[]
    if len(j)>1:
        for x in (range(len(j)-1)):
            temp.append(CGates(j[x],j[x+1]))
        temp.append(CGates(j[len(j)-1],j[0]))
        loops.append(temp)


for x in loops:
    for y in x:
        print("(",end='')
        #print(y)
        for z in y:
           print(z.getName(),end='/')
        print(")",end='--->')
    print()



   
    




        
