from models.GSB import GSBModel
from utilities.document_utls import res_to_excel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount

'''Borda count  window GSB model testing '''

path = 'collections/CF/docs'
path_to_write = '/data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

for i in range(5,26):
    print(i)
    M = WindowedGSBModel(testcol,i)
    M.fit(min_freq=10)
    M.evaluate()

    N = GSBModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    dest_path= "collections/test/Results"
    #M
    #res_to_excel(M,"testM.xlsx",dest_path,sheetname="test13")
    #N
    #res_to_excel(N,"testN.xlsx",dest_path,sheetname="test16")
    #bord
    res_to_excel(bord,"Bord_wind_gsb.xlsx",dest_path,sheetname=f"gsb_win_{i}")
