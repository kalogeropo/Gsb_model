from numpy import mean
from pandas import DataFrame

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from models.WindowedGSB import WindowedGSBModel
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

importance_vals = [h for h in range(30, 500, 20)]
#prune_vals = [p for p in range(30, 90, 10)]
#prune_vals = [p for p in range(90, 150, 10)]
#prune_vals = [p for p in range(150, 190, 10)]
#prune_vals = [p for p in range(190, 250, 10)]
prune_vals = [1] #----> irrelevant
countdown = len(importance_vals) * len(prune_vals)
dest_path = "collections/test/Results"
MAP = []
name = []
for h in importance_vals:
    for p in prune_vals:
        print(countdown)
        countdown -= 1
        test = WindowedGSBModel(testcol,8,True)
        test.fit(min_freq=11)
        test.evaluate()
        res_to_excel(test, "windwed_h.xlsx", dest_path, sheetname=f"GSB_{h}")
        MAP.append(mean(test.precision))
        testname = f"wind_8_h={h}"
        name.append(testname)

df = DataFrame(list(zip(MAP, name)), columns=["map", "Names"])
write(xl_namefile="windwed_h.xlsx", dest_path=dest_path, sheetname="windowed_h_aggregate", data=df)