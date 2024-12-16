from models.GSB import GSBModel
from networkx import Graph
from typing import Dict, Tuple, Set,List


class DocGraph(GSBModel):

    def __init__(self, collection, k_core_bool=False, h_val=1, p_val=0):
        super().__init__(collection, k_core_bool=k_core_bool, h_val=h_val)
        # Initialize additional attributes or methods here
    
    @staticmethod
    def get_model():
        return __class__.__name__
    
    def create_graph(self) -> Graph:
        """
        Create a graph with text nodes, word nodes, and weighted edges based on term frequencies and importance.

        Args: self
        Returns:
            nx.Graph: The created graph with nodes and edges.
        """
        doc_words = {}  # {doc_id: {word: tf}}
        
        doc_ids,word_docs, word_importance,doc_words = self.collect_info()
        # Create an undirected graph
        G = Graph()

        # Add text nodes
        for doc_id in doc_ids:
            G.add_node(f'text_{doc_id}', type='text')

        # Add word nodes and edges with weights between words and texts

        for word, docs in word_docs.items():
            G.add_node(word, type='word')
            
            for doc_id, tf in docs.items():
                importance = word_importance[word]
                weight = importance * tf
                G.add_edge(word, f'text_{doc_id}', weight=weight)
            
            #doc_words[doc_id] = set()  
            

        # Add edges between text nodes based on shared words with the calculated threshold
        for doc1 in doc_ids:
            for doc2 in doc_ids:
                if doc1 >= doc2:
                    continue
                common_words = set(doc_words[doc1].keys()).intersection(set(doc_words[doc2].keys()))
                if not common_words:
                    continue
                weight = sum((max(word_docs[word][doc2], word_docs[word][doc1]) * word_importance[word]) for word in common_words if word in word_docs)
                if weight > 0:
                    G.add_edge(f'text_{doc1}', f'text_{doc2}', weight=weight)

        # Create the text subgraph
        text_nodes = [node for node in G.nodes if G.nodes[node]['type'] == 'text']
        text_subgraph = G.subgraph(text_nodes).copy()

        return text_subgraph
    def collect_info(self):
        """Parses the collection for information  
        
        Returns:
           doc_ids (Set[int]): Set of document IDs.
            word_docs (Dict[str, Dict[int, int]]): dictionary with words and their document term frequencies.
            word_importance (Dict[str, float]):  dictionary with words and their importance scores.
            doc_words (Dict[int, Dict[str, int]]):  dictionary with document IDs and their words with term frequencies.

        """
        word_docs = {}  # {word: {doc_id: tf}}
        word_importance = {}    # {word: importance}
        doc_words = {}  # {doc_id: {word: tf}}
        doc_ids = set()

        return doc_ids,word_docs, word_importance,doc_words
        
    def fit(self):
        
        pass
    def evaluate(self):
        pass