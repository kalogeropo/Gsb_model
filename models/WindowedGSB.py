from numpy import zeros

from models.GSB import GSBModel
from utilities.document_utls import calculate_tf

from typing import Union

class WindowedGSBModel(GSBModel):
    """
    The windowed version of the Graph-Based Set-Based model.
    Applies a windowed co-occurrence logic (fixed or percentage-based)
    instead of full-document adjacency.

    Args:
        collection: The document collection.
        window: Window size (int for fixed, float ∈ (0, 1) for percentage).
        h_val: Weighting factor for enhanced edges.
        k_core_bool: Enable or disable k-core pruning.
        window_cut_off: Whether to truncate incomplete windows.
    """

    def __init__(self,
                 collection,
                 window: int | float = 8,
                 h_val: int | float = 1,
                 k_core_bool: bool = False,
                 window_cut_off: bool = True):
        self.window = window
        self.window_cut_off = window_cut_off
        super().__init__(collection, k_core_bool=k_core_bool, h_val=h_val)

    def get_model(self):
        return self.__class__.__name__

    def doc_to_matrix(self, document):
        window_size = - 1
        if isinstance(self.window, int):
            window_size = self.window
        elif isinstance(self.window, float):
            window_size = int(self.window * len(document.terms))
        # create windowed document
        windowed_document = document.split_document(window_size, self.window_cut_off)
        adj_matrix = zeros(shape=(len(document.tf), len(document.tf)), dtype=int)
        for segment in windowed_document:
            w_tf = calculate_tf(segment)
            for i, term_i in enumerate(document.tf):
                for j, term_j in enumerate(document.tf):
                    if term_i in w_tf.keys() and term_j in w_tf.keys():
                        if i == j:
                            adj_matrix[i][j] += w_tf[term_i] * (w_tf[term_i] + 1) / 2
                        else:
                            adj_matrix[i][j] += w_tf[term_i] * w_tf[term_j]
        return adj_matrix
