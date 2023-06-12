from Preprocess.Collection import Collection
from models.GSB import GSBModel
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.document_utls import res_to_excel

"""percentage window testing """

path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

list_of_prec = [i for i in range(0,100,5)]

for i in list_of_prec:
    print(f"{list_of_prec.index(i)+1} of {len(list_of_prec)}")
    perc = i/100
    M = WindowedGSBModel(testcol,perc)
    M.fit(min_freq=10)
    M.evaluate()

    N = GSBModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    dest_path= "collections/test/Results"
    res_to_excel(bord,"testBord_percentage_Gsb.xlsx",dest_path,sheetname=f"gsb_perc_{i}")
