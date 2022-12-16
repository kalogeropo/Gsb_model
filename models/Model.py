from abc import ABC, abstractmethod
from math import log2
from time import time

from numpy import array, zeros

from utilities.tools.apriori import apriori


class Model(ABC):
    """The model class is an abstract class contains variables, lists and methods that an ir model commonly uses.
        Abstract methods will be overriden on different models on a subclass level.
        The model will contain:
            a. name -> model name
            b. query_vector -> query_vector
            c. document vectors
            d. precision
            e. recall
            f. collection -> a complete collection of documents and queries that will be evaluated
    """
    """As function naming conventions for the each method we will use the sklearn fit,fit_transform and evaluate, 
    as they are commonly used, and will make code easier to read and understand"""

    def __init__(self, collection):
        # init list and variables
        self._model = "Base Abstract Model"  # protected, model name by class
        self.collection = collection  # collection which will be used by the model

        #
        self._queries = self.collection.queries
        self._relevant = self.collection.relevant
        self._queryVectors = []
        self._docVectors = []
        # metrics
        self.precision = []
        self.recall = []

    # @abstractmethod
    def get_model(self):
        pass
        # return __class__.__name__

    # the base model fit function will implement the set based document Queries representation. can be overriden
    # in any subclass at will.
    def fit(self, queries=None, min_freq=1):
        if queries is None:
            queries = self._queries
        inverted_index = self.collection.inverted_index
        for i, query in enumerate(queries, start=1):
            print(f"\nQuery {i} of {len(queries)}")
            print(f"Query length: {len(query)}")
            apriori_start = time()
            freq_termsets = apriori(query, inverted_index, min_freq)
            apriori_end = time()
            print(f"Frequent Termsets: {len(freq_termsets)}")
            print(f"Apriori iter {i} took {apriori_end - apriori_start} secs.")

            self._queryVectors = self.calculate_ts_idf(freq_termsets)
            self._docVectors = self.calculate_tsf(freq_termsets)
            return self



    def calculate_ts_idf(self, termsets):
        # len(value) => in how many documents each termset appears
        return array([round(log2(1 + (self.collection.num_docs / len(value))), 3) for value in termsets.values()])

    # term set frequency
    def calculate_tsf(self, termsets):
        #    d1  d2  d3  . . .  di
        # S1 f11 f12 f13 . . . f1i
        # S2     f22            .
        # S3         f33        .
        # .               .     .
        # .                  .  .
        # Sj fj1 fj2 fj3 . . . fij
        N = self.collection.num_docs
        inv_index = self.collection.inverted_index
        tf_ij = zeros((len(termsets), N))
        # for each termset
        for i, (termset, docs) in enumerate(termsets.items()):
            # e.x. termset = fronzenset{'t1', 't2', 't3'}
            terms = list(termset)  # ['t1', 't2', 't3']
            temp = {}
            # for each term in the termset
            for term in terms:
                post_list = inv_index[term]['posting_list']
                # for term's id, tf pair
                for id, tf in post_list:
                    # if belongs to the intersection of the termset
                    if id in docs:
                        # create a dict to hold frequencies for each term of termset
                        # by taking the min f, we get the termset frequency
                        if id in temp:
                            temp[id] += [tf]
                        else:
                            temp[id] = [tf]
            # assign raw termset frequencies
            for id, tfs in temp.items():
                tf_ij[i, id - 1] = round((1 + log2(min(tfs))), 3)

        return array(tf_ij)

    def evaluate(self):
        pass
