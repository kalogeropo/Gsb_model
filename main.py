from os import listdir, getcwd
from os.path import expanduser, join
from time import time

from document import Collection
from graphs import GraphDoc, UnionGraph
from matplotlib.pyplot import show
from networkx import to_numpy_matrix, to_numpy_array
from numpy import fill_diagonal, dot, matmul
from sklearn.metrics.pairwise import cosine_similarity

from apriori import apriori
from retrieval import calculate_idf, calculate_tf_ij, calculate_tnw, calculate_doc_weights

#TO DO: 1. calculate Node weights from union graph
#TO DO: 2. ADD the weights to inverted index
#TO DO: 3. CREATE the retrieval process (Classes: indexing, retrival->set-based->metrics)
#TO DO:    3.a. Index Class -> import an inv index
#TO DO:    3.b. Query document parsing -> graphs-weights -> apriori -> set based -> metrics

    
def main():
    # define path
    current_dir = getcwd()
    test_path = "".join([current_dir, "/data/baeza_docs"])

    # list files
    filenames = [join(test_path, f) for f in listdir(test_path)]
    graph_documents = []
    for filename in filenames:
        graph_doc = GraphDoc(filename, window=0)

        # graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
        # print(graph_doc.get_win_terms())
        # graph_doc.draw_graph()
        graph_documents += [graph_doc]

    ug = UnionGraph(graph_documents)
    union_graph = ug.union_graph()

    # adj = to_numpy_array(ug.graph)s
    # adj_diagonal = list(ug.calculate_win().values())
    # fill_diagonal(adj, adj_diagonal)
    # print(adj)

    print('\n')
    inv_index = ug.get_inverted_index()

    # queries = [['TERM1', 'TERM2', 'TERM3', 'TERM51']]
    # queries = [['IS', 'CF', 'MUCUS', 'ABNORMAL']]
    queries = [['a', 'b', 'd', 'n']]
    for query in queries:
        freq_termsets = apriori(query, inv_index, min_freq=1)

    print(freq_termsets, len(freq_termsets), '\n')

    # bug for the whole collection!!
    N = len(filenames)
    idf = calculate_idf(freq_termsets, N)
    print(idf, '\n')
    tf_ij = calculate_tf_ij(freq_termsets, inv_index, N)
    print(tf_ij, '\n')
    tnw = calculate_tnw(freq_termsets, inv_index)
    print(tnw, '\n')

    doc_weights = calculate_doc_weights(tf_ij, idf, tnw)
    print(doc_weights)
    print('\n')

    q = idf
    print("Cosine similarities:")
    sims = cosine_similarity(doc_weights.T, [q])
    print(sims)

    
main()
