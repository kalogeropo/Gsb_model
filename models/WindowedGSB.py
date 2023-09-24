from numpy import zeros

from models.GSB import GSBModel
from utilities.document_utls import calculate_tf


class WindowedGSBModel(GSBModel):
    """The windowed version of the graph based extension of the set based model
    Here will be implemented both the constant or percentage version by overriding
    the init function. The rest of the model is the same as the simple graph based
     extension which is the super class of the model."""

    def __init__(self, collection, window=8,k_core_bool =False):
        self.window = window
        super().__init__(collection,k_core_bool)

    def get_model(self):
        return __class__.__name__

    def doc_to_matrix(self, document):
        window_size = - 1
        if isinstance(self.window, int):
            window_size = self.window
        elif isinstance(self.window, float):
            window_size = int(self.window * len(document.terms))
        # create windowed document
        windowed_document = document.split_document(window_size)
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
