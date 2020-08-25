# -------------------------------------------------------------------
#	Converts a standard gameboard to a graph file
#
#	(c) 2020 Diego Aulet-Leon (005466524) & Rutvi Patel (17618768)
#
#	Date: 7/14/2020
#	email: dauletle@gmail.com & prutvi8@gmail.com
#   version: 1.1.0
# ------------------------------------------------------------------
import os

import numpy as np
import time
from pathlib import Path

output_folder = Path("../output/")


class GameBoard(object):
    # Dsize is the length of the data
    # data = array of all the characters
    def __init__(self, maze_file):
        if not os.path.exists(maze_file):
            print("Please create a data folder, and assure that the following file is in the location:\n" + str(
                maze_file))
            exit()

        f = open(maze_file, "r")
        maze_str = f.read()

        self.Fmatrix = 0

        self.goal = 0
        self.goal_x_coordinate = 0
        self.goal_y_coordinate = 0
        self.Dsize = 0
        self.Dsize_x = 0
        self.Dsize_y = 0
        self.data = []
        self.start = 0
        self.start_x_coordinate = 0
        self.start_y_coordinate = 0
        self.width = 0

        for x in range(len(maze_str)):
            if maze_str[x] != "\n":
                self.Dsize += 1
            self.data.append(maze_str[x])
        # print(self.Dsize)

    def GoalNode(self):
            return self.goal+1


    # returns goal node position
    def Get_GoalNode(self):
        if (self.Fmatrix[self.goal][self.goal+1] ==1):
            return self.goal+1
        if (self.Fmatrix[self.goal][self.goal-1] ==1):
            return self.goal -1
        if (self.Fmatrix[self.goal][self.goal-self.width] == 1):
            return self.goal - self.width
        if (self.Fmatrix[self.goal][self.goal + self.width] == 1):
            return self.goal + self.width

        return self.goal + 1

    # returns starting node position
    def StartNode(self):
        return self.start + 1

    def MazeMatrix_Build(self):

        print("\n")
        temp = []
        arr = []

        for x in range(len(self.data)):
            if self.data[x] != "\n":
                temp.append(self.data[x])
            else:
                self.Dsize_x = len(temp)
                arr.append(temp)
                temp = []
        arr.append(temp)
        self.Dsize_y = len(arr)
        # print(arr)

        print("\n")
        self.width = len(arr[1])

        # Code for creating the matrix
        counter = 0
        mat = np.zeros((self.Dsize, self.Dsize), dtype=int)

        # For the y coordinates of the matrix
        for y in range(len(arr)):
            # For the x coordinates of the matrix
            for x in range(len(arr[y])):
                if arr[y][x] != "%":
                    if arr[y][x] == ".":
                        self.goal = counter
                        self.goal_x_coordinate = x
                        self.goal_y_coordinate = y

                        # mat[counter][counter] = 1
                    if arr[y][x] == "P":
                        self.start = counter
                        self.start_x_coordinate = x
                        self.start_y_coordinate = y

                    # Assure that it's not out of bounds
                    if y != len(arr):
                        # If the coordinate below is a space
                        if arr[y + 1][x] == " " or arr[y + 1][x] == ".":
                            mat[counter][((y + 1) * len(arr[y])) + x] = 1
                    # If the coordinate to the left of the space is there, and is a space
                    if x > 0:
                        if arr[y][x - 1] == " " or arr[y][x - 1] == ".":
                            mat[counter][counter - 1] = 1
                    # If the coordinate to the right of the space is there, and is a space
                    if x != len(arr[y]):
                        if arr[y][x + 1] == " " or arr[y][x + 1] == ".":
                            mat[counter][counter + 1] = 1
                    # If the coordinate to above is there, and is a space
                    if y > 0:
                        if arr[y - 1][x] == " " or arr[y - 1][x] == ".":
                            mat[counter][((y - 1) * len(arr[y])) + x] = 1

                counter += 1
        self.Fmatrix = mat
        return mat

    def SaveMatrix(self, path):
        f = open(path, "w")

        Fmatrix = self.MazeMatrix_Build()
        # print(Fmatrix)

        for x in range(self.Dsize):
            for y in range(self.Dsize):
                f.write(str(Fmatrix[x][y]))
                if y < self.Dsize - 1:
                    f.write("\t")
            f.write("\n")

        pass

    def PlotSolution(self, solution, path):
        # Don't worry about it for now, we may use it foe the next assignment
        pass

    def HeuristicAtCurrentNode(self, position):
        x = position % self.Dsize_x
        y = (position - x) // self.Dsize_x
        return abs(x - self.goal_x_coordinate) + abs(y - self.goal_y_coordinate)

    def FindAdjacentPositions(self, current_node):
        tmp = []

        # Check above node
        if current_node > self.Dsize_x:
            node_to_search = self.Fmatrix[current_node][current_node - self.Dsize_x]
            if node_to_search == 1:
                tmp.append(current_node - self.Dsize_x)
        # Check to the left of the node
        if current_node % self.Dsize_x > 0:
            node_to_search = self.Fmatrix[current_node][current_node - 1]
            if node_to_search == 1:
                tmp.append(current_node - 1)
        # Check to the right of the node
        if current_node % self.Dsize_x < self.Dsize_x - 1:
            node_to_search = self.Fmatrix[current_node][current_node + 1]
            if node_to_search == 1:
                tmp.append(current_node + 1)
        # Check below the node
        if current_node + self.Dsize_x < self.Dsize:
            node_to_search = self.Fmatrix[current_node][current_node + self.Dsize_x]
            if node_to_search == 1:
                tmp.append(current_node + self.Dsize_x)

        return tmp

    def FindPathToGoal(self):
        solution = []
        tmp = []
        node_to_search = 0
        search_complete = False

        # Fmatrix = self.MazeMatrix_Build()
        tmp.append(self.start)

        while not search_complete:
            current_node = tmp.pop()

            # Check above node
            if current_node > self.Dsize_x:
                node_to_search = self.Fmatrix[current_node][current_node - self.Dsize_x]
                if node_to_search == 1:
                    tmp.append(current_node - self.Dsize_x)
                    search_complete = True
            # Check to the left of the node
            if current_node % self.Dsize_x > 0:
                node_to_search = self.Fmatrix[current_node][current_node - 1]
                if node_to_search == 1:
                    tmp.append(current_node - 1)
                    search_complete = True
            # Check to the right of the node
            if current_node % self.Dsize_x < self.Dsize_x - 1:
                node_to_search = self.Fmatrix[current_node][current_node + 1]
                if node_to_search == 1:
                    tmp.append(current_node + 1)
                    search_complete = True
            # Check below the node
            if current_node + self.Dsize_x < self.Dsize:
                node_to_search = self.Fmatrix[current_node][current_node + self.Dsize_x]
                if node_to_search == 1:
                    tmp.append(current_node + self.Dsize_x)
                    search_complete = True

            return tmp

        # pass


# ------------------------[End of class Gameboard]----------------------------------------

def saveOutput(board1, input_file):
    time_str = time.strftime("%Y-%m-%d_%H-%M-%S")
    stem = Path(input_file).stem
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    out = str(output_folder) + "\\" + str(stem) + "_" + time_str + ".txt"
    board1.SaveMatrix(out)
    print("Goal node", board1.GoalNode())

    print("Start node", board1.StartNode())
