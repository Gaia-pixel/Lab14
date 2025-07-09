import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.peso = 0
        self.maxCammino = []
        self.graph = None
        self.idmap = {}

    def get_stores(self):
        return DAO.get_stores()

    def buildGraph(self, store, k):
        self.graph = nx.DiGraph()
        allNodes = DAO.getAllNodes(store)
        self.graph.add_nodes_from(allNodes)
        for n in allNodes:
            self.idmap[n.order_id] = n

        self.getAllArchi2(store, k)


    def getAllArchi1(self, store, k):
        allArchi = DAO.getAllArchi1(store, k)
        for a1, a2, a3 in allArchi:
            self.graph.add_edge(self.idmap[a2], self.idmap[a1], weight = a3)

    def getAllArchi2(self, store, k):
        allOrdini = DAO.getAllArchi2(store)
        for id1, data1, n1 in allOrdini:
            for id2, data2, n2 in allOrdini:
                if 0 < (data2-data1).days < k:
                    self.graph.add_edge(self.idmap[id2], self.idmap[id1], weight = n1+n2)

    def getNodes(self):
        return self.graph.nodes()
    # return self.idmap.values

    def grafoEsiste(self):
        # return self.graph is not None
        if self.graph is not None:
            return True
        return False

    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()


    def getCammino(self, nodo):
        cammino = nx.dfs_tree(self.graph, nodo)  # cammino più lungo
        n = list(cammino.nodes())
        return n

    def getMaxCammino(self, nodo):
        self.ricorsione([nodo])
        return self.maxCammino, self.peso

    def ricorsione(self, parziale):
        if self.pesoCorrente(parziale) > self.peso:
            self.maxCammino = copy.deepcopy(parziale)
            self.peso = self.pesoCorrente(parziale)
        else:
            for n in self.idmap.values():
                if self.condizione(n, parziale):
                    parziale.append(n)
                    self.ricorsione(parziale)
                    parziale.pop()

    def pesoCorrente(self, parziale):
        peso = 0
        for i in range(len(parziale)-1):
            nodo1 = parziale[i]
            nodo2 = parziale[i+1]
            peso += self.graph[nodo1][nodo2]['weight']
        return peso


    def condizione(self, n, parziale):
        if len(parziale) == 1:
            if self.graph.has_edge(parziale[-1], n):
                return True
            else:
                return False

        if n in parziale:
            return False
        nodo1 = parziale[-1]
        nodo2 = parziale[len(parziale)-2]
        ultimoPeso = self.graph[nodo2][nodo1]['weight']
        if self.graph.has_edge(nodo1, n) and self.graph[nodo1][n]['weight'] < ultimoPeso:
            return True
        return False

