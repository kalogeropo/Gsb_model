from numpy import array, zeros, round, dot
from numpy.linalg import norm
from math import log, log2


def calculate_tf(terms):
    tf = {}
    for term in terms:
        if term not in tf:
            tf[term] = 1
        elif term in tf:
            tf[term] += 1
    return tf


def calculate_ts_idf(termsets, N):
    # len(value) => in how many documents each termset appears
    return array([round(log2(1 + (N / len(value))), 3) for value in termsets.values()])


# termset frequency
def calculate_tsf(termsets, inv_index, N):
    #    d1  d2  d3  . . .  di
    # S1 f11 f12 f13 . . . f1i
    # S2     f22            .
    # S3         f33        .
    # .               .     .
    # .                  .  .
    # Sj fj1 fj2 fj3 . . . fij

    tf_ij = zeros((len(termsets), N))
    # for each termset
    for i, (termset, docs) in enumerate(termsets.items()):
        # e.x. termset = fronzenset{'t1', 't2', 't3'}
        terms = list(termset) # ['t1', 't2', 't3']
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
                    if id in temp: temp[id] += [tf]
                    else: temp[id] = [tf]

        # assign raw termset frequencies
        for id, tfs in temp.items():
            tf_ij[i, id-1] = round((1 + log2(min(tfs))), 3)

    return array(tf_ij)


def calculate_tnw(termsets, inv_index):
    termset_weight = []
    for termset in termsets:
        tnw = 1
        for term in termset:
            if term in inv_index:
                tnw *= inv_index[term]['nwk']
        termset_weight += [round(tnw, 3)]

    return array(termset_weight)


def calculate_doc_weights(tf_ij, idf, tnw=1):
    ########## each column corresponds to a document #########
    return round((tf_ij.T * (idf * tnw)).T, 3)


def cosine_similarity(u, v):
    if (u == 0).all() | (v == 0).all():
        return 0.
    else:
        return dot(u,v) / (norm(u)*norm(v))

def evaluate_sim(query, dtm):
    doc_sim = {}

    for id, doc_vec in enumerate(dtm.T, start=1):
        doc_sim[id] = cosine_similarity(query, doc_vec)

    return {id: sim for id, sim in sorted(doc_sim.items(), key=lambda item: item[1], reverse=True)}
"""

def evaluate_sim(query, dtm, k=50):
    doc_sim = {}

    for id, doc_vec in enumerate(dtm.T):
        doc_sim[id] = cosine_similarity(query, doc_vec)

    return {id: sim for id, sim in sorted(doc_sim.items(), key=lambda item: item[1], reverse=True)}

"""
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

    avg_pre = sum(precision)/len(precision)
    avg_rec = sum(recall)/len(recall)
    return avg_pre, avg_rec


    
