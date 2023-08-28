from networkx import info
from utilities.document_utls import res_to_excel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount

path = 'collections/CF/docs'
# path = 'collections/test/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
# print(testcol)
testcol.create_collection()
# print(testcol.inverted_index)
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)
# print(q)
# print(len(testcol.inverted_index))
M = WindowedGSBModel(testcol,7)


print(M.get_model())
print(info(M.graph))
#M.graph node2vec # καθε κομβο
#M.fit(min_freq=10)
#M.evaluate()
# df = M.results_to_df()
print(len(M.ranking))

N = WindowedGSBModel(testcol, 16)
print(N.get_model())
# print(info(N.graph))
N.fit(min_freq=10)
N.evaluate()
# df = M.results_to_df()
print(len(N.ranking))

# testing = Gow(testcol)
# testing.fit()
# testing.evaluate()
# print(len(testing.ranking))
# df = testing.results_to_df()
# write(xl_namefile='example.xlsx', dest_path="collections/test/Results", sheetname="test", data=df)

bord = BordaCount(M.ranking, N.ranking, testcol)
bord.fit()
bord.evaluate()
dest_path= "collections/test/Results"
#M
res_to_excel(M,"testM.xlsx",dest_path,sheetname="test13")
#N
res_to_excel(N,"testN.xlsx",dest_path,sheetname="test16")
#bord
res_to_excel(bord,"testBord.xlsx",dest_path,sheetname="test13_16")
