from numpy import mean
from pandas import DataFrame

from models.GSB import GSBModel
from utilities.Result_handling import write, expir_start

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

importance_vals =[50]
prune_vals = [p for p in range(350, 710, 20)]
countdown = len(importance_vals) * len(prune_vals)
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
