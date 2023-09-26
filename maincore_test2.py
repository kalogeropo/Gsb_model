from numpy import mean
from pandas import DataFrame

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from utilities.ExcelWriter import write
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

#importance_vals = [h for h in range(30, 200, 20)]
importance_vals =[50]
# prune_vals = [p for p in range(350, 610, 20)]
prune_vals = [p for p in range(610, 710, 20)]
countdown = len(importance_vals) * len(prune_vals)
dest_path = "collections/test/Results"
MAP = []
name = []
for h in importance_vals:
    for p in prune_vals:
        print(countdown)
        countdown -= 1
        test = GSBModel(testcol, True, h_val=h, p_val=p)
        # test = WindowedGSBModel(testcol, 8, True)
        test.fit(min_freq=11)
        test.evaluate()
        #res_to_excel(test, "gsb_h_prune_w_o_3.xlsx", dest_path, sheetname=f"GSB_{h}_{p}")
        MAP.append(mean(test.precision))
        testname = f"GSB_h={h}_p={p}"
        name.append(testname)

df = DataFrame(list(zip(MAP, name)), columns=["map", "Names"])
write(xl_namefile="gsb_h_prune_w_o_3.xlsx", dest_path=dest_path, sheetname="GSB_50_610_710", data=df)
