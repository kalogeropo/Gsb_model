"""
                                    models - testing
-----------------------------------------------------------------------------
indexing
------->index ----------------------------------------------------------------
    collection path, test name, model,          parametres
1. ****************,---------, index-complete,     NULL
2. ****************,---------, index-percentage,   perc ->float
3. ****************,---------, index-constant,     window-size ->int
4. ****************,---------, index-sliding,      slidning-window-size ->int -> TODO
5. ****************,---------, index-sent-par,     perc_window, paragraph-size -> TODO
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
10. ****************,---------, GoW-Tw-idf,   NULL -> TODO
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
from utilities import excelwriter


class tester():
    def __init__(self, name, model, params=[], coll_path="/data/docs", rel=None, quer=None):
        print(coll_path)
        if quer is None:
            quer = []
        if rel is None:
            rel = []
        self.relevant_docs = rel
        self.queries = quer
        self.test_name = name
        self.model = model
        self.parametres = params
        self.window_size = 0
        current_dir = getcwd()
        self.path = coll_path
        #print(self.path)
        self.dest_path = "".join([current_dir, "/results/", self.test_name, '/'])
        #print(self.dest_path)
        # create dest_folder if not exists for result aggregation
        if not path.exists(self.dest_path):
            makedirs(self.dest_path)

    def start_model(self):
        if self.model == "index-complete":
            self.window_size = 0
            self.collection = self.indexing()
        ######INDEXING
        # we defer the windows size by type (float or int)
        if self.model == "index-percentage" or self.model == "index-constant":
            try:
                self.window_size = int(self.parametres[0])
            except ValueError:
                self.window_size = float(self.parametres[0])
            print(self.window_size)
            self.collection = self.indexing()
            print(self.collection.graph)
            self.create_indexes(True, True)

        # if self.model=="index-sliding":
        # if self.model=="index-sent-par":
        #######RETRIVAL
        # if self.model=="set-based_sum_tfs":
        if self.model=="set-based_min_tf":
            self.retrieve_set_based(min_freq=int(self.parametres[0]),graphs=False)
        # if self.model=="graph-ext_sum_tfs":
        if self.model == "graph-ext_min_tf":
            self.retrieve_set_based(min_freq=int(self.parametres[0]),graphs=True)
        # if self.model=="GoW-Tw-idf":

    def create_indexes(self, inverted_index=True, graph_index=False):
        if inverted_index:
            index = self.collection.get_inverted_index()
            self.collection.doc_id = self.test_name
            self.collection.save_inverted_index(self.dest_path)
        if graph_index:
            self.collection.index_graph("".join([self.dest_path, " test.json"]))

    def indexing(self):
        self.path = "".join([self.path, '/docs/'])
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

    def retrieve_set_based(self,min_freq=1,graphs=True):
        path = "".join(["results/", self.test_name, "/"])
        col = Collection.load_collection(path)
        #print(col.inverted_index)
        inv_index = col.inverted_index

        N = 1239
        avg_pre = []
        avg_rec = []
        for i, (query, rel_docs) in enumerate(zip(self.queries, self.relevant_docs)):
            #print(f"\nQuery {i} of {len(self.queries)}")

            # stop @i query
            # if i == 15: break

            #print(f"Query length: {len(query)}")
            apriori_start = time()
            freq_termsets = apriori(query, inv_index, min_freq)
            apriori_end = time()
            #print(f"Frequent Termsets: {len(freq_termsets)}")
            #print(f"Apriori iter {i} took {apriori_end - apriori_start} secs.")

            vector_start = time()
            # bug for the whole collection!!
            idf = calculate_ts_idf(freq_termsets, N)
            # print(idf, '\n')
            tf_ij = calculate_tsf(freq_termsets, inv_index, N)
            # print(tf_ij, '\n')
            if graphs:
                tnw = calculate_tnw(freq_termsets, inv_index)
                # print(tnw, '\n')
                doc_weights = calculate_doc_weights(tf_ij, idf, tnw)
                # print(doc_weights)
                # print('\n')
            else:
                doc_weights = calculate_doc_weights(tf_ij, idf)
            vector_end = time()
            #print(f"Vector Space dimensionality {doc_weights.shape}")
            #print(f"Vector iter {i} took {vector_end - vector_start} secs.\n")
            q = idf
            document_similarities = evaluate_sim(q, doc_weights)
            # print(len(document_similarities))

            pre, rec = calc_precision_recall(document_similarities.keys(), rel_docs)
            #print(pre, rec)

            avg_pre.append(pre)
            avg_rec.append(rec)
        df = pd.DataFrame(list(zip(avg_pre, avg_rec)), columns=["A_pre", "A_rec"])
        test_writer = excelwriter(path)
        test_writer.write_results("".join([self.test_name,"_",self.model]), df)
