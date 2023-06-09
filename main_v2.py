from models.SetBased import SetBasedModel
from utilities.document_utls import res_to_excel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount

"""Borda count :window and set based model"""
path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

M = SetBasedModel(testcol)
M.fit(min_freq=10)
M.evaluate()

N = WindowedGSBModel(testcol,10)
N.fit(min_freq=10)
N.evaluate()
print(len(N.ranking))

bord = BordaCount(M.ranking, N.ranking, testcol)
bord.fit()
bord.evaluate()
dest_path="collections/test/debug_res"
#M
res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
#N
res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test10")
#bord
res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__10")

###########################################################
M = SetBasedModel(testcol)
M.fit(min_freq=10)
M.evaluate()

N = WindowedGSBModel(testcol,13)
N.fit(min_freq=10)
N.evaluate()
print(len(N.ranking))

bord = BordaCount(M.ranking, N.ranking, testcol)
bord.fit()
bord.evaluate()
dest_path="collections/test/debug_res"
#M
res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
#N
res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test13")
#bord
res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__13")
####################################################################################
M = SetBasedModel(testcol)
M.fit(min_freq=10)
M.evaluate()

N = WindowedGSBModel(testcol,16)
N.fit(min_freq=10)
N.evaluate()
print(len(N.ranking))

bord = BordaCount(M.ranking, N.ranking, testcol)
bord.fit()
bord.evaluate()
dest_path="collections/test/debug_res"
#M
res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
#N
res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test16")
#bord
res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__16")


######################################################################################
M = SetBasedModel(testcol)
M.fit(min_freq=10)
M.evaluate()

N = WindowedGSBModel(testcol,19)
N.fit(min_freq=10)
N.evaluate()
print(len(N.ranking))

bord = BordaCount(M.ranking, N.ranking, testcol)
bord.fit()
bord.evaluate()
dest_path="collections/test/debug_res"
#M
res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
#N
res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test19")
#bord
res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__19")
###############################################################################
# M = SetBasedModel(testcol)
# M.fit(min_freq=10)
# M.evaluate()
#
# N = WindowedGSBModel(testcol,7)
# N.fit(min_freq=10)
# N.evaluate()
# print(len(N.ranking))
#
# bord = BordaCount(M.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()
# dest_path="collections/test/debug_res"
# #M
# res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
# #N
# res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test7")
# #bord
# res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__7")
print("-------THE END---------------------")