# -*- coding: utf-8 -*-

from algorithm.graph import Graph, Edge
from algorithm.negativecycle import NegativeCycle
from math import log, exp

class Speculation:
    def __init__(self, model):
        graph = Graph(model.numCurrencies())
        for cur1 in model.currencies():
            for cur2 in model.currencies():
                if cur1 == cur2: continue
                v = model.currencyIndex(cur1)
                w = model.currencyIndex(cur2)
                edge = Edge(v, w, -log(model.getRatio(cur1, cur2)))
                graph.addEdge(edge)
        negcycle = NegativeCycle(graph)
        self.exists = negcycle.exists
        if self.exists:
            self.path = [model.getCurrency(v) for v in negcycle.vertices]
            self.ratio = exp(-sum(e.weight for e in negcycle.edges))
