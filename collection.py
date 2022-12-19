import utilities as utl
from networkx.readwrite import json_graph
from json import dumps, load, loads
from os.path import exists, join
from os import mkdir, listdir, getcwd

from graphs import GraphDoc
from math import log
from networkx import Graph, set_node_attributes, get_node_attributes, to_numpy_array
from numpy import fill_diagonal


class Collection():
    def __init__(self, path, graph_docs=[]):
        # create path
        path = join(getcwd(), path)
        # check if exists else create directory
        if not exists(path): mkdir(path)

        self.path = path
        # TODO: create a params attr to handle all file naming for loading and storing
        self.params = {} 

        self.graph_docs = graph_docs
        self.inverted_index = {}


    def create_inverted_index(self):

        nwk = self.calculate_nwk()
        id, cnt = 0

        for graph_doc in self.graph_docs:
            for key, value in graph_doc.tf.items():
                try:
                    if key not in self.inverted_index:
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
                except:
                    cnt += 1
                    print(f"Keys not found {cnt}")

        return self

    
    def get_inverted_index(self):
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


    def union_graph(self, kcore=[], kcore_bool=False):
        
        self.graph = Graph()
        # for every graph document object
        for gd in self.graph_docs:
            terms = list(gd.tf.keys())
            # iterate through lower triangular matrix
            for i in range(gd.adj_matrix.shape[0]):
                # gain value of importance
                h = 0.06 if terms[i] in kcore and kcore_bool else 1
                for j in range(gd.adj_matrix.shape[1]):
                    if i >= j:
                        if self.graph.has_edge(terms[i], terms[j]):
                            self.graph[terms[i]][terms[j]]['weight'] += (gd.adj_matrix[i][j] * h)
                        else:
                            self.graph.add_edge(terms[i], terms[j], weight=gd.adj_matrix[i][j] * h)

        # in-wards edge weights represent Win
        w_in = {n: self.graph.get_edge_data(n, n)['weight'] for n in self.graph.nodes()}

        # set them as node attr
        set_node_attributes(self.graph, w_in, 'weight')

        # remove in-wards edges
        for n in self.graph.nodes(): self.graph.remove_edge(n, n)

        return self.graph
        
    
    def calculate_win(self):
        return get_node_attributes(self.graph, 'weight')


    def calculate_wout(self):
        return {node: val for (node, val) in self.graph.degree(weight='weight')}


    def number_of_nbrs(self):
         return {node: val for (node, val) in self.graph.degree()}


    def calculate_nwk(self, a=1, b=10):
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


    def save_inverted_index(self, name='inv_index.json'):
        # define indexes path
        path = join(self.path, 'indexes', name)

        try: 
            with open(path, 'w', encoding='UTF-8') as inv_ind:
                # create inv ind if not created 
                if not self.inverted_index:
                    self.create_inverted_index()
                # store as JSON
                inv_ind.write(dumps(self.inverted_index))
        except:
                raise ('Inverted Index failure.')


    def save_graph_index(self, name='graph_index.json'):

        if self.graph is None:
            self.union_graph()
        else:
            # define path to store index
            path = join(self.path, 'indexes', name)

            # format data to store
            graph_index = json_graph.adjacency_data(self.graph)

            # store via the help of json dump
            with open(path, "w") as gf:
                gf.write(dumps(graph_index, cls=utl.NpEncoder))

            return self


    def load_graph(self, name='graph_index.json'):
        # path to find stored graph index
        print(self.path)
        path = join(self.path, 'indexes', name)
        # open file and read as dict
        with open(path) as gf:
            js_graph = load(gf)

        self.graph = json_graph.adjacency_graph(js_graph)

        return self.graph

    
    def get_adj_matrix(self):
        
        if self.graph is None:
            try:
                self.load_graph()
            except:
                self.union_graph()

        adj = to_numpy_array(self.graph)
        adj_diagonal = list(self.calculate_win().values())
        fill_diagonal(adj, adj_diagonal)
        
        return adj


    def load_inverted_index(self, name="inv_index.json"):
        # path to find stored graph index
        path = join(self.path, 'indexes', name)
        # open file and read as dict
        with open(path) as f:
            # reconstructing the data as a dictionary
            self.inverted_index = load(f)

        return self.inverted_index


    @classmethod
    def load_col(cls):
        obj = cls.__new__(cls)
        super(Collection, obj).__init__(path='')

        obj.load_graph()
        obj.load_inverted_index()
        
        return obj


    # Alternative implementation of the above method
    def load_collection(self):

        self.load_graph()
        self.load_inverted_index()
        
        return self
