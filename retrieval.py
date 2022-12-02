from numpy import array, zeros
from math import log

def calculate_idf(freq_termsets, N):
    # len(value) => in how many documents each termset appears
    return array([log(1 + (N / len(value))) for value in freq_termsets.values()])


def calculate_fij(freq_termsets, inv_index, N):
    #    d1  d2  d3  . . .  di
    # S1 f11 f12 f13 . . . f1i
    # S2     f22            .
    # S3         f33        .
    # .               .     .
    # .                  .  .
    # Sj fj1 fj2 fj3 . . . fij

    f_ij = zeros((len(freq_termsets), N))
    # for each termset
    for i, (termset, docs) in enumerate(freq_termsets.items()):
        # e.x. termset = {'t1', 't2', 't3'}
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
            f_ij[i, id-1] = min(tfs)

    return array(f_ij)


