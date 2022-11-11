from os import listdir, getcwd
from os.path import expanduser, join
from time import time
from graphs import GraphDoc, UnionGraph
from matplotlib.pyplot import show
from networkx import to_numpy_matrix, to_numpy_array

#TO DO: 1. calculate Node weights from union graph
#TO DO: 2. ADD the weights to inverted index
#TO DO: 3. CREATE the retrieval process (Classes: indexing, retrival->set-based->metrics)
#TO DO:    3.a. Index Class -> import an inv index
#TO DO:    3.b. Query document parsing -> graphs-weights -> apriori -> set based -> metrics

def main():
    # define path
    current_dir = getcwd()
    test_path = "".join([current_dir, "/data/test_docs"])

    # list files
    filenames = [join(test_path, f) for f in listdir(test_path)]

    graph_documents = []
    for filename in filenames:
        print(filename)
        graph_doc = GraphDoc(filename, window=10)
        print(graph_doc.adj_matrix)
        graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
        print(graph_doc.graph)
        # graph_doc.draw_graph()
        graph_documents += [graph_doc]


    ug = UnionGraph(graph_documents, window=10)

    # takes as input list of graph document ob
    union_graph = ug.union_graph()
    print(union_graph)

    adj = to_numpy_array(union_graph)
    print(adj)
    """
    print(ug.union_graph().degree(weight='weight'))
    print(ug.union_graph().degree())
    wins = []
    i=0
    for nd in list(ug.union_graph().nodes):
       wins.append(tuple((nd, adj[i][i])))
       i+=1
       print(nd)

    print(wins)
    """


main()
