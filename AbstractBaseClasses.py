#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-

import warnings

class BaseNode:
    """A node is the intersection of two lines, or a dead end"""
    registry = {}
    next_index = 0
    radius = 3  # The radius of a node is actually the tolerance of error in a node's coordinate. The shape of a node is actually a square, not a circle
    
    def __new__(cls, *args, **kwargs):
        """Assign each instance a unique id number"""
        i = BaseNode.next_index
        BaseNode.next_index += 1
        instance = super().__new__(cls)
        instance.__index = i
        BaseNode.registry[i] = instance
        cls.registry[i] = instance
        return instance

    def __init__(self, x, y):
        """
        :param coordinate: a 2-tuple (x,y)
        :param N: An instance of BaseEdge, default to None
        :param S: An instance of BaseEdge, default to None
        :param E: An instance of BaseEdge, default to None
        :param W: An instance of BaseEdge, default to None
        """
        try:
            assert isinstance(x, int)
            assert isinstance(y, int)
        except AssertionError:
            err = TypeError("Coordinate must be a tuple (x,y), where x and y are int")
            err.__suppress_context__ = True
            raise err

        self.x = x
        self.y = y
        self._edges = {}  # edges are stored in format angle:edge

    def add_edge(self, angle, edge):
        raise NotImplemented

    def get_edge(self, angle):
        return self._edges[angle]
    
    @property
    def index(self):
        return self.__index
    
    def __hash__(self):
        """Make nodes hashable so that they can be stored in a hash-table"""
        return self.index
    
    def __repr__(self):
        return "<BaseNode {i} at {coordinate}>".format(i=self.index, coordinate=(self.x, self.y))
    
    def __eq__(self, other):
        if isinstance(other, int):
            return self.index == other
        elif isinstance(other, BaseNode):
            return self.index == other.index
        else:
            raise TypeError("%s cannot be compared with instance of %s" % (other.__class__, self.__class__))


class BaseEdge:
    """An edge is the part that connecting two nodes"""
    
    def __init__(self, length: int):
        self.length = length
        self.nodes = []

    def add_node(self, node: BaseNode):
        if len(self.nodes) > 1:
            raise OverflowError("An edge can only connect nodes. Current parents are %s and %s" % self.nodes)
        elif node in self.nodes:
            raise ValueError("%s is already a node of this edge" % node)
        else:
            self.nodes.append(node)
    
    def __len__(self):return self.length
    
    def __repr__(self):
        return "<BaseEdge with length of "+str(self.length)+">"

