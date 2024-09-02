import cProfile
import pstats
from io import StringIO
from os import listdir, path
from os.path import join
from networkx import Graph
from numpy import fill_diagonal, dot, array

from Preprocess.Collection import Collection


def profile_create_or_update_graph_index(instance, filenames=None):
    # Create a profiler object
    pr = cProfile.Profile()

    # Start profiling
    pr.enable()

    # Call the function you want to profile
    instance.create_or_update_graph_index(filenames)

    # Stop profiling
    pr.disable()

    # Create a string stream to hold the profiling results
    s = StringIO()

    # Create a stats object and sort by cumulative time
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')

    # Print the profiling results
    ps.print_stats()

    # Return the profiling results as a string
    return s.getvalue()
def doc_to_matrix(document):
    # get list of term frequencies
    rows = array(list(document.tf.values()))
    # reshape list to column and row vector

    row = rows.reshape(1, rows.shape[0]).T
    col = rows.reshape(rows.shape[0], 1).T
    # create adjecency matrix by dot product
    adj_matrix = dot(row, col)
    # calculate Win weights (diagonal terms)
    win = [(w * (w + 1) * 0.5) for w in rows]
    fill_diagonal(adj_matrix, win)
    return adj_matrix


class onlineGSB(Collection):
    def __init__(self, path, docs=None, name=''):
        super().__init__(path, docs, name)
        self.union_graph = Graph()

    def create_or_update_graph_index(self, filenames=None):
        if filenames is None:
            filenames = [join(self.path, id) for id in listdir(self.path)]
            #print(filenames)
        else:
            pass
            # for file in filenames:
            #     if not path.exists(file):
            #         filenames.remove(file)
        self.add_batch_docs(filenames)
        for doc in self.docs:
            terms = list(doc.tf.keys())
            adj_matrix = doc_to_matrix(doc)
            for i in range(adj_matrix.shape[0]):
                if terms[i] not in self.union_graph.nodes:
                    self.union_graph.add_node(terms[i], posting_list=[[doc.doc_id, doc.tf[terms[i]]]])
                else:
                    self.union_graph.nodes[terms[i]]["posting_list"].append([doc.doc_id, doc.tf[terms[i]]])
                for j in range(adj_matrix.shape[1]):
                    if i >= j:
                        if self.union_graph.has_edge(terms[i], terms[j]):
                            self.union_graph[terms[i]][terms[j]]['weight'] += (adj_matrix[i][j])  # += Wout
                        else:
                            if adj_matrix[i][j] > 0:
                                self.union_graph.add_edge(terms[i], terms[j], weight=adj_matrix[i][j])
        w_in = {n: self.union_graph.get_edge_data(n, n)['weight'] for n in self.union_graph.nodes()}
        return self.union_graph

    def save_graph_index(self):
        pass


