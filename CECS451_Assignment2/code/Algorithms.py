# import CECS451_Assignment2.code.gameBoard as game
import CECS451_Assignment2.code.Node_Class as Node


class Algorithms:
    def __init__(self, board, startNode, endNode):
        self.board = board
        self.startNode = startNode
        self.endNode = endNode
        self.allNodes = {}
        self.allNodes[self.startNode.get_id()] = self.startNode
        self.allNodes[self.endNode.get_id()] = self.endNode

        self.bfsPath = []
        self.bfsFringe = 0


        self.dfsPaths = []


    def run_DFS(self):
        # print("Running DFS:\n")
        v = self.startNode
        vLst = self.board.FindPathToGoal()

        list = []
        v.parent = v
        for x in range(len(vLst)):
            list.append(Node.Vertex(vLst[x]))
            self.allNodes[vLst[x]] = list[len(list) - 1]

        for x in range(len(list)):
            y = list.pop(0)
            list.append(y)

            v.adjacent = list
            time = 0
            # print("\n\npath", x + 1)
            self.dfs(self.board, v, time)

            path = []
            xnode = self.endNode
            while (xnode != self.startNode):
                path.append(xnode.get_id())
                xnode = xnode.parent

            # print(path)
            self.dfsPaths.append(path)

            for i in self.allNodes:
                self.allNodes[i].parent = None

    def dfs(self, board, v, time):
        time = time + 1
        v.start = time
        board.start = v.get_id()
        self.create_adjNode(board.FindPathToGoal(), v, 0)
        for u in v.adjacent:
            if (v.get_id() == board.goal + 1):
                # print("Node:", v.get_id(), ", Parent:", v.parent.id, ", Start time:", v.start, "endTime:", v.end)
                pass

            elif (u.parent == None):
                u.parent = v
                # print("Node:", v.get_id(),", Start time:", v.start, "endTime:", v.end)
                self.dfs(board, u, time)
            elif (u.end == None):
                print("Caught in a loop")

    def create_adjNode(self, tmp, u, b):
        if (u == self.startNode):
            pass
        else:
            list = []
            for x in range(len(tmp)):
                if tmp[x] not in self.allNodes:
                    self.allNodes[tmp[x]] = Node.Vertex(tmp[x])
                    list.append(self.allNodes[tmp[x]])
                if tmp[x] in self.allNodes:
                    list.append(self.allNodes[tmp[x]])

            u.adjacent = list

    def runBFS(self):
        # print("\n\nRunning BFS:\n")
        v = self.startNode
        bfspath = []

        self.bfs(self.board, v)

        pnode = self.endNode
        while (pnode != self.startNode):
            bfspath.append(pnode.get_id())
            pnode = pnode.parent

        self.bfsPath = bfspath
        # print(self.bfsPath)

        for i in self.allNodes:
            self.allNodes[i].parent = None

    def bfs(self, board, v):
        v.parent = v
        v.cost = 0
        queue = []
        queue.append(v)
        while (len(queue) != 0):
            u = queue.pop(0)
            self.bfsFringe = self.bfsFringe + 1
            board.start = u.get_id()
            self.create_adjNode(board.FindPathToGoal(), u, 0)

            for x in u.adjacent:
                if (x.parent == None):
                    x.parent = u
                    x.cost = u.cost + 1
                    queue.append(x)

            # print("Node:", u.get_id(), ", parent:", u.parent.get_id(), ", cost:", u.cost)

            if (u.get_id() == board.GoalNode()):
                break

    def getBFSPath_result(self):
        print("BFS Algorithm output:\nFringe:", self.bfsFringe, "\nCost:", len(self.bfsPath),
              "\nPath:", self.bfsPath, )
        print(self.CreatingMaze(self.bfsPath))

    def getDFSPath_result(self):
        print("DFS Algorithm output:\nMultiple Paths")
        # print(self.CreatingMaze(self.dfsPaths[1]))
        if (len(self.dfsPaths)==3):
            h = self.dfsPaths[0]
            if h == self.dfsPaths[1] or h == self.dfsPaths[2]:
                self.dfsPaths.remove(h)

        for x in self.dfsPaths:
            print("Cost:", len(x), "\nPath:", x)
            y = self.CreatingMaze(x)
            print(y, "\n")


    def getAStarPath_result(self, path):
        print("A* Algorithm output:")
        # print("path:", path)
        print(self.CreatingMaze(path))



    def CreatingMaze(self, path):
        data = self.board.data
        width = self.board.width

        for i in data:
            if i == "P":
                print()
            if i == "\n":
                data.remove(i)

        for i in path:
            data[i] = "."

        length = len(data) // width

        # maze code here

        pstr = ""
        for x in range(length):
            for y in range(width):
                pstr = pstr + data[x * width + y]
            pstr = pstr + "\n"

        return pstr
