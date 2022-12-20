from os import listdir, getcwd
from os.path import join
from time import time
from pandas import DataFrame

from apriori import apriori
from collection import Collection
from graphs import GraphDoc
from retrieval import *
from utilities import excelwriter
from parse import Parser
from networkx import to_numpy_array, to_numpy_matrix


def main():

    # create Collection Object by defining the path
    collection = Collection(path='collections\\baeza', model='GSB', window=0, graph_docs=[]).load_collection()
    print(collection.inv_index)
    print(collection.graph)
    # print(collection.union_graph())
    # print(collection.inverted_index())
    # collection.save_inverted_index()
    # collection.save_graph_index()
    # print(collection.get_adj_matrix())

    # print(f'\nCreation of Union Graph took {time() - graph_start} secs')
    # collection.save_graph_index()
    # collection.save_inverted_index()
    # un_gr = Collection().load_graph()
    # print(un_gr)

    """
    inv_index = collection.create_inverted_index()
    print(inv_index)
    # col = Collection().load_collection()
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
        # tnw = calculate_tnw(freq_termsets, inv_index)
        # print(tnw, '\n')

        doc_weights = calculate_doc_weights(tf_ij, idf, tnw=1)
        print(doc_weights)
        print('\n')
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
    # df = DataFrame(list(zip(avg_pre, avg_rec)), columns=["A_pre", "A_rec"])
    # test_writer = excelwriter()
    # stest_writer.write_results('', df)


# TODO: testing framework, logging result handling
# TODO: fix set based calculation weights and test it with the summing one
# TODO: implement vazirgiannis window and ranking (github: gowpy)

"""

main()
