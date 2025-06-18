import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.storeSelezionato = None

    def read_store (self, e):
        if e.control.value is None:
            self.storeSelezionato = None
        else:
            self.storeSelezionato = e.control.value

        print(self.storeSelezionato)

    def fillDDStore(self):
        stores = self._model.get_stores()
        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(key=s.store_id, text=s.store_id, data=s))
        self._view.update_page()


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()  # cancello ciò che ho stampato con la chiamata precedente
        store = self._view._ddStore.value
        if store == None or store == "":
            self._view.create_alert("Store non selezionato!")
            return

        self._model.build_graph(store)
        numNodi = self._model.getNumNodes()
        numArchi = self._model.getNumEdges()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato correttamente:"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {numNodi}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {numArchi}"))

        self._view.update_page()


    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass
