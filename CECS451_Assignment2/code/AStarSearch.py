import numpy as np


class Node:
    """
        A node class for A* Pathfinding
        parent is parent of the current Node
        position is current position of the Node in the maze
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# This function return the path of the search
def return_path(current_node, board):
    path = []
    no_rows = board.Dsize_x
    no_columns = board.Dsize_y
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    return path[::-1]


def a_star_search(board, cost, start, end):
    """
        Returns a list of positions as a path from the given start to the given end in the given maze
    """

    # Create start and end node with initized values for g, h and f
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both yet_to_visit and visited list
    # in this list we will put all node that are yet_to_visit for exploration.
    # From here we will find the lowest cost node to expand next
    queue = []
    # in this list we will put all node those already explored so that we don't explore it again
    visited = []

    # Add the start node
    queue.append(start_node)

    # Adding a stop condition. This is to avoid any infinite loop and stop
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = board.Dsize

    """
        1) We first get the current node by comparing all f cost and selecting the lowest cost node for further expansion
        2) Check max iteration reached or not . Set a message and stop execution
        3) Remove the selected node from yet_to_visit list and add this node to visited list
        4) Perofmr Goal test and return the path else perform below steps
        5) For selected node find out all children (use move to find children)
            a) get the current postion for the selected node (this becomes parent node for the children)
            b) check if a valid position exist (boundary will make few nodes invalid)
            c) if any node is a wall then ignore that
            d) add to valid children node list for the selected parent

            For all the children node
                a) if child in visited list then ignore it and try next node
                b) calculate child node g, h and f values
                c) if child in yet_to_visit list then ignore it
                d) else move the child to yet_to_visit list
    """

    # Loop until you find the end
    while len(queue) > 0:

        # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
        outer_iterations += 1

        # Get the current node
        current_node = queue[0]

        current_index = 0
        for index, item in enumerate(queue):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        x = current_node.position % board.Dsize_x
        y = (current_node.position - x) // board.Dsize_x
        print("position: ", current_node.position, ", position-x: ", x, ", position-y: ", y, ", f: ", current_node.f)

        # if we hit this point return the path such as it may be no solution or
        # computation cost is too high
        if outer_iterations > max_iterations:
            print("giving up on pathfinding too many iterations")
            return return_path(current_node, board)

        # Pop current node out off yet_to_visit list, add to visited list
        queue.pop(current_index)
        visited.append(current_node)

        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            return return_path(current_node, board)

        # Generate children from all adjacent squares
        children = []

        tmp = board.FindAdjacentPositions(current_node.position)
        for node_position in tmp:
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through children
        for child in children:
            can_append = True

            # Child is on the visited list (search entire visited list)
            for visited_child in visited:
                if child == visited_child:
                    can_append = False
                    break
                if not can_append:
                    break
            if not can_append:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost

            # Heuristic costs calculated here, this is using eucledian distance
            child.h = board.HeuristicAtCurrentNode(child.position)

            child.f = child.g + child.h

            for open_node in queue:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the yet_to_visit list
            # if not child in queue:
            queue.append(child)
