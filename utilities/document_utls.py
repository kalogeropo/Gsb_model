from _csv import writer
from os import makedirs
from os.path import exists

import pickle

from networkx import from_numpy_array
from numpy import dot, fill_diagonal, diag, mean
from numpy.linalg import norm
import string

try:
    from rank_bm25 import BM25Okapi
except ModuleNotFoundError:
    from os import system

    system("pip install rank_bm25")
from utilities.Result_handling import write


def adj_to_graph(adj_matrix):
    G = from_numpy_array(adj_matrix)
    # print(G.edges(data=True))
    return G


def nodes_to_terms(terms, maincore):
    k_core = []
    for i in maincore:
        k_core.append(terms[i])
    # print(k_core)
    return k_core


def calc_average_edge_w(adj_matrix):
    return mean(adj_matrix) / 2


def prune_matrix(adj_matrix, threshold):
    diagonal1 = diag(adj_matrix).copy()
    # print(diagonal1)
    if threshold > 1:
        adj_matrix[adj_matrix <= threshold] = 0
        # print(diagonal1)
    fill_diagonal(adj_matrix, diagonal1)
    new_diagonal = adj_matrix.diagonal()
    return adj_matrix


def remove_punctuation(input_string):
    # Make a translator object to replace punctuation with none
    translator = str.maketrans('', '', string.punctuation)
    # Use the translator
    return input_string.translate(translator)


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


def evaluate_bm25_score(q, bm25_vectors):
    doc_sim = {}
    score = bm25_vectors.get_scores(q)
    #print(len(score))
    for id, s in enumerate(score.T, start=1):
        doc_sim[id] = s
    return {id: sim for id, sim in sorted(doc_sim.items(), key=lambda item: item[1], reverse=True)}


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


def calc_precision_recall(doc_sims, relevant, k):
   # print(len(doc_sims))
    cnt = 0
    retrieved = 1
    recall = []
    precision = []
    mrr = 0
    for doc in doc_sims:
        if doc in relevant:
            cnt += 1
            p = cnt / retrieved
            if cnt == 1:
                mrr = p
            r = cnt / len(relevant)
            precision += [p]
            recall += [r]
        retrieved += 1
        if retrieved == k:
            break

    try:
        avg_pre = sum(precision) / len(precision)
    except ZeroDivisionError:
        avg_pre = 0
    try:
        avg_rec = sum(recall) / len(recall)
    except ZeroDivisionError:
        avg_rec = 0
    if avg_rec == 0 or avg_pre == 0:
        print(f"Doc SIM: {doc_sims}\nRel:{relevant}\nret:{retrieved}")
    return avg_pre, avg_rec, mrr


# write list to binary file
def write_list(a_list, name):
    # store list in binary file so 'wb' mode
    with open(name, 'wb') as fp:
        pickle.dump(a_list, fp)
        print('Done writing list into a binary file')


def read_list(name):
    with open(name, 'rb') as f:
        my_list = pickle.load(f)
        return my_list


# transform json index to old index (input json index, output index.dat [id,term,wout,[plist]])
def graphToIndex(id, terms, calc_term_w, plist, *args, **kwargs):
    filename = kwargs.get('filename', None)
    if not filename:
        filename = 'inverted index.dat'
    f = open(filename, "a+")
    data = ','.join(
        [str(i) for i in plist])  # join list to a string so we can write it in the inv index and load it with ease
    f.write('%s;%s;%s;%s;\n' % (id, terms, calc_term_w, data))
    f.close()
    return 1


def json_to_dat(collection, filename=None):
    print(filename)
    index = collection.inverted_index
    print(len(index.keys()))
    for key in index.keys():
        id = index[key]['id']
        terms = index[key]['term']
        plist = index[key]['posting_list']
        if 'nwk' in index[key].keys():
            nwk = index[key]['nwk']
        else:
            print("NWK has not been calculated!!!!!!! is it intended?")
            nwk = 0
        graphToIndex(id, nwk, terms, plist, filename=filename)

def write_to_tsv(data:list[str] ,filename: str|None =None):
    """
    Appends a single row of data to a TSV file.

    Args:
        data: List of strings to write as a row.
        filename: Path to the file. Must be a valid file path.
    """
    if filename is None:
        raise ValueError("filename must be provided")
    with open(filename, 'a', newline='') as f_output:
        tsv_output = writer(f_output, delimiter='\t')
        tsv_output.writerow(data)