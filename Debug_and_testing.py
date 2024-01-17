from networkx import info

from models.GSB import GSBModel
from models.GoW import Gow
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from models.ΒΜ25 import BM25Model
from utilities.Result_handling import res_to_excel, expir_start, write

#CF
path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"

#NPL
# path = 'experiments/collections/NPL/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/NPL'
# dest_path = "experiments/paper_results/NPL_results"
# print(q)
# print(len(testcol.inverted_index))

testcol, q, r = expir_start(path, path_to_write, col_path)
testcol.collection_to_tsv(qrel=True)

#df = testcol.q_r_stats()
#write(xl_namefile='example.xlsx', dest_path="experiments/paper_results", sheetname="cf_queries", data=df)

# N = WindowedGSBModel(testcol,7)
# print(N.get_model())
# N.fit()
# N.evaluate()
# df = M.results_to_df()
#print(len(N.ranking))
#df = N.results_to_df()
#write(xl_namefile='example.xlsx', dest_path="experiments/paper_results", sheetname="cf_supp_1", data=df)

# testbm25 = BM25Model(testcol)
# testbm25.fit()
# testbm25.evaluate()
#print(testbm25.precision)

# testing = Gow(testcol)
# testing.fit()
# testing.evaluate()
# print(len(testing.ranking))
# df = testing.results_to_df()
# write(xl_namefile='example.xlsx', dest_path="experiments/collections/test", sheetname="test2", data=df)

# bord = BordaCount(testbm25.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()
# res_to_excel(bord,"[cf]Bm25_windows7.xlsx",dest_path,sheetname="bm25_win7")

#M
#res_to_excel(M,"testM.xlsx",dest_path,sheetname="test13")
# #N
# res_to_excel(N,"testN.xlsx",dest_path,sheetname="test16")
# #bord
# res_to_excel(bord,"testBord.xlsx",dest_path,sheetname="test13_16")


