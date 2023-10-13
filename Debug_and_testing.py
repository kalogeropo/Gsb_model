from networkx import info

from models.GoW import Gow
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.Result_handling import res_to_excel, expir_start, write

# CF
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

M = WindowedGSBModel(testcol,7)

print(M.get_model())
print(info(M.graph))
M.fit(min_freq=10)
print(M.ranking)
M.evaluate()
df = M.results_to_df()
write(xl_namefile='example.xlsx', dest_path="experiments/collections/test", sheetname="test0", data=df)

# print(f"ranking size = {len(M.ranking)}\nfirst Q: {M.ranking[0]}")


N = WindowedGSBModel(testcol, 3)
print(N.get_model())
# print(info(N.graph))
N.fit(min_freq=10)
N.evaluate()
# df = M.results_to_df()
print(len(N.ranking))
df = N.results_to_df()
write(xl_namefile='example.xlsx', dest_path="experiments/collections/test", sheetname="test1", data=df)

# testing = Gow(testcol)
# testing.fit()
# testing.evaluate()
# print(len(testing.ranking))
# df = testing.results_to_df()
# write(xl_namefile='example.xlsx', dest_path="experiments/collections/test", sheetname="test2", data=df)

# bord = BordaCount(M.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()

#M
#res_to_excel(M,"testM.xlsx",dest_path,sheetname="test13")
# #N
# res_to_excel(N,"testN.xlsx",dest_path,sheetname="test16")
# #bord
# res_to_excel(bord,"testBord.xlsx",dest_path,sheetname="test13_16")
