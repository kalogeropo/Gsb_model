import json
from os import listdir, getcwd
from os.path import expanduser, join
from time import time

from graphs import GraphDoc
from collection import Collection
from matplotlib.pyplot import show
from networkx import to_numpy_matrix, to_numpy_array

from numpy import fill_diagonal, dot
from sklearn.metrics.pairwise import cosine_similarity

from apriori import apriori, intersection
from retrieval import *

from networkx.readwrite import json_graph


    
def main():
    # define path
    current_dir = getcwd()
    test_path = "".join([current_dir, "/data/docs"])

    # list files
    filenames = [join(test_path, f) for f in listdir(test_path)]
    graph_documents = []
    for filename in filenames:
        graph_doc = GraphDoc(filename, window=10)

        # graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
        # print(graph_doc.get_win_terms())
        # graph_doc.draw_graph()
        graph_documents += [graph_doc]

    collection = Collection(graph_documents)
    union_graph = collection.union_graph()
    #collection.index_graph("test.json")
    # adj = to_numpy_array(union_graph)
    # adj_diagonal = list(collection.calculate_win().values())
    # fill_diagonal(adj, adj_diagonal)
    # print(adj)
    
    print('Union Graph Ready.\n')

    inv_index = collection.get_inverted_index()

    # queries = [['TERM1', 'TERM2', 'TERM3', 'TERM51']]
    # queries = [['IS', 'CF', 'MUCUS', 'ABNORMAL']]

    # queries = [['a', 'b', 'd', 'n']]
    with open('data/Queries.txt') as f:
        queries = [q.upper().split() for q in f.readlines()]

    with open('data/Relevant.txt') as f:
        relevant_docs = [[int(id) for id in d.split()] for d in f.readlines()]

    N = 1239
    avg_pre = []
    avg_rec = []
    for i, (query, rel_docs) in enumerate(zip(queries, relevant_docs)):
        if i == 20: break
        
        print(f"Query length: {len(query)}")
        apriori_start = time()
        freq_termsets = apriori(query, inv_index, min_freq=1)
        apriori_end = time()
        print(f"Frequent Termsets: {len(freq_termsets)}")
        print(f"Apriori iter {i} took {apriori_end-apriori_start} secs.")

        vector_start = time()
        # bug for the whole collection!!
        idf = calculate_ts_idf(freq_termsets, N)
        # print(idf, '\n')
        tf_ij = calculate_tsf(freq_termsets, inv_index, N)
        # print(tf_ij, '\n')
        tnw = calculate_tnw(freq_termsets, inv_index)
        # print(tnw, '\n')

        doc_weights = calculate_doc_weights(tf_ij, idf, tnw)
        # print(doc_weights)
        # print('\n')
        vector_end = time()
        print(f"Vector Space dimensionality {doc_weights.shape}")
        print(f"Vector iter {i} took {vector_end-vector_start} secs.\n")
        q = idf
        document_similarities = evaluate_sim(q, doc_weights)
        # print(len(document_similarities))

        pre, rec = calc_precision_recall(document_similarities.keys(), rel_docs)
        print(pre, rec)

        avg_pre.append(pre)
        avg_rec.append(rec)


main()