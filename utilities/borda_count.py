class BordaCount:
    def __int__(self, ranking_a, ranking_b, collection):
        self.modelA = ranking_a
        self.modelB = ranking_b
        self.collection = collection
        self._queries = self.collection.queries
        self._relevant = self.collection.relevant

    def fit(self):
        pass
    def evaluate(self):
        pass
