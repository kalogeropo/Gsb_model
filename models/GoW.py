from gowpy.feature_extraction.gow import TwidfVectorizer

from models.Model import Model
from utilities.document_utls import cosine_similarity, calc_precision_recall


class Gow(Model):
    @staticmethod
    def get_model(self):
        return __class__.__name__

    def _model_func(self, **kwargs):
        pass

    def _vectorizer(self, **kwargs):
        text = kwargs['Text']
        vec = self.vectorizer.fit_transform(text)
        vec = vec.todense()
        # print(vec)

        qv = vec[self.collection.num_docs - 1:]
        dv = vec[0:self.collection.num_docs - 1]
        # print(len(qv))
        # print(len(dv))
        return qv, dv

    def __init__(self, collection, window=4,
                 isdirected=False,
                 min_dfreq=0.0, max_dfreq=1.0,
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
        if queries is None:
            queries = self._queries
        text = []
        debug_ids = []
        prev_doc = self.collection.docs[0]
        for doc in self.collection.docs:
            # print(doc)
            if doc.doc_id != prev_doc.doc_id + 1:
                text.append("")
                debug_ids.append(prev_doc.doc_id + 1)
                # print(doc.doc_id)
            text.append(" ".join(doc.terms))
            debug_ids.append(doc.doc_id)
            prev_doc = doc
        # print(text[125:130])
        # print(debug_ids[125:130])
        for q in queries:
            text.append(" ".join(q))

        self._queryVectors, self._docVectors = self._vectorizer(Text=text)

        return self

    def evaluate(self):
        for j, q in enumerate(self._queryVectors):
            eval_list = []
            for i in range(0, len(self._docVectors)):
                eval = cosine_similarity(q, self._docVectors[i, :].transpose())
                # print(eval)
                eval_list.append((i, float(eval)))
            eval_list = sorted(eval_list, key=lambda x: x[1], reverse=True)
            #print(eval_list)
            ordered_docs = [tup[0] for tup in eval_list]
            self.ranking.append([ordered_docs])
            pre, rec = calc_precision_recall(ordered_docs, self.collection.relevant[j])
            self.precision.append(pre)
            self.recall.append(rec)
        return self
