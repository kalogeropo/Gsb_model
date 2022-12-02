from os import listdir, getcwd
from os.path import expanduser, join
from time import time

from document import Collection
from graphs import GraphDoc, UnionGraph
from matplotlib.pyplot import show
from networkx import to_numpy_matrix, to_numpy_array
from numpy import fill_diagonal
from itertools import combinations

from apriori import apriori

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
    test = Collection()
    for filename in filenames:
        # print(filename)
        graph_doc = GraphDoc(filename, window=0)
        # for term in graph_doc.tf.keys():
            # print(term)
        #    test.add_to_inv_ind(term, graph_doc.tf[term], [graph_doc.doc_id, graph_doc.tf[term]], 0) # (term, term_freq, posting_list, nwk)
        # print(graph_doc.doc_id)
        #print(graph_doc.adj_matrix)
        graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
        #print(graph_doc.get_win_terms())
        #graph_doc.draw_graph()
        graph_documents += [graph_doc]


    ug = UnionGraph(graph_documents)
    ug.graph = ug.union_graph()
    #print(ug.get_inverted_index())
    #print('\n\n')
    # adj = to_numpy_array(ug.graph)
    # adj_diagonal = list(ug.calculate_win().values())
    # print(adj_diagonal)
    # fill_diagonal(adj, adj_diagonal)
    # print(adj)
    # test = collection()
    # test.add_to_inv_ind("asd",3,["keimeno1",1,"keimeno 2",2],0.00045)
    # test.add_to_inv_ind("asd1",3,["keimeno3",2,"keimeno4",123],0.32215)

    print('\n')
    inv_index = ug.get_inv_index()
    print(inv_index)
    print("")

    queries = [['TERM1', 'TERM2', 'TERM3', 'TERM4', 'TERM51']]
    # queries = [['PSEUDOMONAS', 'AERUGINOSA', 'INFECTION', 'IN']]
    for query in queries:
       freq_termsets = apriori(query, inv_index, min_freq=2)

    print(freq_termsets, '\n')
    final = {}
    for item in freq_termsets:
        final = final | item

    print(final, len(final))




main()
