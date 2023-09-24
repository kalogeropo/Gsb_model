from Preprocess.Collection import Collection
from models.GSB import GSBModel
from models.WindowedGSB import WindowedGSBModel
from utilities.document_utls import res_to_excel

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

importance_vals = [h for h in range(10, 110, 10)]
prune_vals = [p for p in range(30,70,10)]
for h in importance_vals:
    for p in prune_vals:
        test = GSBModel(testcol,True,h_val=h, p_val=p)
        #test = WindowedGSBModel(testcol, 8, True)
        print(test.model)
        test.fit(min_freq=11)
        test.evaluate()
        dest_path = "collections/test/Results"
        res_to_excel(test, "gsb_h_prune.xlsx", dest_path, sheetname=f"GSB_{h}_{p}")
