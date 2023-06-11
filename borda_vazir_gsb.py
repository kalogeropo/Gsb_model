from models.GSB import GSBModel
from models.GoW import Gow
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

wind_list = [i for i in range(5,26)]
for i in wind_list:
    print(f"{wind_list.index(i)} of {len(wind_list)}")
    M = Gow(testcol, i)
    M.fit()
    M.evaluate()

    N = GSBModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    dest_path = "collections/test/Results"
    res_to_excel(bord, "testBord_vazir_gsb.xlsx", dest_path, sheetname=f"gsb_GoW_{i}")
