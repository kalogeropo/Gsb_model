from os import listdir
from os.path import expanduser, join
from time import time
from graphs import GraphDoc, UnionGraph, draw
from matplotlib.pyplot import show
from networkx import to_numpy_matrix

def main():

    # define path
    home = expanduser('~')
    path = f'{home}/Desktop/thesis/data/test_docs'
            
    # list files
    filenames = [join(path, f) for f in listdir(path)]

    graph_documents = []
    for filename in filenames:
        graph_doc = GraphDoc(filename)
        graph_documents += [graph_doc]
   
    # takes as input list of graph document objects
    ug = UnionGraph(graph_documents)
    # print(ug.path, ug.tf, ug.doc_id)
    # ug.save_inverted_index()
    union_graph = ug.union_graph()
    # ug.draw_graph(union_graph)
    print(to_numpy_matrix(union_graph))



main()