import pickle
from os.path import join

from datasets import load_dataset

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.document_utls import res_to_excel, calc_precision_recall

# """Uncomment to load collection  11- 32 and 40"""
# dataset = 'lifestyle'
# datasplit = 'dev'
#
# collection_dataset = load_dataset("colbertv2/lotte_passages", dataset)
#
# collection1 = [x for x in collection_dataset[datasplit + '_collection']]
#
# queries_dataset = load_dataset("colbertv2/lotte", dataset)
# queries = [x['query'] for x in queries_dataset['search_' + datasplit]]
#
# nbits = 2  # encode each dimension with 2 bits
# doc_maxlen = 300  # truncate passages at 300 tokens
#max_id = 5000
# index_name = f'{dataset}.{datasplit}.{nbits}bits'
#
# answer_pids = [x['answers']['answer_pids'] for x in queries_dataset['search_' + datasplit]]
# filtered_queries = [q for q, apids in zip(queries, answer_pids) if any(x < max_id for x in apids)]
#
# print(collection1[0:4])
# print(filtered_queries[0:4])
# print(answer_pids[0:4])
# collection1 = collection1[0:max_id]

path = 'collections/lifestyle_small_fivek/docs'
path_to_write = 'collections/lifestyle_small_fivek/index'
col_path = 'collections/lifestyle_small_fivek/'

testcol = Collection(path, name="test")

#testcol.create_col_from_list(collection1, True, filtered_queries, answer_pids, col_path)

testcol.create_collection()
# print(testcol.inverted_index)
testcol.save_inverted_index(path_to_write)
r, q = testcol.load_collection(col_path)
print(len(r))
print(len(q))
print(testcol.num_docs)
print(len(testcol.inverted_index))
#-------------------------------------------------TEST 1
# N = GSBModel(testcol)
# N.fit(min_freq=1)
# N.evaluate(k=256)
# dest_path = "collections/test/Results"
# res_to_excel(N, "GSB_BIG_temp.xlsx", dest_path, sheetname=f"gsb_256")
#
# with open('collections/lifestyle_small_fivek/index/my_list1000.pkl', 'rb') as f:
#     colbert_Rank = pickle.load(f)
# print(len(colbert_Rank))
# for i in colbert_Rank:
#     print(len(i))
#
# pre_list = []
# recall_list = []
# for i, (q, rel, test) in enumerate(zip(testcol.queries, testcol.relevant, colbert_Rank)):
#     # print(q)
#     pre, rec, mrr = calc_precision_recall(test, rel, k=256)
#     pre_list.append(pre)
#     recall_list.append(rec)
# print(pre_list)
#
# bord = BordaCount(colbert_Rank, N.ranking, testcol)
# bord.fit()
# bord.evaluate(k=256)
#
# res_to_excel(bord, "GSB_BIG_temp.xlsx", dest_path, sheetname=f"borda_gsb_col256")
#
# M = WindowedGSBModel(testcol, 10)
# M.fit(min_freq=1)
# M.evaluate(k=256)
#
# res_to_excel(M, "GSB_BIG_temp.xlsx", dest_path, sheetname=f"win10_256")
#
# bord = BordaCount(colbert_Rank, M.ranking, testcol)
# bord.fit()
# bord.evaluate(k=256)
#
# res_to_excel(bord, "GSB_BIG_temp.xlsx", dest_path, sheetname=f"borda_win10_col_256")
 #--------------------------------TEST 2
# for i in range(0,5):
#     N = GSBModel(testcol)
#     N.fit(min_freq=1)
#     N.evaluate(k=256)
#     dest_path = "collections/test/Results"
#     res_to_excel(N, "col_gsb.xlsx", dest_path, sheetname=f"gsb_{i}")
#
#     with open('collections/lifestyle_small_fivek/index/my_list1000.pkl', 'rb') as f:
#         colbert_Rank = pickle.load(f)
#     print(len(colbert_Rank))
#
#     pre_list = []
#     recall_list = []
#     for i, (q, rel, test) in enumerate(zip(testcol.queries, testcol.relevant, colbert_Rank)):
#         # print(q)
#         pre, rec, mrr = calc_precision_recall(test, rel, k=256)
#         pre_list.append(pre)
#         recall_list.append(rec)
#     print(pre_list)
#
#     bord = BordaCount(colbert_Rank, N.ranking, testcol)
#     bord.fit()
#     bord.evaluate(k=256)
#
#     res_to_excel(bord, "col_gsb.xlsx", dest_path, sheetname=f"col_gsb_{i}")

for i in range(8,13):
    N = WindowedGSBModel(testcol,i)
    N.fit(min_freq=1)
    N.evaluate(k=256)
    dest_path = "collections/test/Results"
    res_to_excel(N, "col_windowed.xlsx", dest_path, sheetname=f"Windowed_gsb_{i}")

    with open('collections/lifestyle_small_fivek/index/my_list1000.pkl', 'rb') as f:
        colbert_Rank = pickle.load(f)
    print(len(colbert_Rank))

    pre_list = []
    recall_list = []
    for i, (q, rel, test) in enumerate(zip(testcol.queries, testcol.relevant, colbert_Rank)):
        # print(q)
        pre, rec, mrr = calc_precision_recall(test, rel, k=256)
        pre_list.append(pre)
        recall_list.append(rec)
    print(pre_list)

    bord = BordaCount(colbert_Rank, N.ranking, testcol)
    bord.fit()
    bord.evaluate(k=256)

    res_to_excel(bord, "col_windowed.xlsx", dest_path, sheetname=f"col_win_{i}")