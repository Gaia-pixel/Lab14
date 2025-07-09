import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.nodoSelezionato = None
        self.storeSelezionato = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStores(self):
        stores = self._model.get_stores()
        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(key = s, data = s, on_click= self.handleStoreSelection))
        self._view.update_page()

    def handleStoreSelection(self, e):
        self.storeSelezionato = e.control.data

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        if self.storeSelezionato is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare uno store"))
            self._view.update_page()
            return
        try:
            k = int(self._view._txtIntK.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserire un numero intero"))
            self._view.update_page()
            return

        self._model.buildGraph(self.storeSelezionato, k)
        self.fillDDNode()
        nodi, archi = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"grafo creato con {nodi} nodi e {archi} archi"))
        self._view.update_page()


    def handleCerca(self, e):
        if self.nodoSelezionato is None and not self._model.grafoEsiste():
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un nodo di partenza"))
            self._view.update_page()
            return
        cammino = self._model.getCammino(self.nodoSelezionato)
        self._view._txt_result.controls.append(ft.Text(f"cammino trovato, di seguito i nodi"))
        for c in cammino:
            self._view._txt_result.controls.append(ft.Text(c))
        self._view.update_page()

    
    def fillDDNode(self):
        self._view._ddNode.options.clear()
        nodi = self._model.getNodes()
        for n in nodi:
            self._view._ddNode.options.append(ft.dropdown.Option(key = n, data = n, on_click= self.handleAggiungiNodi))
        self._view.update_page()
        
    def handleAggiungiNodi(self, e):
        self.nodoSelezionato = e.control.data

    def handleRicorsione(self, e):
        maxPercorso, peso = self._model.getMaxCammino(self.nodoSelezionato)
        self._view._txt_result.controls.append(ft.Text(f"Di seguito il cammino massimo partendo da {self.nodoSelezionato}, che ha peso {peso}"))
        for n in maxPercorso:
            self._view._txt_result.controls.append(ft.Text(n))
        self._view.update_page()
