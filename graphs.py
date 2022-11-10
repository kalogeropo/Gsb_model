from networkx import Graph, draw, disjoint_union_all, from_numpy_array, to_numpy_matrix
from document import Document
from numpy import array, transpose, dot, diagonal, fill_diagonal
from matplotlib.pyplot import show
from json import dumps

class GraphDoc(Document):
    def __init__(self, path):
        super().__init__(path)
        self.adj_matrix = self.create_adj_matrix() 
        self.graph = None

                                                                              
    ################################################################################################
    # For more info see LEMMA 1 and LEMMA 2 of P: A graph based extension for the Set-Based Model, A: Doukas-Makris
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
                        adj_matrix[i][j] = rows[i] * (rows[i] + 1) * 0.5 # Win
            
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

    
    def draw_graph(self, graph=None):
        if self.graph is None:
            self.graph = graph
    
            labels = {n: self.graph[n][n]['weight'] for n in self.graph.nodes}
            colors = [self.graph[n][n]['weight'] for n in self.graph.nodes]
            draw(self.graph, with_labels=True, labels=labels, node_color=colors)
            show()
            return 


class UnionGraph(GraphDoc):
    def __init__(self, graph_docs, path=None):
        super().__init__(path)
        self.graph_docs = graph_docs
        self.inverted_index = {}


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


    def union(self, kcore=[], kcorebool=False):
        # empty union at first
        union_graph = Graph()

        for gd in self.graph_docs:
            adj_matrix = gd.adj_matrix
            terms = list(gd.tf.keys())

            for i in range(adj_matrix.shape[0]):
                h = 0.06 if i in kcore and kcorebool == True else 1
                
                # Win of each node
                w_in = gd.tf[terms[i]] * (gd.tf[terms[i]] + 1) * 0.5 * h
                if not union_graph.has_node(terms[i]):
                    union_graph.add_node(terms[i], weight=w_in)
                    # print(f'Created node {terms[i]} with weight {w_in}')
                # else re-weight
                else:
                    union_graph.nodes[terms[i]]['weight'] += w_in
                    # print(f'Updated node {terms[i]} new weight {union_graph.nodes[terms[i]]}')
                # visit only lower diagonal
                for j in range(adj_matrix.shape[1]):
                    if i > j:
                        if not union_graph.has_edge(terms[i], terms[j]):
                            # assign Wout weight
                            union_graph.add_edge(terms[i], terms[j], weight=adj_matrix[i][j] * h)
                            # print(f'({terms[i], terms[j]}) edge weight: {adj_matrix[i][j] * h}')
                        else:
                            union_graph[terms[i]][terms[j]]['weight'] += adj_matrix[i][j] * h
                            # print(f'({terms[i], terms[j]}) Wout edge weight updated')

        return union_graph

