from networkx import info

from models.SetBased import SetBasedModel
from utilities.document_utls import res_to_excel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount

path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

# wind_list = [8,9,11,12,14,15,17,18,20,21,22,23,24,25]
# for i in wind_list:
#     print(f"{wind_list.index(i)} of {len(wind_list)}")
#     M = WindowedGSBModel(testcol,i)
#     M.fit(min_freq=10)
#     M.evaluate()
#
#     N = SetBasedModel(testcol)
#     N.fit(min_freq=10)
#     N.evaluate()
#
#     bord = BordaCount(M.ranking, N.ranking, testcol)
#     bord.fit()
#     bord.evaluate()
#     dest_path= "collections/test/Results"
#     res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname=f"set_wind_{i}")

