from itertools import combinations


def intersection(a, b):
    return list(set(a) & set(b))


def union(a, b):
    return a + list(set(b) - set(a))


def create_candidate_1(query, inv_index):
    one_termsets = []
    for term in query:
        if term in inv_index:
            post_list = inv_index[term]['posting_list']
            doc_ids = [id for id, _ in post_list]
            t = frozenset([term])
            if t not in one_termsets:
                one_termsets.append([t, doc_ids])
        else:
            print('<word "%s" has not required support or it already exists.>' % term)

    return dict(one_termsets)


def create_freq_term(termsets, min_freq):
    freq_ts = {}
    for termset, doc_ids in termsets.items():
        if len(doc_ids) >= min_freq:
            freq_ts[termset] = doc_ids

    return freq_ts


def create_candidate_k(freq_termsets, k):
    """create the list of k-item candidate"""
    ck = {}

    # for generating candidate of size two (2-itemset)
    if k == 0:
        for t1, t2 in combinations(freq_termsets.keys(), 2):
            t1_ids = freq_termsets[t1]
            t2_ids = freq_termsets[t2]

            ck[t1 | t2] = intersection(t1_ids, t2_ids)

    else:
        for t1, t2 in combinations(freq_termsets.keys(), 2):

            # termsets ids
            t1_ids = freq_termsets[t1]
            t2_ids = freq_termsets[t2]

            # if the two (k+1)-item sets has
            # k common elements then they will be
            # unioned to be the (k+2)-item candidate
            # intr = intersection(t1_ids, t2_ids)
            intr = t1 & t2
            if len(intr) == k:
                termset = t1 | t2
                if termset not in ck:
                    ck[termset] = intersection(t1_ids, t2_ids)

    return ck


def apriori(query, inv_index, min_freq):
    # the candidate sets for the 1-item is different,
    # create them independently of others
    c1 = create_candidate_1(query, inv_index)

    # filter the frequenct ones
    freq_termsets = [create_freq_term(c1, min_freq=min_freq)]

    k = 0
    while len(freq_termsets[k]) > 0:
        freq_term = freq_termsets[k]

        # create (k+1)
        ck = create_candidate_k(freq_term, k)

        # filter with respect to minimum frequency
        freq_term = create_freq_term(ck, min_freq=min_freq)

        # append to total
        freq_termsets.append(freq_term)

        # increment round
        k += 1

    # unify freq termsets into one dictionary
    ts = {}
    for item in freq_termsets:
        ts = ts | item
    return ts