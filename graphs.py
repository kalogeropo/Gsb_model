import networkx as nx
from matplotlib import pyplot as plt

from networkx import Graph, draw, disjoint_union_all, from_numpy_array, to_numpy_matrix
from document import Document
from numpy import array, transpose, dot, diagonal, fill_diagonal, zeros
from matplotlib.pyplot import show
from json import dumps


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
            row = transpose(rows.reshape(1, rows.shape[0]))
            col = transpose(rows.reshape(rows.shape[0], 1))

            # create adjecency matrix by dot product
            adj_matrix = dot(row, col)

            # calculate Win weights (diagonal terms)
            for i in range(adj_matrix.shape[0]):
                for j in range(adj_matrix.shape[1]):
                    if i == j:
                        adj_matrix[i][j] = rows[i] * (rows[i] + 1) * 0.5  # Win

            return adj_matrix


    def create_adj_matrix_with_window(self):

        terms = list(self.tf.keys())
        windowed_doc = self.split_document(self.window)
        adj_matrix = zeros(shape=(len(terms), len(terms)))

        for segment in windowed_doc:
            doc = Document(5)
            tf = doc.get_tf(segment)
            for i in range(adj_matrix.shape[0]):
                for j in range(adj_matrix.shape[1]):
                    term_i = terms[i]
                    term_j = terms[j]
                    if term_i in tf.keys() and term_j in tf.keys():
                        if i == j:
                            adj_matrix[i][j] += tf[term_i] * (tf[term_i] + 1)/2
                        else:
                            adj_matrix[i][j] += tf[term_i] * tf[term_j]
        return adj_matrix


    def create_graph_from_adjmatrix(self):

        # check if adj matrix not built yet
        if self.adj_matrix is None:
            self.adj_matrix = self.create_adj_matrix()

        graph = Graph()
        termlist = list(self.tf.keys())
        for i in range(self.adj_matrix.shape[0]):
            graph.add_node(i, term=termlist[i])
            for j in range(self.adj_matrix.shape[1]):
                if i > j:
                    graph.add_edge(i, j, weight=self.adj_matrix[i][j])

        return graph

    def graphToPng(self, *args, **kwargs):
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
        pos_nodes = nx.circular_layout(graph)
        nx.draw(graph, pos_nodes, with_labels=True, **options)
        pos_atrs = {}
        for node, coords in pos_nodes.items():
            pos_atrs[node] = (coords[0], coords[1] + 0.01)

        node_attrs = nx.get_node_attributes(graph, 'term')
        cus_node_att = {}
        for node, attr in node_attrs.items():
            cus_node_att[node] = attr
        nx.draw_networkx_labels(graph, pos_atrs, labels=cus_node_att, font_color='red', font_size=8)

        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos_nodes, edge_labels=labels)
        plt.show()

    def draw_graph(self, graph=None):
        if self.graph is None:
            self.graph = graph
            labels = {n: self.graph[n][n]['weight'] for n in self.graph.nodes}
            colors = [self.graph[n][n]['weight'] for n in self.graph.nodes]
            draw(self.graph, with_labels=True, labels=labels, node_color=colors)
            show()
        else:
            print(self.graph)
            return


class UnionGraph(GraphDoc):
    def __init__(self, graph_docs, window, path=None):
        super().__init__(path, window)
        self.graph_docs = graph_docs
        self.inverted_index = {}


    # creates and updates an inverted_index
    def get_inverted_index(self):
        inverted_index = {}
        for graph_doc in self.graph_docs:
            for key, value in graph_doc.tf.items():
                if key in self.inverted_index:
                    inverted_index[key] += [[graph_doc.doc_id, value]]
                else:
                    inverted_index[key] = [[graph_doc.doc_id, value]]
        return inverted_index


    def create_inverted_index(self):
        self.inverted_index = self.get_inverted_index()


    def save_inverted_index(self):
        with open(f'inverted_index{self.doc_id}.txt', 'w', encoding='UTF-8') as inv_ind:
            if not self.inverted_index:
                self.create_inverted_index()
            inv_ind.write(dumps(self.inverted_index))


    def union_graph(self, kcore=[], kcore_bool=False):
        union = Graph()
        # for every graph document object
        for gd in self.graph_docs:
            terms = list(gd.tf.keys())
            # iterate through lower triangular matrix
            for i in range(gd.adj_matrix.shape[0]):
                # gain value of importance
                h = 0.06 if terms[i] in kcore and kcore_bool else 1
                for j in range(gd.adj_matrix.shape[1]):
                    if i >= j:
                        # 
                        if union.has_edge(terms[i], terms[j]):
                            union[terms[i]][terms[j]]['weight'] += (gd.adj_matrix[i][j] * h)
                        else:
                            union.add_edge(terms[i], terms[j], weight=gd.adj_matrix[i][j] * h)
        return union

    def calculate_Wout(self, node):
        pass
    def calculate_Win(self, node):
        pass
    def number_of_nbrs(self, node):
        pass