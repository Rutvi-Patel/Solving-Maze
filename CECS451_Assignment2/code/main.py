from pathlib import Path
import CECS451_Assignment2.code.gameBoard as game
import CECS451_Assignment2.code.AStarSearch as Astar
import CECS451_Assignment2.code.Algorithms as algos
import CECS451_Assignment2.code.Node_Class as Node


data_folder = Path("../data")
maze_file_path = data_folder / "smallMaze.lay"


def main():
    board1 = game.GameBoard(maze_file_path)
    board1.MazeMatrix_Build()

    #Try to run one at a time cause apparently they don't run together


    startNode = Node.Vertex(board1.start)



    endNode = Node.Vertex(board1.Get_GoalNode())
    test1 = algos.Algorithms(board1,startNode,endNode)
    # """
    test1.run_DFS()
    test1.runBFS()
    test1.getBFSPath_result()
    test1.getDFSPath_result()
    # """

    path = Astar.a_star_search(board1, 1, board1.start, board1.goal)
    print(test1.getAStarPath_result(path))

    # saveOutput(board1, maze_file_path)


if __name__ == '__main__':
    main()
