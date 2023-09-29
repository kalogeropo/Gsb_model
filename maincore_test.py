from numpy import mean
from pandas import DataFrame

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from utilities.Result_handling import write, expir_start, res_to_excel

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

importance_vals = [h for h in range(30, 530, 100)]
prune_vals = [p for p in range(30, 330, 25)]
countdown = len(importance_vals) * len(prune_vals)

num_of_edges = []
MAP = []
name = []

for h in importance_vals:
    for p in prune_vals:
        print(countdown)
        countdown -= 1

        test = GSBModel(testcol, True, h_val=h, p_val=p)
        test.fit(min_freq=10)
        test.evaluate()

        num_of_edges.append(test.graph.number_of_edges())
        #res_to_excel(test, "gsb_h_prune_num_edges.xlsx", dest_path, sheetname=f"GSB_{h}_{p}")
        MAP.append(mean(test.precision))
        testname = f"GSB_h={h}_p={p}"
        name.append(testname)

df = DataFrame(list(zip(MAP, name, num_of_edges)), columns=["map", "Names","Graph Edges"])
write(xl_namefile="gsb_h_prune_num_edges.xlsx", dest_path=dest_path, sheetname="GSB_comp_hyper_aggresive_v2", data=df)
