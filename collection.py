import utilities as utl
from networkx.readwrite import json_graph
from json import dumps, load, loads
from os.path import exists, join
from os import makedirs, listdir, getcwd

from graphs import GraphDoc
from math import log
from networkx import Graph, set_node_attributes, get_node_attributes, to_numpy_array, is_empty
from numpy import fill_diagonal

# collection would be either load from path or create from path
# load from path -> col_path
# create from path -> path
# load variable will determine if Collection obj will make indexes from scrath or load them from existing path
# graph_docs will be optional for other uses

class Collection():
    def __init__(self, model, path, window=0, graph_docs=[]):
        
        # model defines the way on how the term weights will be calculated
        self.model = model

        # dict object to handle the different filepaths for every collection object
        self.path = {
            'path': join(getcwd(), path),
            'docs_path': join(getcwd(), path, 'docs'),
            'index_path': join(getcwd(), path, 'indexes', model),
            'results_path': join(getcwd(), path, 'results', model),
        }

        # can be used to hold different user given information
        self.params = {}

        # boolean flag to distinguish when to create collection from scratch
        # and when we can simply load from files
        # self.load = load

        # union graph
        self.graph = Graph()

        # inverted index 
        self.inv_index = {}

        # graph document objects
        self.graph_docs = graph_docs
        if not graph_docs: 
            self.graph_docs = self.create_graph_docs(window)

    
    def create_model_directory(self):
        # check if exists else create directories
        for path in self.path.values(): 
            if not exists(path): makedirs(path)


    def create_graph_docs(self, w):
        
        # get path for documents
        path = self.path['docs_path']

        # list files
        filenames = [join(path, f) for f in listdir(path)]

        # list to hold every GraphDoc obj
        graph_documents = []

        # for every document file
        for filename in filenames:
            # create it's graph based structure based on window w
            # and represent it as and adjecency matrix
            graph_doc = GraphDoc(filename, window=w)
            # graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
            # append 
            graph_documents += [graph_doc]

        return graph_documents


    def inverted_index(self):

        nwk = self.calculate_nwk()
        id, cnt = 0, 0

        for graph_doc in self.graph_docs:
            for key, value in graph_doc.tf.items():
                try:
                    if key not in self.inv_index:
                        self.inv_index[key] = {
                            'id': id,
                            'tf': value,
                            'posting_list': [[graph_doc.doc_id, value]],
                            'nwk': nwk[key],
                            'term': key
                        }
                        id += 1
                    else:
                        self.inv_index[key]['tf'] += value
                        self.inv_index[key]['posting_list'] += [[graph_doc.doc_id, value]]
                except:
                    cnt += 1
                    print(f"Keys not found {cnt}")

        return self.inv_index


    def get_inverted_index(self):
        return self.inv_index


    # creates posting list for each term in collection
    def posting_lists(self):
        inverted_index = {}
        for graph_doc in self.graph_docs:
            for key, value in graph_doc.tf.items():
                if key in inverted_index:
                    inverted_index[key] += [[graph_doc.doc_id, value]]
                else:
                    inverted_index[key] = [[graph_doc.doc_id, value]]

        return inverted_index


    def union_graph(self, kcore=[], kcore_bool=False):
        
        if not self.graph_docs: raise 'Empty Graph Documents. Union Cannot Be Created.'

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

        if is_empty(self.graph): 
            self.graph = self.union_graph()

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

    
    def get_adj_matrix(self):
        
        if is_empty(self.graph):
            try:
                self.load_graph()
            except:
                self.graph = self.union_graph()

        adj = to_numpy_array(self.graph)
        adj_diagonal = list(self.calculate_win().values())
        fill_diagonal(adj, adj_diagonal)
        
        return adj


    def save_inverted_index(self, name='inv_index.json'):
        # define indexes path
        path = join(self.path['index_path'], name)

        try: 
            with open(path, 'w', encoding='UTF-8') as inv_ind:
                # create inv ind if not created 
                if not self.inv_index:
                    self.inverted_index()
                # store as JSON
                inv_ind.write(dumps(self.inv_index))

         # if directory does not exist
        except FileNotFoundError:
                # create directory
                self.create_model_directory()
                # call method recursively to complete the job
                self.save_inverted_index()
        finally: # if fails again, reteurn object
            return self


    def save_graph_index(self, name='graph_index.json'):
        
        # check if union is created, otherwise auto-create
        if is_empty(self.graph): self.graph = self.union_graph()

        # define path to store index
        path = join(self.path['index_path'], name)

        # format data to store
        graph_index = json_graph.adjacency_data(self.graph)

        try:
            # store via the help of json dump
            with open(path, "w") as gf:
                gf.write(dumps(graph_index, cls=utl.NpEncoder))
        
        # if directory does not exist
        except FileNotFoundError:
                # create directory 
                self.create_model_directory()

                # call method recursively to complete the job
                self.save_graph_index()
        finally: # if fails again, reteurn object
            return self


    def load_graph(self, name='graph_index.json'):

        # path to find stored graph index
        path = join(self.path['index_path'], name)

        try:
            # open file and read as dict
            with open(path) as gf: js_graph = load(gf)
        
        except FileNotFoundError:
            raise('There is no such file to load collection.')

        self.graph = json_graph.adjacency_graph(js_graph)

        return self.graph


    def load_inverted_index(self, name="inv_index.json"):

        # path to find stored graph index
        path = join(self.path['index_path'], name)

        try:
            # open file and read as dict while reconstructing the data as a dictionary
            with open(path) as f: self.inv_index = load(f)

        except FileNotFoundError:
            raise('There is no such file to load collection.')

        return self.inv_index


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
