from gowpy.feature_extraction.gow import TwidfVectorizer

from models.Model import Model
from models.ΒΜ25 import dubg
from utilities.document_utls import cosine_similarity, calc_precision_recall
from typing import Optional, Any
from numpy import array, ndarray

class Gow(Model):
    """
    Graph-of-Words based information retrieval model using TwidfVectorizer from gowpy.
    """
    def __init__(self,
                 collection,
                 window: int = 4,
                 isdirected: bool = False,
                 min_dfreq: float = 0.0,
                 max_dfreq: float = 1.0,
                 term_weighting_scheme: str = 'degree'):
        """
        Initialize the GoW model with graph-based term weighting.

        Args:
            collection: Document collection
            window: Context window size for co-occurrence
            isdirected: Whether the graph is directed
            min_dfreq: Minimum document frequency threshold
            max_dfreq: Maximum document frequency threshold
            term_weighting_scheme: Graph centrality metric
        """
        self.vectorizer = TwidfVectorizer(
            directed=isdirected,
            window_size=window,
            min_df=min_dfreq,
            max_df=max_dfreq,
            term_weighting=term_weighting_scheme
        )
        super().__init__(collection)

    def get_model(self):
        return self.__class__.__name__

    def _model_func(self, freq_termsets: Any) -> ndarray:
        raise NotImplementedError("Gow model does not implement _model_func directly.")
    
    def _generate_vectors(self, **kwargs) -> tuple[ndarray, ndarray]:
        text = kwargs.get('Text')
        if not text or not isinstance(text, list):
            raise ValueError("Text must be provided as a list of strings.")
        
        vec = self.vectorizer.fit_transform(text).todense()
        qv = vec[self.collection.num_docs:]
        dv = vec[:self.collection.num_docs]
        return qv, dv

    def _vectorizer(self, tsf_ij: ndarray, idf: ndarray, *args: Any) -> ndarray:     
        raise NotImplementedError("Gow model does not implement __vectorizer directly use generate vectors instead.")

        # text = kwargs.get('Text')
        # print(text[self.collection.num_docs])
        # vec = self.vectorizer.fit_transform(text)
        # vec = vec.todense()
        # # print(len(vec))
        # # print(vec)
        # # print(self.collection.num_docs)
        # qv = vec[self.collection.num_docs:len(vec)]
        # # print(qv[0])
        # dv = vec[0:self.collection.num_docs]
        # # print(dv[-1])
        # print(len(qv))
        # print(len(dv))
        # print(qv[0])
        # return qv, dv
    
    #def fit(self, *args, **kwargs) -> "Gow":
    #    return self.aggregate()
    
    def fit(self,queries: Optional[list[list[str]]], *args, **kwargs) -> "Gow":
        if queries is None:
            if not hasattr(self, '_queries'):
                raise AttributeError("Model instance lacks '_queries' attribute.")
            queries = self._queries
        print(len(self.collection.docs))
        prev_doc = self.collection.docs[0]
        text = [" ".join(prev_doc.terms)]
        for doc in self.collection.docs[1:]:
            # print(doc)
            if doc.doc_id != prev_doc.doc_id + 1:
                text.append(" ")
                print(f"doc id:{doc.doc_id} and prev {prev_doc.doc_id}")
            text.append(" ".join(doc.terms))
            prev_doc = doc
        
        if not isinstance(queries, list) or not all(isinstance(q, list) for q in queries):
            raise ValueError("Expected 'queries' to be a list of lists of strings.")
        for q in queries:
            text.append(" ".join(q))

        self._queryVectors, self._docVectors = self._generate_vectors(Text=text)

        return self

    def evaluate(self, k=None) -> tuple[ndarray, ndarray]:
        for j, q in enumerate(self._queryVectors):
            eval_list = []
            for i in range(0, len(self._docVectors)):
                eval = cosine_similarity(q, self._docVectors[i, :].transpose())
                # print(eval)
                eval_list.append((i, float(eval)))
            eval_list = sorted(eval_list, key=lambda x: x[1], reverse=True)
            # print(eval_list)
            ordered_docs = [tup[0] for tup in eval_list]
            self.ranking.append(ordered_docs)
            if k is None: k = len(ordered_docs)
            # print(f"j:{j}, {len(self.collection.relevant[j])}")
            pre, rec, mrr = calc_precision_recall(ordered_docs, self.collection.relevant[j], k)
            self.precision.append(pre)
            self.recall.append(rec)
        return array(self.precision), array(self.recall)
