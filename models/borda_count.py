import pandas as pd

from models.Model import Model
from utilities.document_utls import calc_precision_recall


class BordaCount(Model):
    def __init__(self, ranking_a, ranking_b, collection):
        super().__init__(collection)
        self.modelA = ranking_a
        self.modelB = ranking_b
        self.bordaRanking = []

    def fit(self):
        # zip rankings in order to create a df
        for item in zip(self.modelA, self.modelB):
            # print(len(item))
            # print(f"item0 {item[0]} \n \n kai  item1 {item[1]}" )
            # df = pd.DataFrame(list(zip(Q52_GSB, Q52_set)), columns=['Q52_gsb', 'Q52_set'])

            df = pd.DataFrame(list(zip(item[0], item[1])), columns=['Q_model_A', 'Q_model_B'])
            # print(df)
            candidate_set = set()
            for id, colum in enumerate(df.columns):
                for candidate_doc in df[colum]:
                    # print(candidate_doc)
                    candidate_set.add(candidate_doc)
            num_of_candidates = len(candidate_set)
            # print(candidate_set)
            scores = dict([(can, 0) for can in candidate_set])
            # print(scores)
            for candidate in scores.keys():
                # print(candidate)
                for i, col in enumerate(df.columns):
                    # print(candidate)
                    points = df.loc[df[col] == candidate].index.values
                    for item in points:
                        scores[candidate] += num_of_candidates - item

            scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
            # print(scores)
            self.bordaRanking.append(list(scores.keys()))

    def evaluate(self):
        # print(self.bordaRanking)
        number_of_queries = len(self.bordaRanking)
        for i, (bordarank, rel) in enumerate(zip(self.bordaRanking, self._relevant)):
            pre, rec = calc_precision_recall(bordarank, rel)
            # print(pre, rec)
            #print(f"=> Query {i + 1}/{number_of_queries}, precision = {pre:.3f}, recall = {rec:.3f}")
            self.precision.append(round(pre, 3))
            self.recall.append(round(rec, 3))
        return 0

    def get_model(self):
        return __class__.__name__

    def _model_func(self, freq_termsets):
        pass

    def _vectorizer(self, tsf_ij, idf, *args):
        pass
