from os import listdir, getcwd
from os.path import expanduser, join
from time import time
from graphs import GraphDoc, UnionGraph
from matplotlib.pyplot import show
from networkx import to_numpy_matrix

#TO DO: 1. calculate Node weights from union graph
#TO DO: 2. ADD the weights to inverted index
#TO DO: 3. CREATE the retrieval process (Classes: indexing, retrival->set-based->metrics)
#TO DO:    3.a. Index Class -> import an inv index
#TO DO:    3.b. Query document parsing -> graphs-weights -> apriori -> set based -> metrics

def main():
    # define path
    current_dir = getcwd()
    test_path = "".join([current_dir, "/data/test_docs"])
    print(test_path)

    test_doc_path = "".join([test_path, "/01"])
    doc = GraphDoc(test_doc_path, window=10)
    print(doc.create_adj_matrix_with_window())

    # list files
    filenames = [join(test_path, f) for f in listdir(test_path)]
    graph_documents = []
    for filename in filenames:
        graph_doc = GraphDoc(filename, window=10)
        print(graph_doc.create_graph_from_adjmatrix())
        graph_doc.graph = graph_doc.create_graph_from_adjmatrix()
        graph_doc.draw_graph(graph_doc.graph)
        graph_documents += [graph_doc]

    # takes as input list of graph document objects
    ug = UnionGraph(graph_documents, window=10)
    print(ug.union_graph())
    # ug.save_inverted_index()
    union_graph = ug.union_graph()
    ug.draw_graph(union_graph)
    print(to_numpy_matrix(union_graph))


main()
