from typing import List, Any
import pandas as pd
import numpy as np

from models.Model import Model
from utilities.document_utls import calc_precision_recall



class BordaCount(Model):

    """
    Implements the Borda count voting mechanism to aggregate two ranking lists
    into a single consensus ranking for each query.
    """
    def __init__(self, ranking_a: List[List[Any]], ranking_b: List[List[Any]], collection):
        """
        Args:
            ranking_a: List of document rankings from model A (one per query)
            ranking_b: List of document rankings from model B (one per query)
            collection: The document collection and ground truth
        """
        super().__init__(collection)
        self.modelA = ranking_a
        self.modelB = ranking_b
        self.bordaRanking: List[List[Any]] = []
    
    def fit(self, *args, **kwargs) -> "BordaCount":
        return self.aggregate()

    def aggregate(self) -> "BordaCount":
        """
        Applies Borda count aggregation across all queries using the input rankings.
        Populates `self.bordaRanking` with the consensus result.
        """
        for rank_a, rank_b in zip(self.modelA, self.modelB):
            df = pd.DataFrame(zip(rank_a, rank_b), columns=['Q_model_A', 'Q_model_B'])
            candidate_set = set(df['Q_model_A']).union(df['Q_model_B'])
            num_candidates = len(candidate_set)

            scores = {candidate: 0 for candidate in candidate_set}
            for candidate in scores:
                for col in df.columns:
                    positions = df.index[df[col] == candidate].tolist()
                    for pos in positions:
                        scores[candidate] += num_candidates - pos

            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            self.bordaRanking.append([doc_id for doc_id, _ in sorted_scores])

        return self

    def evaluate(self, k: int = None) -> tuple[np.ndarray, np.ndarray]:
        """
        Evaluates the Borda-ranked lists using precision and recall.

        Args:
            k (int): Top-k cutoff. If None, uses full ranking length.

        Returns:
            Tuple of (precision array, recall array)
        """
        number_of_queries = len(self.bordaRanking)
        for i, (ranked_docs, relevant_docs) in enumerate(zip(self.bordaRanking, self._relevant)):
            k_eval = k if k is not None else len(ranked_docs)
            pre, rec, _ = calc_precision_recall(ranked_docs, relevant_docs, k_eval)
            self.precision.append(round(pre, 8))
            self.recall.append(round(rec, 8))

        return np.array(self.precision), np.array(self.recall)

    def get_model(self) -> str:
        return self.__class__.__name__

    def _model_func(self, freq_termsets: Any) -> np.ndarray:
        raise NotImplementedError("BordaCount does not implement _model_func")

    def _vectorizer(self, tsf_ij: np.ndarray, idf: np.ndarray, *args: Any) -> np.ndarray:
        raise NotImplementedError("BordaCount does not implement _vectorizer")
