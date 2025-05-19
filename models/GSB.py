import time
from math import log2

from networkx import Graph, set_node_attributes, get_node_attributes,  k_core, selfloop_edges
from numpy import dot, fill_diagonal, array, zeros, float64, ndarray
from models.Model import Model
from utilities.document_utls import calc_average_edge_w, prune_matrix, adj_to_graph, nodes_to_terms

from typing import Any,Dict


class GSBModel(Model):
    """The GSBModel - Graph Based extension of the SetBased model will be consisted of:
            a. graph - the union graph
            b. _nwk - the term weights derived of each node
            c. as well as any field of its superclass Model
    The main model funct and vectorizer are overriden as we need a different functionality"""

    def __init__(self,
             collection,
             k_core_bool: bool = False,
             h_val: int | float = 1,
             p_val: int | float = 0):
        """
        Initialize the GSBModel with optional k-core pruning and parameter normalization.

        Args:
        collection: The document collection to model.
        k_core_bool (bool): Enable k-core filtering on per-document graphs.
        h_val (int | float): Weight amplification factor (as int or percentage).
        p_val (int | float): Edge weight pruning threshold (as percentage or float).
        """

        self.start_time = time.time()
        self.k_core_bool = k_core_bool
            # Normalize h and p based on type
        self.h = h_val if isinstance(h_val, int) else h_val * 100
        self.p = p_val / 100 if isinstance(p_val, int) else p_val
        super().__init__(collection)

        self.model = self.get_model()
        self.graph: Graph = self.union_graph()
        self._nwk = self._calculate_nwk()
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"model took {self.elapsed_time} secs")


    def _model_func(self, freq_termsets: Any) -> ndarray:
        tns = zeros(len(freq_termsets), dtype=float)
        inverted_index = self.collection.inverted_index
        for i, termset in enumerate(freq_termsets):
            temp = 1
            for term in termset:
                if term in inverted_index:
                    temp *= inverted_index[term]['nwk']
            tns[i] = round(temp, 3)
        return tns


    def _vectorizer(self, tsf_ij: ndarray, idf: ndarray, *args: Any) -> ndarray:
        """
        Applies the model-specific vectorization formula using term weighting (tns).

        Args:
            tsf_ij (np.ndarray): Termset-document frequency matrix.
            idf (np.ndarray): Inverse document frequency vector.
            *args (Any): Expects the first item to be a NumPy array `tns` of term weights.

        Returns:
            np.ndarray: The weighted document-term matrix.
        """
        tns = args[0]  # Unpack explicitly instead of `tns, *_ = args` for clarity
        return tsf_ij * (idf * tns).reshape(-1, 1)
    

    def get_model(self) ->str:
        return self.__class__.__name__

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

    def union_graph(self) ->Graph:
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

    def _calculate_win(self) -> Dict:
        return get_node_attributes(self.graph, 'weight')

    def _calculate_wout(self)  -> Dict[Any, Any]:
        return {node: val for (node, val) in self.graph.degree(weight='weight')} # type: ignore

    def _number_of_nbrs(self) -> Dict:
        return {node: val for (node, val) in self.graph.degree()} # type: ignore

    def kcore_nodes(self, nxgraph, k=None) -> Any:
        nxgraph.remove_edges_from(selfloop_edges(nxgraph))
        try:
            maincore = k_core(nxgraph, k)
        except ValueError:
            maincore = Graph()
            print("k-core decomposition failed")
            print(f"nxgraph: {nxgraph}\n nxgraph.nodes: {nxgraph.nodes}\n nxgraph.edges: {nxgraph.edges}")    
        # print(maincore.nodes)
        return maincore.nodes

    def _calculate_nwk(self, a: float = 1, b: float = 10) -> Dict [str, float]: 
        """
        Calculate node weights (nwk) for terms in the union graph.

        Args:
            a (float): Weighting factor for Wout.
            b (float): Weighting factor for neighbor normalization.

        Returns:
            Dict[str, float]: Mapping of term to nwk score.
        """
        nwk = {}
        Win = self._calculate_win()
        Wout = self._calculate_wout()
        ngb = self._number_of_nbrs()
        for term in list(Win.keys()):
            try:

                f = float64(a * Wout[term] / ((Win[term] + 1) * (ngb[term] + 1)))
                s = float64(b / (ngb[term] + 1))
                score = round(log2(1 + f) * log2(1 + s), 3)
        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error calculating nwk for term '{term}': {e}")
                score = 0
            
            nwk[term] = score
            self.collection.inverted_index[term]['nwk'] = score
        return nwk
    


