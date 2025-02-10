import time
from math import log, log2

from networkx import Graph, set_node_attributes, get_node_attributes,  k_core, selfloop_edges
from numpy import dot, fill_diagonal, array, zeros, float64
from Preprocess import Document
from models.Model import Model
from utilities.document_utls import calc_average_edge_w, prune_matrix, adj_to_graph, nodes_to_terms


class GSBModel(Model):
    """The GSBModel - Graph Based extension of the SetBased model will be consisted of:
            a. graph - the union graph
            b. _nwk - the term weights derived of each node
            c. as well as any field of its superclass Model
    The main model funct and vectorizer are overriden as we need a different functionality"""

    def __init__(self, collection, k_core_bool=False, h_val=1, p_val=0):
        self.start_time = time.time()
        self.k_core_bool = k_core_bool
        if isinstance(h_val, int):
            self.h = h_val
        elif isinstance(h_val, float):
            self.h = h_val * 100
        if isinstance(p_val, int):
            self.p = p_val / 100
        elif isinstance(p_val, float):
            self.p = p_val
        super().__init__(collection)
        self.model = self.get_model()
        self.graph = self.union_graph()
        self._nwk = self._calculate_nwk()
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"model took {self.elapsed_time} secs")

    def _model_func(self, freq_termsets):
        tns = zeros(len(freq_termsets), dtype=float)
        inverted_index = self.collection.inverted_index
        for i, termset in enumerate(freq_termsets):
            temp = 1
            for term in termset:
                if term in inverted_index:
                    temp *= inverted_index[term]['nwk']
            tns[i] = round(temp, 3)
        return tns

    def _vectorizer(self, tsf_ij, idf, *args):
        tns, *_ = args
        return tsf_ij * (idf * tns).reshape(-1, 1)

    @staticmethod
    def get_model():
        return __class__.__name__

    def doc_to_matrix(self, document):
        # get list of term frequencies
        rows = array(list(document.tf.values()))
        # reshape list to column and row vector

        row = rows.reshape(1, rows.shape[0]).T
        col = rows.reshape(rows.shape[0], 1).T
        # create adjecency matrix by dot product
        adj_matrix = dot(row, col)
        # calculate Win weights (diagonal terms)
        win = [(w * (w + 1) * 0.5) for w in rows]
        fill_diagonal(adj_matrix, win)
        return adj_matrix

    def union_graph(self):
        union = Graph()
        for doc in self.collection.docs:
            terms = list(doc.tf.keys())
            adj_matrix = self.doc_to_matrix(doc)
            kcore = []
            if self.k_core_bool:
                if self.model == "GSBModel":
                    thres_edge_weight = self.p * calc_average_edge_w(adj_matrix)
                    adj_matrix = prune_matrix(adj_matrix,thres_edge_weight)
                g = adj_to_graph(adj_matrix)
                maincore = self.kcore_nodes(g)
                kcore = nodes_to_terms(terms, maincore)

            # iterate through lower triangular matrix
            for i in range(adj_matrix.shape[0]):
                # gain value of importance
                h = self.h if terms[i] in kcore and self.k_core_bool else 1
                for j in range(adj_matrix.shape[1]):
                    if i >= j:
                        if union.has_edge(terms[i], terms[j]):
                            union[terms[i]][terms[j]]['weight'] += (adj_matrix[i][j] * h)  # += Wout
                        else:
                            if adj_matrix[i][j] > 0:
                                union.add_edge(terms[i], terms[j], weight=adj_matrix[i][j] * h)
        w_in = {n: union.get_edge_data(n, n)['weight'] for n in union.nodes()}
        set_node_attributes(union, w_in, 'weight')
        for n in union.nodes: union.remove_edge(n, n)
        return union

    def _calculate_win(self):
        return get_node_attributes(self.graph, 'weight')

    def _calculate_wout(self):
        return {node: val for (node, val) in self.graph.degree(weight='weight')}

    def _number_of_nbrs(self):
        return {node: val for (node, val) in self.graph.degree()}

    def kcore_nodes(self, nxgraph, k=None):
        nxgraph.remove_edges_from(selfloop_edges(nxgraph))
        try:
            maincore = k_core(nxgraph, k)
        except ValueError:
            maincore = Graph()
            print("k-core decomposition failed")
            print(f"nxgraph: {nxgraph}\n nxgraph.nodes: {nxgraph.nodes}\n nxgraph.edges: {nxgraph.edges}")    
        # print(maincore.nodes)
        return maincore.nodes

    def _calculate_nwk(self, a=1, b=10):
        nwk = {}
        Win = self._calculate_win()
        # print(Win)
        Wout = self._calculate_wout()
        # print(Wout)
        ngb = self._number_of_nbrs()
        # print(ngb)
        for k in list(Win.keys()):
            try:

                f = float64(a * Wout[k] / ((Win[k] + 1) * (ngb[k] + 1)))
                s = float64(b / (ngb[k] + 1))
                self.collection.inverted_index[k]['nwk'] = round(log2(1 + f) * log2(1 + s), 3)
            except ValueError:
                print(f"f = {f}\ns = {s}\n")
                if f<0:
                    print("**************")
                    print(Wout[k])
                    print(Win[k])
                    print(ngb[k])
                    print("**************")
                self.collection.inverted_index[k]['nwk'] = 0
        return nwk
    


