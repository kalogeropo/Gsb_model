from models.SetBased import SetBasedModel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.Result_handling import expir_start

#CF
path = 'experiments/collections/CF/docs'
path_to_write = 'experiments/temp'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"

#NPL
# path = 'experiments/collections/NPL/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/NPL'
# dest_path = "experiments/paper_results/NPL_results"
testcol, q, r = expir_start(path, path_to_write, col_path)


# M = SetBasedModel(testcol)
# M.fit(min_freq=10)
# M.evaluate()
#
# N = WindowedGSBModel(testcol,10)
# N.fit(min_freq=10)
# N.evaluate()
# print(len(N.ranking))
#
# bord = BordaCount(M.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()
# dest_path= "collections/test/Results"
# #M
# res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
# #N
# res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test10")
# #bord
# res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__10")
#
# ###########################################################
# M = SetBasedModel(testcol)
# M.fit(min_freq=10)
# M.evaluate()
#
# N = WindowedGSBModel(testcol,13)
# N.fit(min_freq=10)
# N.evaluate()
# print(len(N.ranking))
#
# bord = BordaCount(M.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()
# dest_path= "collections/test/Results"
# #M
# res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
# #N
# res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test13")
# #bord
# res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__13")
# ####################################################################################
# M = SetBasedModel(testcol)
# M.fit(min_freq=10)
# M.evaluate()
#
# N = WindowedGSBModel(testcol,16)
# N.fit(min_freq=10)
# N.evaluate()
# print(len(N.ranking))
#
# bord = BordaCount(M.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()
# dest_path= "collections/test/Results"
# #M
# res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
# #N
# res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test16")
# #bord
# res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__16")
#
#
# ######################################################################################
# # M = SetBasedModel(testcol)
# # M.fit(min_freq=10)
# # M.evaluate()

N = WindowedGSBModel(testcol,7)
N.fit(min_freq=10)
N.evaluate()
print(len(N.ranking))

# bord = BordaCount(M.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()
# dest_path= "collections/test/Results"
# #M
# res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
# #N
# res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test19")
# #bord
# res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__19")
# ###############################################################################
# # M = SetBasedModel(testcol)
# # M.fit(min_freq=10)
# # M.evaluate()
# #
# # N = WindowedGSBModel(testcol,7)
# # N.fit(min_freq=10)
# # N.evaluate()
# # print(len(N.ranking))
# #
# # bord = BordaCount(M.ranking, N.ranking, testcol)
# # bord.fit()
# # bord.evaluate()
# # dest_path="collections/test/Results"
# # #M
# # res_to_excel(M,"testsetbased.xlsx",dest_path,sheetname="test1")
# # #N
# # res_to_excel(N,"testwindowed.xlsx",dest_path,sheetname="test7")
# # #bord
# # res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname="test__7")
# print("-------THE END---------------------")
# doc (---- ----  ----)