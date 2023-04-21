from gowpy.feature_extraction.gow import TwidfVectorizer

from models.Model import Model


class Gow(Model):
    @staticmethod
    def get_model(self):
        return __class__.__name__

    def _model_func(self, **kwargs):
        pass

    def _vectorizer(self, **kwargs):
        pass

    def __init__(self,collection,window=4,
                 isdirected = False,
                 min_dfreq=0.0,max_dfreq=1.0,
                term_weighting_scheme='degree'):
        self.vectorizer = TwidfVectorizer(
            # Graph-of-words specificities
            directed=isdirected,
            window_size=window,
            # Token frequency filtering
            min_df=min_dfreq,
            max_df=max_dfreq,
            # Graph-based term weighting approach
            term_weighting=term_weighting_scheme
        )
        super().__init__(collection)

    def fit(self, queries=None, min_freq=1):
        text =[]

        #for index_doc in range(self.collection.num_docs):
        #     if self.collection.docs[index_doc].doc_id > index_doc:
        #         text.append([])
        #         print(f"index {index_doc + 1}")
        #     else:
        #         text.append(self.collection.docs[index_doc].terms)
        #         print(f"index {index_doc+1} and docid {self.collection.docs[index_doc].doc_id}")
        # print(len(text))
        # cnt =0
        # pos =0
        # for list in text:
        #     pos+=1
        #     if not list:
        #
        #         print(pos)
        #         cnt+=1
        # print(cnt)
        if queries is None:
            queries = self._queries
            no_of_qs = len(queries)

