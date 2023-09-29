from numpy import mean
from pandas import DataFrame

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from utilities.Result_handling import write, expir_start

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

importance_vals =[50]
times_simple_GSB = []
times_GSB_prune_importance = []

prune_vals = [p for p in range(10, 610, 20)]
countdown = len(importance_vals) * len(prune_vals)

MAP = []
MAP_simple = []
name = []
n = []
num_of_complete_edges = []
num_of_pruned_edges = []

for h in importance_vals:
    for p in prune_vals:
        print(countdown)
        countdown -= 1
        test = GSBModel(testcol, True, h_val=h, p_val=p)
        test.fit(min_freq=10)
        test.evaluate()
        times_GSB_prune_importance.append(test.elapsed_time)
        MAP.append(mean(test.precision))
        num_of_pruned_edges.append(test.graph.number_of_edges())
        print(mean(test.precision))
        testname = f"GSB_h={h}_p={p}"
        name.append(testname)

        test2 = GSBModel(testcol)
        test2.fit(min_freq=10)
        test2.evaluate()
        times_simple_GSB.append(test2.elapsed_time)
        MAP_simple.append(mean(test2.precision))
        print(mean(test2.precision))
        n.append(f"GSB")
        num_of_complete_edges.append(test2.graph.number_of_edges())

        #if countdown == 28: break
df = DataFrame(list(zip(times_GSB_prune_importance,MAP, name,num_of_pruned_edges,n,MAP_simple,times_simple_GSB,num_of_complete_edges)),
               columns=["time_pruned","map_pruned", "Pruned","Pruned Edges","Simple","map_simple" , "times_simple","Complete Edges"])
write(xl_namefile="gsb_h_prune_w_o_3.xlsx", dest_path=dest_path, sheetname="stats", data=df)
