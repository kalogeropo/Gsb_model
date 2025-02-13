try:
    from rank_bm25 import BM25Okapi
except ModuleNotFoundError:
    from os import system

    system("pip install rank_bm25")

from models.Model import Model
from utilities.document_utls import calc_precision_recall, evaluate_bm25_score


def dubg(a, b):
    cnt = 0
    nq = 0
    for item in a:
        print(item.doc_id)
        if item.terms != b[cnt]:
            nq +=1
            print(F"counter = {cnt} and doc_id = {item.doc_id}")
            cnt+=1
        cnt+=1


class BM25Model(Model):

    @staticmethod
    def get_model(self):
        return __class__.__name__

    def _model_func(self, **kwargs):
        pass

    def _vectorizer(self, **kwargs):
        text = kwargs['Text']
        #print(text)
        bm25 = BM25Okapi(text)
        return bm25

    def __init__(self, collection):
        super().__init__(collection)

    def fit(self, queries=None, min_freq=None):
        if queries is None:
            queries = self._queries

        prev_doc = self.collection.docs[0]
        text = [prev_doc.terms]
        for doc in self.collection.docs[1:]:
            # print(doc)
            # handle missing files with empty text ""
            if doc.doc_id != prev_doc.doc_id + 1:
                text.append("")
                #print(len(text))
                #print(f"doc id:{doc.doc_id} and prev {prev_doc.doc_id}")

            text.append(doc.terms)
            prev_doc = doc

        self._queryVectors = queries
        #dubg(self.collection.docs, text)
        # print(self._queryVectors)
        self._docVectors = self._vectorizer(Text=text)

        return self

    def evaluate(self, k=None):
        # print(len(self._queryVectors))
        # print(self._queryVectors)
        for j, q in enumerate(self._queryVectors):
            document_similarities = evaluate_bm25_score(q, self._docVectors)
            #print(len(document_similarities.keys()))
            self.ranking.append(list(document_similarities.keys()))
            if k is None: k = len(list(document_similarities.keys()))
            print(k)
            # print(f"j:{j}, {len(self.collection.relevant[j])}")
            pre, rec, mrr = calc_precision_recall(document_similarities.keys(), self.collection.relevant[j], k)
            self.precision.append(pre)
            self.recall.append(rec)
            # if j > 0: break
        return self
