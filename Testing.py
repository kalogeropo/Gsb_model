"""
                                    models- testing
-----------------------------------------------------------------------------
indexing
------->index ----------------------------------------------------------------
    collection path, test name, model,          parametres
1. ****************,---------, index-complete,     NULL
2. ****************,---------, index-percentage,   perc ->float
3. ****************,---------, index-constant,     window-size ->int
4. ****************,---------, index-sliding,      slidning-window-size ->int
5. ****************,---------, index-sent-par,     perc_window, paragraph-size
retrival
--->SET-BASED---------------------------------------------------------------------
    collection path, test name, model,               parametres
6. ****************,---------, set-based_min_tf,       min_support ->>> TODO
7. ****************,---------, set-based_sum_tfs,      min_support
---->Graph-Windowed--------------------------------------------------------------
    collection path, test name, model,           parametres
8. ****************,---------, graph-ext_min_tf,   min_support ->>>>>>TODO
9. ****************,---------, graph-ext_sum_tfs,  min_support
---->OTHER MODELS-------------------------------------------------------------------
    collection path, test name, model,     parametres
10. ****************,---------, GoW-Tw-idf,   NULL
---->MODEL TO ADD IN FUTURE---------------------------------------------------------
    collection path, test name,   model,      parametres
11. ****************,---------, pruned-GSB    edge-perc
12. ****************,---------, k-core-GSB    edge-perc=none, significance h (none to implement windowed,if isnum complete)
13. ****************,---------, Dens-GSB      edge-perc=none, significance h          << >>
14. ****************,---------, embed-on-edge word2vec = true, doc2vec = true
---->Stopword detection----------------------------------------------------------------

"""

from os import listdir, getcwd, path, makedirs
from os.path import join
from time import time

import pandas as pd

from apriori import apriori
from collection import Collection
from graphs import GraphDoc
from retrieval import *


class tester():
    def __init__(self, name, model, params=[], coll_path="/data/docs",rel_path = ""):
        self.rel_path = rel_path
        self.test_name = name
        self.model = model
        self.parametres = params
        self.window_size = 0
        self.perc_size = 0
        current_dir = getcwd()
        self.path = "".join([current_dir, coll_path])
        self.dest_path = "".join([current_dir, "/results/", self.test_name,'/'])
        print(self.dest_path)
        # create dest_folder if not exists for result aggregation
        if not path.exists(self.dest_path):
            makedirs(self.dest_path)

    def start_model(self):
        if self.model == "index-complete":
            self.window_size = 0
            self.collection = self.indexing()
        #we defer the windows size by type (float or int)
        if self.model=="index-percentage" or self.model=="index-constant":
            try:
                self.window_size = int(self.parametres[0])
            except ValueError:
                self.window_size = float(self.parametres[0])
            print(self.window_size)
            self.collection = self.indexing()
            self.create_indexes(True,True)
        print(self.collection.graph)
        # if self.model=="index-sliding":
        # if self.model=="index-sent-par":
        # if self.model=="set-based_min_tf":
        # if self.model=="set-based_sum_tfs":
        # if self.model=="graph-ext_min_tf":
        # if self.model=="graph-ext_sum_tfs":
        # if self.model=="GoW-Tw-idf":

    def create_indexes(self,inverted_index = True, graph_index = False):
        if inverted_index:
            index = self.collection.get_inverted_index()
            self.collection.doc_id = self.test_name
            self.collection.save_inverted_index(self.dest_path)
        if graph_index:
            self.collection.index_graph("".join([self.dest_path," test.json"]))

    def indexing(self):
        filenames = [join(self.path, f) for f in listdir(self.path)]
        graph_documents = []
        graph_start = time()
        for filename in filenames:
            graph_doc = GraphDoc(filename, window=self.window_size)
            graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
            # print(graph_doc.get_win_terms())
            # graph_doc.draw_graph()
            graph_documents += [graph_doc]
        collection = Collection(graph_documents)
        union_graph = collection.union_graph()
        # collection.index_graph("test.json")
        # adj = to_numpy_array(union_graph)
        # adj_diagonal = list(collection.calculate_win().values())
        # fill_diagonal(adj, adj_diagonal)
        # print(adj)
        graph_end = time()
        print(f'Doc to Union Graph took {graph_end - graph_start} secs')
        print('Union Graph Ready.\n')

        return collection
