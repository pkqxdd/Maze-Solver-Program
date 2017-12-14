# -*- coding:utf8 -*-

from AbstractBaseClasses import BaseNode, BaseEdge
import math, warnings


class Node(BaseNode):
    map_occupy = {}  # A dict that stores coverage area of a node. This is used for fast overlap testing. Trading space for time
    map_origin = {}  # A reversed dict of Node.registry
    registry = {}  # override registry in BaseNode so they are two different dict

    def __init__(self, x, y):
        super().__init__(x, y)
        self.undiscovered_edges = set()  # stores the angle of undiscovered edges

        # Add this node to the map
        self.__class__.map_occupy[(x, y)] = self.index
        self.__class__.map_origin[(x, y)] = self.index
        for i in range(0, self.radius):
            for j in range(0, self.radius):
                self.__class__.map_occupy[(self.x + i, self.y + j)] = self.index
                self.__class__.map_occupy[(self.x - i, self.y + j)] = self.index
                self.__class__.map_occupy[(self.x + i, self.y - j)] = self.index
                self.__class__.map_occupy[(self.x - i, self.y - j)] = self.index
    
    @classmethod
    def find_node(cls,*coordinate) -> int:
        """returns the index number of the node at coordinate, -1 if no such node is found"""
        try:
            assert isinstance(coordinate, (tuple, list))
            assert len(coordinate) == 2
            assert isinstance(coordinate[0], int)
            assert isinstance(coordinate[1], int)
        except AssertionError:
            err = TypeError("Coordinate must be a tuple (x,y), where x and y are int")
            err.__suppress_context__ = True
            raise err
        
        try:
            return cls.map_occupy[coordinate]
        except KeyError:
            return -1

    def __repr__(self):
        return "<Node {i} at {coordinate}>".format(i=self.index, coordinate=str((self.x, self.y)))
    
    def add_edge(self, angle, edge: BaseEdge):
        if angle in self.undiscovered_edges:
            self.undiscovered_edges.remove(angle)
        elif angle in self._edges:
            warnings.warn("Blocked: Attempting to overwrite angle " + str(angle) + " of " + str(self))
            return False
        assert -179.9 < angle < 180.1, "Angle " + str(angle) + ' to ' + str(edge)
        self._edges[angle] = edge
        return True

    def connect_to(self, node: BaseNode):
        """
        :param node: an instance of BaseNode
        :return: True if the two nodes are connected, False otherwise
        """
        if not isinstance(node,BaseNode):
            raise TypeError("Node must be an instance of BaseNode")
        if node.index == self.index:
            warnings.warn("Attempting to connect " + str(self) + " with itself")
            return False

        dy = node.y - self.y
        dx = node.x - self.x

        # using int everywhere to avoid float-point error
        distance = math.sqrt(dy ** 2 + dx ** 2)  # pythagorean theorem
        angle = round(math.degrees(math.asin(dy / distance)))  # angle of the edge in degrees for this node
        if angle == 0: angle = round(
            math.degrees(math.acos(dx / distance)))  # sin(0) = sin(180) in degrees, so here I use cos
        
        edge = Edge(round(distance), self, node)

        end0 = self.add_edge(angle, edge)
        end1 = node.add_edge(angle - 180 if angle > 0 else angle + 180, edge)
        if end0 and end1:
            return True
        else:
            # an edge cannot be added because something else is connecting to a node from exactly same direction,
            # which should not happen.
            if end0:
                del self._edges[angle]
            if end1:
                del node._edges[angle - 180 if angle > 0 else angle + 180]
            return False
        
        
class DeadEnd(BaseNode):
    def __init__(self, *coordinate):  # A DeadEnd has only one edge
        super().__init__(*coordinate)
    
    def add_edge(self, angle, edge: BaseEdge):
        if len(self._edges) == 1:
            raise OverflowError("A DeadEnd should have only one edge")
        else:
            self._edges[angle] = edge
    
    def __repr__(self):
        return "<DeadEnd {i} at {coordinate}>".format(i=self.index, coordinate=(self.x, self.y))
    
class Edge(BaseEdge):
    registry = {}
    
    def __init__(self,length,node0,node1):
        super().__init__(length)
        self.nodes.append(node0)
        self.nodes.append(node1)

    def get_other(self, origin: [Node or int]) -> Node:
        """Return the node to which the origin node is connecting"""
        if isinstance(origin, BaseNode):
            index = origin.index
        elif isinstance(origin, int):
            index = origin
        else:
            raise TypeError("Origin must be either an int or a Node")

        if index in self.nodes:
            return self.nodes[1] if index == self.nodes[0] else self.nodes[0]
        else:
            raise ValueError("Node %d is not connected with this edge" % index)

    def __repr__(self):
        return "<Edge of length {length} connecting {node0} to {node1}>".format(length=self.length, node0=repr(self.nodes[0]), node1=(self.nodes[1]))
