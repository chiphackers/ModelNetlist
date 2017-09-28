from mynetlist import *

def bfs(graph, start):
	explored=[]
	Path={'start':start}
	queue=[]+start
	while queue:
		node = queue.pop(0)
		if node not in explored:
			explored.append(node)
			neighbours = graph.neighbors(node)
			Path[node]=neighbours
			for neighbour in neighbours:
				queue.append(neighbour)
	return Path

def bfsT(graph, start,end):
	explored=[]
	Path={'start':start}
	queue=[]+start
	while queue:
		node = queue.pop(0)
		if end==node:
			return Path
		if node not in explored:
			explored.append(node)
			neighbours = graph.neighbors(node)
			Path[node]=neighbours
			for neighbour in neighbours:
				queue.append(neighbour)
	return Path

def bfsTS(graph, start,end,search):
	explored=[]
	Path={'start':start}
	queue=[]+start
	SEARCH=[]
	while queue:
		node = queue.pop(0)
		if end==node:
			return SEARCH
		if node not in explored:
			if node.getType()==search:
				SEARCH.append(node)
			explored.append(node)
			neighbours = graph.neighbors(node)
			Path[node]=neighbours
			for neighbour in neighbours:
				queue.append(neighbour)
	return SEARCH

def printPath(inputPoints):
	path=bfs(netlist._graph,inputPoints)
	for i in path:
		u=''
		for j in path[i]:
			u=str(j)+","+u
		print(str(i)+":"+u)	

def printPathT(inputPoints,endPoint):
	path=bfsT(netlist._graph,inputPoints,endPoint)
	for i in path:
		u=''
		for j in path[i]:
			u=str(j)+","+u
		print(str(i)+":"+u)	

def printPathTS(inputPoints,endPoint,search):
	path=bfsTS(netlist._graph,inputPoints,endPoint,search)
	for i in path:
		print(str(i))

#printPath([and1.input(0),net3])
#printPathT([and1.input(0),net3],net1)
printPathTS([and1.input(0),net3],net1,'AND2')

