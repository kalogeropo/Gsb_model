from itertools import combinations


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
    

def union(lista, listb):
    return lista + list(set(listb) - set(lista))


def create_candidate_1(query, inv_index):
    one_termsets = []
    for term in query:
        if term in inv_index:
            post_list = inv_index[term]['posting_list']
            doc_ids = [id for id, tf in post_list]
            one_termsets.append([frozenset([term]), doc_ids])
        else:
            print('word %s has not required support or it already exists:' % term)

    return dict(one_termsets)


def create_freq_term(termsets, min_freq):

    pruned_list = {}
    for termset, doc_ids in termsets.items():
        if len(doc_ids) >= min_freq:
            pruned_list[termset] = doc_ids
    return pruned_list


def create_candidate_k(freq_termsets, k):
    """create the list of k-item candidate"""
    ck = {}
    
    # for generating candidate of size two (2-itemset)
    if k == 0:
        for t1, t2 in combinations(freq_termsets.keys(), 2):
            t1_ids = freq_termsets[t1]
            t2_ids = freq_termsets[t2]

            # item = intersection(t1_ids, t2_ids) # union of two sets
            ck[t1 | t2] = intersection(t1_ids, t2_ids)
    else:    
        for t1, t2 in combinations(freq_termsets.keys(), 2):   
            # if the two (k+1)-item sets has
            # k common elements then they will be
            # unioned to be the (k+2)-item candidate
            t1_ids = freq_termsets[t1]
            t2_ids = freq_termsets[t2]
            intr = intersection(t1_ids, t2_ids)
            if len(intr) == k:
                termset = t1 | t2
                if termset not in ck:
                    ck[termset] = intr
    return ck


def apriori(query, inv_index, min_freq):
    # the candidate sets for the 1-item is different,
    # create them independently of others
    c1 = create_candidate_1(query, inv_index)
    # print(f"Initial 1-termsets: {c1}\n")
    freq_termset = create_freq_term(c1, min_freq=min_freq)
    # print(f'Frequent termsets: {freq_termset}\n')
    freq_termsets = [freq_termset]

    k = 0
    while len(freq_termsets[k]) > 0:
        freq_term = freq_termsets[k]
        ck = create_candidate_k(freq_term, k) 
        # print(f"Candidate termsets: {ck}\n")      

        freq_term = create_freq_term(ck, min_freq=min_freq)
        # print(f'Frequent termsets: {freq_term}\n')

        freq_termsets.append(freq_term)
        k += 1
    
    # unify into one dictionary
    ts = {}
    for item in freq_termsets:
        ts = ts | item
    return ts
