# -*- coding: utf-8 -*-

class NegativeCycle:
    def __init__(self, graph):
        self._graph = graph
        self._distTo = [float("+inf") for _ in range(graph.nVert)]
        self._distTo[0] = 0
        self._edgeTo = [None for _ in range(graph.nVert)]
        for _ in range(graph.nVert):
            self._relaxAll()
        oldDist = tuple(self._distTo)
        self._relaxAll()
        newDist = tuple(self._distTo)
        if oldDist == newDist:
            self.exists = False
        else:
            self.exists = True
            self.vertices = []
            self.edges = []
            v = [old == new for old, new in zip(oldDist, newDist)].index(False)
            while v not in self.vertices:
                self.vertices.append(v)
                self.edges.append(self._edgeTo[v])
                v = self.edges[-1].src
            self.vertices = self.vertices[self.vertices.index(v):]
            self.edges = self.edges[self.vertices.index(v):]
            self.edges = tuple(reversed(self.edges))
            self.vertices = tuple(reversed(self.vertices))

    def _relaxAll(self):
        for e in self._graph.edges:
            if self._distTo[e.dst] > self._distTo[e.src] + e.weight:
                self._distTo[e.dst] = self._distTo[e.src] + e.weight
                self._edgeTo[e.dst] = e