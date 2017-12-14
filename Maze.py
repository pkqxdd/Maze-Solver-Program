# -*- coding:utf8 -*-
import warnings, math, heapq

from AbstractBaseClasses import BaseNode
from DataStructures import Node, DeadEnd


class NoSolution(Exception): pass

class Maze:
    def __init__(self):
        self.origin = None
        self.exit = None

    @staticmethod  # TODO: also return total distance of the shortest route
    def search_route(node0: BaseNode, node1: Node) -> list:
        """
        :param node0: A BaseNode
        :param node1: A Node, because there is no point to travel to a DeadEnd
        :return: A list of nodes of the optimal path from start to end. Including node0 and node1
        This function uses A* search algorithm to find the optimal path between two nodes
        """
        
        frontier = Frontier()
        frontier.add(SearchNode(node0, node1))
        explored = set()

        while len(frontier):  # while not empty
            node = frontier.pop()  # node is always an instance of SearchNode
            explored.add(node)
            
            if node == node1:  # goal reached
                res = [node.node]  # the node here is a SearchNode object and node.node is the actual Node object
                while node.parent is not None:
                    res.append(node.parent.node)  # trace back to origin
                    node = node.parent
                res.reverse()
                return res
            
            node.expand(goal=node1)
            
            for n in node.children:
                if n not in frontier.union(explored):
                    frontier.add(n)
                elif n in frontier:
                    frontier.remove(n)
                    frontier.add(n)  # I know this looks confusing
                    
                    # the underlying data structure for the frontier is a set, which only compares the hash and equality of two objects
                    # two SearchNodes are compared to be equal if they have the same index, which came from the original Node
                    # the hash value of a SearchNode is also its index. So even if two SearchNodes have completely differently parent and cost,
                    # they are treated to be the same object by the frontier if they have the same index number
                    # So this two lines actually switched the node to a completely different one
        
        raise NoSolution("No possible route found between %s and %s" % (node0, node1))

    def mark_origin(self, o: Node):
        self.origin = o

    def create_origin(self):
        self.origin = self.add_node(0, 0)

    def mark_exit(self, e: Node):
        self.exit = e

    def find_way_out(self):
        return self.search_route(self.origin, self.exit)

    def connect(self, n0: int, n1: int):
        """
        :param n0: index of 0th Node
        :param n1: index of first BaseNode
        :return: return value from n0.connect_to(n1)
        This function is similar to Node.connect_to, but does not require a node instance
        """
    
        return Node.registry[n0].connect_to(BaseNode.registry[n1])

    def add_node(self, x, y, isDeadEnd=False) -> BaseNode:
        "Proxy to create a new node"
        if isDeadEnd:
            return DeadEnd(x, y)
        else:
            return Node(x, y)

    @staticmethod
    def calculate_distance(x0: int, y0: int, x1: int, y1: int) -> int:
        return round(math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2))

    @staticmethod
    def calculate_midpoint(x0: int, y0: int, x1: int, y1: int) -> (int, int):
        return (x0 + x1) // 2, (y0 + y1) // 2


class SearchNode:
    "This is for A* search only because a normal node does not store cost or its parent"
    
    def __init__(self, node: BaseNode, goal: Node, parent=None, cost=0):
        self.x = node.x
        self.y = node.y
        self.node = node
        self.parent = parent  # this may be switched to a weakref for better performance
        self.g = cost
        self.index = node.index
        self.children = set()
        self.h = self.heuristic(node, goal)
    
    @staticmethod
    def heuristic(node0: BaseNode, node1: BaseNode) -> int:
        """This heuristic function is the Euclidean distance between two nodes"""
        return round(math.sqrt((node0.x - node1.x) ** 2 + (node0.y - node1.y) ** 2))
    
    def expand(self, goal: Node):
        for edge in self.node._edges.values():
            self.children.add(SearchNode(edge.get_other(self.index), goal, self, self.g + edge.length))
    
    def __eq__(self, other):
        return self.index == other.index
    
    def __int__(self):
        return self.g + self.h
    
    def __lt__(self, other):
        return int(self) < int(other)
    
    def __gt__(self, other):
        return int(self) > int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __ge__(self, other):
        return int(self) >= int(other)
    
    def __hash__(self):
        return self.index

    def __repr__(self):
        return "<SearchNode %d at (%d,%d)>" % (self.index, self.x, self.y)


class Frontier:
    def __init__(self):
        self.heap = []
        self.members = set()  # Average time for membership test for a set is O(1) but O(n) for a list, which is the whole point of having this class
    
    def add(self, item):
        heapq.heappush(self.heap, item)
        self.members.add(item)
    
    def pop(self):
        item = heapq.heappop(self.heap)
        self.members.remove(item)
        return item
    
    def remove(self, item):
        self.heap.remove(item)
        self.members.remove(item)
    
    def __len__(self):
        return len(self.heap)
    
    def __contains__(self, item):
        return item in self.members
    
    def union(self, other):
        return self.members.union(other)


def testRandomMaze():
    import random
    import matplotlib.pyplot as plt
    import time
    
    start_time = time.time()
    
    maze = Maze()
    plt.plot(0, 0, 'go')
    for i in range(10):
        x = random.randrange(0, 100)
        y = random.randrange(0, 100)
        plt.plot(x, y, 'bo')
        if Node.find_node(x, y) < 0:
            n = Node(x, y)
            r = random.choice(list(n.registry.copy()))
            n.connect_to(r)
            plt.plot([n.x, r.x], [n.y, r.y], 'r-')
            r = random.choice(list(n.registry.copy()))
            n.connect_to(r)
            plt.plot([n.x, r.x], [n.y, r.y], 'r-')
        else:
            print("Node %s already exist at (%d,%d)" % (Node.registry[Node.find_node(x, y)], x, y))
    
    e = random.choice(Node.registry)
    maze.mark_exit(e)
    plt.plot(e.x, e.y, 'rd')
    
    try:
        print(maze.find_way_out())
    except NoSolution:
        print("No solution")
    print("Time spent: " + str(time.time() - start_time))
    plt.show()


def testMaze():
    maze = Maze()
    maze.create_origin()
    n0 = Node(10, 10)
    n1 = Node(10, 20)
    n2 = Node(20, 20)
    n3 = Node(20, 10)
    n4 = Node(25, 15)
    n5 = Node(30, 20)
    maze.origin.connect_to(n0)
    n0.connect_to(n1)
    n0.connect_to(n3)
    n3.connect_to(n4)
    n4.connect_to(n2)
    n1.connect_to(n2)
    n2.connect_to(n5)
    maze.mark_exit(n5)
    print(maze.find_way_out())


if __name__ == "__main__":
    testRandomMaze()
