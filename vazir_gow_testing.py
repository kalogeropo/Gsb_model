from time import time

import numpy as np
from gowpy.gow.builder import GoWBuilder
from gowpy.feature_extraction.gow import TwidfVectorizer
from os import listdir, getcwd
from os.path import join
from retrieval import cosine_similarity,calc_precision_recall
import pandas as pd
from operator import itemgetter

from utilities import excelwriter

timelist_GoW = []
start = time()

# define path
current_dir = getcwd()
# /collections/CF/docs
# /data/test_docs
test_path = "".join([current_dir, "/collections/CF/docs"])

# list files
filenames = [join(test_path, f) for f in listdir(test_path)]
with open("".join([current_dir, "/collections/CF/Queries.txt"]), "r") as fd:
    queries = [q.upper() for q in fd.readlines()]
# print(queries)
with open("".join([current_dir, "/collections/CF/Relevant.txt"]), "r") as fd:
    relevant = [[int(id) for id in d.split()] for d in fd.readlines()]
# print(relevant)

testing_window = [i for i in range(8,20,2)]
print(testing_window)
for window in testing_window:
    if window == 10: window = 22
    av_pre = []
    av_rec = []
    for query in queries:
    #for query in queries[0:1]:
        text = [query]
        #print(text)
        for file in filenames:
            with open(file, "r") as fd:
                text.append(fd.read())
        # print(text)
        #print(len(text))

        vectorizer_gow = TwidfVectorizer(
            # Graph-of-words specificities
            directed=False,
            window_size=window,
            # Token frequency filtering
            min_df=0.0,
            max_df=1.0,
            # Graph-based term weighting approach
            term_weighting='degree'
        )
        X = vectorizer_gow.fit_transform(text)

        X = X.todense()
        # print(X.sum(axis=1))
        #print(X.shape)
        q = X[0, :]
        #print(q.shape)
        eval_list = []
        for i in range(1,len(X)):
            eval = cosine_similarity(q, X[i,:].transpose())
            #print(eval)
            eval_list.append((i,float(eval)))
        eval_list = sorted(eval_list,key=lambda x: x[1],reverse=True)
        #print(eval_list)
        ordered_docs = [tup[0]for tup in eval_list]
        #print(ordered_docs)
        pre, rec = calc_precision_recall(ordered_docs, relevant[queries.index(query)])

        av_pre.append(pre)
        av_rec.append(rec)
    df = pd.DataFrame(list(av_pre), columns=["A_pre"])
    path = "".join([current_dir, "/results/GoW/"])
    #print(path)
    test_writer = excelwriter(path)
    test_writer.write_results(f"gow{window}u", df)
    #print(df)
    end = time()
    time_dif = end - start
    timelist_GoW.append(int(time_dif))

print(f"time in secs for indexing and retieval of GoW with window size [8,20,2] = {timelist_GoW}")
""""
[ 8,   10,  12,  14,   16,  18  ]
[200, 559, 806, 1080, 1376, 1683]
time in secs for indexing and retieval of GoW with window size [8,20,2] = [200, 559, 806, 1080, 1376, 1683]
"""