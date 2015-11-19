# -*- coding: utf-8 -*-

class Graph:
    def __init__(self, nVert):
        self.nVert = nVert
        self._adj = [[] for _ in range(nVert)]
        self.edges = []

    def addEdge(self, edge):
        self._adj[edge.src].append(edge.dst)
        self.edges.append(edge)

class Edge:
    def __init__(self, src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight