from os import listdir, getcwd
from os.path import join
from time import time
from pandas import DataFrame
from networkx import to_numpy_array
from numpy import fill_diagonal

from apriori import apriori
from collection import Collection
from graphs import GraphDoc
from retrieval import *
from utilities import excelwriter
from parse import Parser


def main():
    # define path
    current_dir = getcwd()
    # test_path = "".join([current_dir, "/data/baeza_docs"])
    test_path = "".join([current_dir, "/collections/CF/docs"])

    # list files
    filenames = [join(test_path, f) for f in listdir(test_path)]
    graph_documents = []
    graph_start = time()
    for filename in filenames:
        graph_doc = GraphDoc(filename, window=0)
    
        # graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
        # print(graph_doc.get_win_terms())
        # graph_doc.draw_graph()
        graph_documents += [graph_doc]
        # print(graph_doc.adj_matrix)
    
    collection = Collection(graph_documents)
    union_graph = collection.union_graph()
    print(union_graph)
    # collection.index_graph("test.json")
    adj = to_numpy_array(union_graph)
    adj_diagonal = list(collection.calculate_win().values())
    fill_diagonal(adj, adj_diagonal)
    # print(adj)
    print(f'\nCreation of Union Graph took {time() - graph_start} secs')

    """
    inv_index = collection.get_inverted_index()
    # col = Collection.load_collection('results/firstest/')
    # print(col.inverted_index)
    # inv_index = col.inverted_index
    queries = [['a', 'b', 'd', 'n']]
    relevant_docs, queries = Parser().load_collection('/CF')
    print(relevant_docs)
    print(queries)

    N = 1239
    avg_pre = []
    avg_rec = []
    for i, (query, rel_docs) in enumerate(zip(queries, relevant_docs)):
        print(f"\nQuery {i} of {len(queries)}")

        # stop @i query
        if i == 10: break

        print(f"Query length: {len(query)}")
        apriori_start = time()
        freq_termsets = apriori(query, inv_index, min_freq=1)
        apriori_end = time()
        print(f"Frequent Termsets: {len(freq_termsets)}")
        print(f"Apriori iter {i} took {apriori_end - apriori_start} secs.")

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
        print(f"Vector iter {i} took {vector_end - vector_start} secs.\n")
        q = idf
        document_similarities = evaluate_sim(q, doc_weights)
        # print(len(document_similarities))

        pre, rec = calc_precision_recall(document_similarities.keys(), rel_docs)
        print(pre, rec)

        avg_pre.append(pre)
        avg_rec.append(rec)
    df = DataFrame(list(zip(avg_pre, avg_rec)), columns=["A_pre", "A_rec"])
    test_writer = excelwriter()
    test_writer.write_results('', df)


# TODO: testing framework, logging result handling
# TODO: fix set based calculation weights and test it with the summing one
# TODO: implement vazirgiannis window and ranking (github: gowpy)
"""
main()
