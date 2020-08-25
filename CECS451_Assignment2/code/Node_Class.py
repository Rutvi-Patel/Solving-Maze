#Rutvi patel
#Student ID: Student
#7/9/2020


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.parent = None
        self.cost = 0
        self.start = 0
        self.end = 0

    def add_neighbor(self, neighbor, weight):
        self.adjacent[neighbor] = weight


    def get_connections(self):
        return self.adjacent.keys()

    def get_weight(self, neighbor):
        if neighbor in self.adjacent.keys():
            return self.adjacent[neighbor]

    def get_id(self):
        return self.id

    def get_adjID(self):
        list = []
        keyys = self.adjacent.keys()
        for x in keyys:
            list.append(x.get_id())
        return list


class Graph:

    def __init__(self):
        self.myDic = {}
        self.edges = []
        self.pnodes = []

    def add_vertex(self, vertex):
        self.myDic[vertex.get_id] = vertex
        self.pnodes.append(vertex)

    def get_vertex(self, node):
        if node in self.pnodes:
            return node

    def add_edge(self, a, b, weight):
        a.add_neighbor(b,weight)
        self.edges.append((a,b,weight))

    def get_vertices(self):
        list = []
        # print(self.pnodes)
        for x in range (len(self.pnodes)):
            list.append(self.pnodes[x].get_id())
        return list

    def graph_summary(self):
        # print (self.pnodes)
        for x in range (len(self.edges)):
            print(self.edges[x][0].get_id(), " to ",self.edges[x][1].get_id(), ": ", self.edges[x][2])
        # for v in range (len(self.pnodes)):
        #     print (self.pnodes[v].get_id())
        #     for x in range ()




#
# def main():
#
#     print("Graph 1 -----------------")
#     graph1 = Graph()
#     a = Vertex("a")
#     b = Vertex("b")
#     c = Vertex("c")
#     d = Vertex("d")
#     s = Vertex("s")
#
#     nodes = [a,b,c,d,s]
#     for x in range (len(nodes)):
#         graph1.add_vertex(nodes[x])
#
#     edge = [(a,c,2),(c,a,3),(a,b,1),(c,d,2),(c,b,9),
#             (s,c,5),(s,a,10),(d,s,7),(d,b,6),
#             (b,d,4)]
#
#     for y in range(len(edge)):
#         graph1.add_edge(edge[y][0], edge[y][1], edge[y][2])
#
#
#     graph1.graph_summary()
#     # print(a.get_adjID())
#     # print(graph1.get_vertex(a))
#     # print(graph1.get_vertices())
#
# main()
