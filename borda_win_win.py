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


for i in wind_list:
    for j in wind_list:
        if i<j:
            print(i,j)

            M = WindowedGSBModel(testcol,i)
            M.fit(min_freq=10)
            M.evaluate()

            N = WindowedGSBModel(testcol,j)
            N.fit(min_freq=10)
            N.evaluate()

            bord = BordaCount(M.ranking, N.ranking, testcol)
            bord.fit()
            bord.evaluate()
            dest_path= "collections/test/Results"
            res_to_excel(bord,"bord_win_win.xlsx",dest_path,sheetname=f"w_{i}_{j}")
