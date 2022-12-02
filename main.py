from os import listdir, getcwd
from os.path import expanduser, join
from time import time

from document import Collection
from graphs import GraphDoc, UnionGraph
from matplotlib.pyplot import show
from networkx import to_numpy_matrix, to_numpy_array
from numpy import fill_diagonal

from apriori import apriori
from retrieval import calculate_idf, calculate_fij

#TO DO: 1. calculate Node weights from union graph
#TO DO: 2. ADD the weights to inverted index
#TO DO: 3. CREATE the retrieval process (Classes: indexing, retrival->set-based->metrics)
#TO DO:    3.a. Index Class -> import an inv index
#TO DO:    3.b. Query document parsing -> graphs-weights -> apriori -> set based -> metrics

    
def main():
    # define path
    current_dir = getcwd()
    test_path = "".join([current_dir, "\\data\\test_docs"])

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

    queries = [['TERM1', 'TERM2', 'TERM3', 'TERM20']]
    # queries = [['PSEUDOMONAS', 'AERUGINOSA', 'INFECTION', 'IN']]
    for query in queries:
        freq_termsets = apriori(query, inv_index, min_freq=2)

    print(freq_termsets, '\n')
    print(len(freq_termsets), '\n')
    N = len(filenames)
    idf = calculate_idf(freq_termsets, N)
    tf_ij = calculate_fij(freq_termsets, inv_index, N)
    print(idf)
    print(tf_ij)
    


main()
