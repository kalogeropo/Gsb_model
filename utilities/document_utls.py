from os import makedirs
from os.path import exists

from numpy import dot
from numpy.linalg import norm


def calculate_tf(terms):
    tf = {}
    for term in terms:
        if term not in tf:
            tf[term] = 1
        elif term in tf:
            tf[term] += 1
    return tf


def create_dir(path):
    if not exists(path):
        makedirs(path)
        print("Directories Created")


def evaluate_sim(query, dtm):
    doc_sim = {}

    for id, doc_vec in enumerate(dtm.T, start=1):
        doc_sim[id] = cosine_similarity(query, doc_vec)

    return {id: sim for id, sim in sorted(doc_sim.items(), key=lambda item: item[1], reverse=True)}
def cosine_similarity(u, v):
    if (u == 0).all() | (v == 0).all():
        return 0.
    else:
        return dot(u, v) / (norm(u) * norm(v))


def calc_precision_recall(doc_sims, relevant):
    cnt = 0
    retrieved = 1
    recall = []
    precision = []
    for doc in doc_sims:
        if doc in relevant:
            cnt += 1
            p = cnt / retrieved
            r = cnt / len(relevant)
            precision += [p]
            recall += [r]
        retrieved += 1

    avg_pre = sum(precision) / len(precision)
    avg_rec = sum(recall) / len(recall)
    return avg_pre, avg_rec
