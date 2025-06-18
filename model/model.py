import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()  # grafo orientato
        self._idmap = {}

    def get_stores(self):
        return DAO.getAllStores()

    def build_graph(self, store):
        self._graph.clear()

        # aggiungo i nodi
        self._nodes = DAO.get_orders(store)
        for n in self._nodes:
            self._idmap[n.order_id] = n
        self._graph.add_nodes_from(self._nodes)

        # aggiungo gli archi


    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()