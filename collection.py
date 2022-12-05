
from graphs import GraphDoc
from matplotlib.pyplot import show
from json import dumps
from math import log 
from networkx import Graph, set_node_attributes, get_node_attributes


class Collection(GraphDoc):
    def __init__(self, graph_docs, window=0, path=''):
        super().__init__(path, window)
        self.graph_docs = graph_docs
        self.inverted_index = {}


    def get_inverted_index(self):

        nwk = self.calculate_nwk()
        id = 0
        for graph_doc in self.graph_docs:
            for key, value in graph_doc.tf.items():
                if key not in self.inverted_index.keys():

                    self.inverted_index[key] = {
                                                'id': id,
                                                'tf': value,
                                                'posting_list': [[graph_doc.doc_id, value]],
                                                'nwk': nwk[key],
                                                'term': key
                                                }
                    id += 1
                else:
                    self.inverted_index[key]['tf'] += value
                    self.inverted_index[key]['posting_list'] += [[graph_doc.doc_id, value]]

        return self.inverted_index


    # creates posting list for each term in collection
    def get_posting_lists(self):
        inverted_index = {}
        for graph_doc in self.graph_docs:
            for key, value in graph_doc.tf.items():
                if key in inverted_index:
                    inverted_index[key] += [[graph_doc.doc_id, value]]
                else:
                    inverted_index[key] = [[graph_doc.doc_id, value]]

        return inverted_index


    def save_inverted_index(self):
            with open(f'inverted_index{self.doc_id}.txt', 'w', encoding='UTF-8') as inv_ind:
                if self.inverted_index:
                    inv_ind.write(dumps(self.inverted_index))
                else: raise("Inverted Index Empty.")


    def union_graph(self, kcore=[], kcore_bool=False):
        union = Graph()
        terms_win = {}
        # for every graph document object
        for gd in self.graph_docs:
            terms = list(gd.tf.keys())
            # iterate through lower triangular matrix
            for i in range(gd.adj_matrix.shape[0]):
                # gain value of importance
                h = 0.06 if terms[i] in kcore and kcore_bool else 1
                for j in range(gd.adj_matrix.shape[1]):
                    if i > j:
                        if union.has_edge(terms[i], terms[j]):
                            union[terms[i]][terms[j]]['weight'] += (gd.adj_matrix[i][j] * h) # += Wout
                        else:
                            union.add_edge(terms[i], terms[j], weight=gd.adj_matrix[i][j] * h)
                    #create a dict of Wins[terms]
                    elif i == j:
                        if terms[i] in terms_win:
                            terms_win[terms[i]] += gd.adj_matrix[i][j] * h # += Win
                        else:
                            terms_win[terms[i]] = gd.adj_matrix[i][j] * h

        set_node_attributes(union, terms_win, 'weight') 

        self.graph = union       

        return union


    def calculate_nwk(self, a=10, b=10):
        nwk = {}
        Win = self.calculate_win()
        Wout = self.calculate_wout()
        ngb = self.number_of_nbrs()
        a, b = a, b

        for k in list(Win.keys()):
            f = a * Wout[k] / ((Win[k] + 1) * (ngb[k] + 1))
            s = b / (ngb[k] + 1)
            nwk[k] = round(log(1 + f) * log(1 + s), 3)
            # print(f'log(1 + ({a} * {Wout[k]} / (({Win[k]} + 1) * ({ngb[k]} + 1)) ) ) * log(1 + ({b} / ({ngb[k]} + 1))) = {nwk[k]}')
        
        return nwk