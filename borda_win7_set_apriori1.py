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
support = [2, 3, 4, 5, 10, 15,20]
for sup in support:
    print(f"{support.index(sup) + 1} out of {len(support)}")

    M = WindowedGSBModel(testcol,7)
    M.fit(min_freq=sup)
    M.evaluate()

    N = SetBasedModel(testcol)
    N.fit(min_freq=sup)
    N.evaluate()

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    dest_path= "collections/test/Results"
    res_to_excel(bord,"borda_set_wind7_apriori.xlsx",dest_path,sheetname=f"set_wind7_apri_{sup}")

