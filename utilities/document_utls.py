from os import makedirs
from os.path import exists

import pickle
from numpy import dot
from numpy.linalg import norm
import string
from utilities.ExcelWriter import write
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
    #print(doc_sims)
    #print(relevant)
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
        if retrieved == k+1:
            break
    try:
        avg_pre = sum(precision) / len(precision)
    except ZeroDivisionError:
        avg_pre =0
    try:
        avg_rec = sum(recall) / len(recall)
    except ZeroDivisionError:
        avg_rec = 0
    return avg_pre, avg_rec, mrr


def res_to_excel(result_model, namefile='example.xlsx', dest_path="collections/test/Results", sheetname="test"):
    df = result_model.results_to_df()
    write(xl_namefile=namefile, dest_path=dest_path, sheetname=sheetname, data=df)


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
