class graph:
    
    """Graph ADT"""    
    def __init__(self):
        self.graph={}
        self.visited={}
            
    def append(self,vertexid,edge,weight):        
        """add/update new vertex,edge,weight"""        
        if vertexid not in self.graph.keys():      
            self.graph[vertexid]={}
            self.visited[vertexid]=0
        if edge not in self.graph.keys():      
            self.graph[edge]={}
            self.visited[edge]=0
        self.graph[vertexid][edge]=weight
        
    def reveal(self):
        """return adjacent list"""
        return self.graph
    
    def vertex(self):
        """return all vertices in the graph"""
        return list(self.graph.keys())
    
    def edge(self,vertexid):
        """return edge of a particular vertex"""
        return list(self.graph[vertexid].keys())
    
    def edge_reverse(self,vertexid):
        """return vertices directing to a particular vertex"""                
        return [i for i in self.graph if vertexid in self.graph[i]]
    
    def weight(self,vertexid,edge):
        """return weight of a particular vertex"""
        return (self.graph[vertexid][edge])
    
    def order(self):
        """return number of vertices"""
        return len(self.graph)
    
    def visit(self,vertexid):
        """visit a particular vertex"""
        self.visited[vertexid]=1
        
    def go(self,vertexid):
        """return the status of a particular vertex"""
        return self.visited[vertexid]
    
    def route(self):
        """return which vertices have been visited"""
        return self.visited
    
    def degree(self,vertexid):
        """return degree of a particular vertex"""
        return len(self.graph[vertexid])
    
    def mat(self):
        """return adjacent matrix"""        
        self.matrix=[[0 for _ in range(max(self.graph.keys())+1)] for i in range(max(self.graph.keys())+1)]        
        for i in self.graph:    
            for j in self.graph[i].keys():    
                self.matrix[i][j]=1        
        return self.matrix
    
    def remove(self,vertexid):  
        """remove a particular vertex and its underlying edges"""
        for i in self.graph[vertexid].keys():
            self.graph[i].pop(vertexid)
        self.graph.pop(vertexid)
        
    def disconnect(self,vertexid,edge):
        """remove a particular edge"""
        del self.graph[vertexid][edge]
    
    def clear(self,vertexid=None,whole=False):
        """unvisit a particular vertex"""
        if whole:
            self.visited=dict(zip(self.graph.keys(),[0 for i in range(len(self.graph))]))
        elif vertexid:
            self.visited[vertexid]=0
        else:
            assert False,"arguments must satisfy whole=True or vertexid=int number"


def bron_kerbosch(ADT,R=set(),P=set(),X=set()):
    """Bron Kerbosch algorithm to find maximal cliques
        P stands for priority queue, where pending vertices are
        R stands for result set, X stands for checked list
        To find maximal cliques, only P is required to be filled
        P=set(ADT.vertex())"""

    #when we have nothing left in the priority queue and checked list
    #we find a maximal clique
    if not P and not X:
        yield R
        
    #while we still got vertices in priority queue
    #we pick a random adjacent vertex and add into the clique
    while P:
        
        v=P.pop()
        
        yield from bron_kerbosch(ADT,
                                 
                                 # add a new adjacent vertex into the result set
                                 #trying to expand the clique to the maximal
                                 R=R.union([v]),
                                 
                                 #the priority queue is bounded by the rule of adjacency
                                 #a vertex can be added into the priority queue
                                 #if and only if it is neighbor to everyone in the current clique
                                 P=P.intersection(ADT.edge(v)),
                                 
                                 #the checked list is bounded by the rule of adjacency as well
                                 X=X.intersection(ADT.edge(v)))
        
        #the vertex has been checked
        X.add(v)


def bron_kerbosch_pivot(ADT,R=set(),P=set(),X=set()):
    """Bron Kerbosch algorithm with pivoting to find maximal cliques
        P stands for priority queue, where pending vertices are
        R stands for result set, X stands for checked list
        To find maximal cliques, only P is required to be filled
        P=set(ADT.vertex())"""

    if not P and not X:
        yield R
    
    #choose a pivot vertex u from the union of pending and processed vertices
    #delay the neighbors of pivot vertex from being added to the clique to reduce recursive calls
    try:
        u=list(P.union(X)).pop()
        N=P.difference(ADT.edge(u))
    
    
    #if the neighbors of pivot u are equivalent to priority queue
    #in that case we just roll back to the function without pivoting
    except IndexError:
        N=P
    
    for v in N:
        
        yield from bron_kerbosch_pivot(ADT,
                                       R=R.union([v]),
                                       P=P.intersection(ADT.edge(v)),
                                       X=X.intersection(ADT.edge(v)))
        P.remove(v)
        X.add(v)

ADT = graph()
ADT.append(1, 2, 1)
ADT.append(1, 4, 1)
ADT.append(1, 5, 1)
ADT.append(1, 6, 1)

ADT.append(2, 1, 1)
ADT.append(2, 4, 1)
ADT.append(2, 5, 1)
ADT.append(2, 6, 1)

ADT.append(3, 5, 1)

ADT.append(4, 1, 1)
ADT.append(4, 2, 1)

ADT.append(5, 1, 1)
ADT.append(5, 2, 1)
ADT.append(5, 3, 1)
ADT.append(5, 6, 1)

ADT.append(6, 1, 1)
ADT.append(6, 2, 1)
ADT.append(6, 5, 1)


ADT.reveal()

print(list(bron_kerbosch_pivot(ADT,P=set(ADT.vertex()))))