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
times_simple_GSB = []
times_GSB_prune_importance = []
prune_vals = [p for p in range(10, 610, 20)]
countdown = len(importance_vals) * len(prune_vals)
dest_path = "collections/test/Results"
MAP = []
MAP_simple = []
name = []
n = []
for h in importance_vals:
    for p in prune_vals:
        print(countdown)
        countdown -= 1
        test = GSBModel(testcol, True, h_val=h, p_val=p)
        test2 = GSBModel(testcol)

        test.fit(min_freq=10)
        test.evaluate()
        test2.fit(min_freq=10)
        test2.evaluate()

        times_GSB_prune_importance.append(test.elapsed_time)
        times_simple_GSB.append(test2.elapsed_time)

        MAP.append(mean(test.precision))
        MAP_simple.append(mean(test2.precision))
        print(mean(test2.precision))
        testname = f"GSB_h={h}_p={p}"
        n.append(f"GSB")
        name.append(testname)
        if countdown == 28:
            break
#df = DataFrame(list(zip(times_GSB_prune_importance,MAP, name,n,MAP_simple,times_simple_GSB)), columns=["time_pruned","map_pruned", "Pruned","Simple","map_simple" , "times_simple"])
#write(xl_namefile="gsb_h_prune_w_o_3.xlsx", dest_path=dest_path, sheetname="stats", data=df)
