from matplotlib import pyplot as plt
from networkx import Graph, draw, circular_layout, get_node_attributes, set_node_attributes, get_edge_attributes, draw_networkx_edge_labels
from numpy import array, transpose, dot, fill_diagonal, zeros

from document import Document
from retrieval import calculate_tf


class GraphDoc(Document):
    def __init__(self, path, window=0):
        super().__init__(path)
        self.window = window

        if window > 0: # boolean flag is already taken into consideration to be true
            if isinstance(window, int):
                self.adj_matrix = self.create_adj_matrix_with_window()
            elif isinstance(window, float):
                num_of_words = len(self.tf)
                self.window = int(num_of_words * window) + 1
                self.adj_matrix = self.create_adj_matrix_with_window()
        else:
            self.adj_matrix = self.create_adj_matrix()
            
        self.graph = None


    ##############################################
    ## Creating a complete graph TFi*TFj = Wout ##
    ##############################################
    def create_adj_matrix(self):
        if self.tf is not None:
            # get list of term frequencies
            rows = array(list(self.tf.values()))

            # reshape list to column and row vector
            row = rows.reshape(1, rows.shape[0]).T
            col = rows.reshape(rows.shape[0], 1).T

            # create adjecency matrix by dot product
            adj_matrix = dot(row, col)

            # calculate Win weights (diagonal terms)
            win = [(w * (w + 1) * 0.5) for w in rows]
            fill_diagonal(adj_matrix, win)

            return adj_matrix


    def create_graph_from_adjmatrix(self):

        # check if adj matrix not built yet
        if self.adj_matrix is None:
            self.adj_matrix = self.create_adj_matrix()
    
        graph = Graph()
        terms = list(self.tf.keys())
        w_in = self.adj_matrix.diagonal()

        for i in range(self.adj_matrix.shape[0]):
            graph.add_node(terms[i], weight=w_in[i])
            for j in range(self.adj_matrix.shape[1]):
                if i > j:
                    graph.add_edge(terms[i], terms[j], weight=self.adj_matrix[i][j])

        return graph
        
    
    def create_adj_matrix_with_window(self):
        windows_size = self.window

        # create windowed document
        windowed_doc = self.split_document(windows_size)

        adj_matrix = zeros(shape=(len(self.tf), len(self.tf)), dtype=int)
        for segment in windowed_doc:
            w_tf = calculate_tf(segment)

            for i, term_i in enumerate(self.tf):
                for j, term_j in enumerate(self.tf):
                    if term_i in w_tf.keys() and term_j in w_tf.keys():
                        if i == j:
                            adj_matrix[i][j] += w_tf[term_i] * (w_tf[term_i] + 1) / 2
                        else:
                            adj_matrix[i][j] += w_tf[term_i] * w_tf[term_j]
        return adj_matrix

    
    def calculate_win(self):
        return get_node_attributes(self.graph, 'weight')


    def calculate_wout(self):
        return {node: val for (node, val) in self.graph.degree(weight='weight')}


    def number_of_nbrs(self):
         return {node: val for (node, val) in self.graph.degree()}


    def draw_graph(self, **kwargs):
        graph = self.graph
        options = {
            'node_color': 'yellow',
            'node_size': 50,
            'linewidths': 0,
            'width': 0.1,
            'font_size': 8,
        }
        filename = kwargs.get('filename', None)
        if not filename:
            filename = 'Union graph'
        plt.figure(filename, figsize=(17, 8))
        plt.suptitle(filename)

        pos_nodes = circular_layout(graph)
        draw(graph, pos_nodes, with_labels=True, **options)

        labels = get_edge_attributes(graph, 'weight')
        draw_networkx_edge_labels(graph, pos_nodes, edge_labels=labels)
        plt.show()
        

