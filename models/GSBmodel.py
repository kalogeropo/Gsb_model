from math import log

from networkx import Graph, set_node_attributes, get_node_attributes
from numpy import dot, fill_diagonal, array, zeros
from Preprocess import Document
from models.Model import Model


class GSBModel(Model):
    def __init__(self, collection):
        super().__init__(collection)
        self.model = self.get_model()
        self.graph = self.union_graph()
        self._nwk = self._calculate_nwk()

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
        tns, *_=args
        return tsf_ij * (idf*tns).reshape(-1, 1)

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

    def union_graph(self, kcore=[], kcore_bool=False):
        union = Graph()
        for doc in self.collection.docs:
            terms = list(doc.tf.keys())
            adj_matrix = self.doc_to_matrix(doc)
            # iterate through lower triangular matrix
            for i in range(adj_matrix.shape[0]):
                # gain value of importance
                h = 0.06 if terms[i] in kcore and kcore_bool else 1
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

    def _calculate_nwk(self, a=1, b=10):
        nwk = {}
        Win = self._calculate_win()
        # print(Win)
        Wout = self._calculate_wout()
        # print(Wout)
        ngb = self._number_of_nbrs()
        # print(ngb)
        for k in list(Win.keys()):
            f = a * Wout[k] / ((Win[k] + 1) * (ngb[k] + 1))
            s = b / (ngb[k] + 1)
            self.collection.inverted_index[k]['nwk'] = round(log(1 + f) * log(1 + s), 3)

        return nwk
