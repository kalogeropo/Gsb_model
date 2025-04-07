from numpy import mean
from pandas import DataFrame

from models.WindowedGSB import WindowedGSBModel
from utilities.Result_handling import write, expir_start, res_to_excel

# CF
# path = 'experiments/collections/CF/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/CF'
# dest_path = "experiments/paper_results"

# NPL
# TODO: ADD NPL paths
# CRAN

path = 'experiments/collections/CRAN/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CRAN'
dest_path = "experiments/paper_results"


testcol, q, r = expir_start(path, path_to_write, col_path)

importance_vals = [h for h in range(30, 500, 20)]
# prune_vals = [p for p in range(30, 90, 10)]
# prune_vals = [p for p in range(90, 150, 10)]
# prune_vals = [p for p in range(150, 190, 10)]
# prune_vals = [p for p in range(190, 250, 10)]
prune_vals = [1]  # ----> irrelevant
countdown = len(importance_vals) * len(prune_vals)

MAP = []
name = []
model_time = []
for h in importance_vals:
    print(countdown)
    countdown -= 1
    test = WindowedGSBModel(testcol, 3, h, True,window_cut_off=False)
    test.fit(min_freq=1, stopwords=True)
    test.evaluate()
    res_to_excel(test, "[CRAN_new]windwed_h.xlsx", dest_path, sheetname=f"GSB_win_3_{h}")
    MAP.append(mean(test.precision))
    testname = f"wind_8_h={h}"
    name.append(testname)
    model_time.append(test.elapsed_time)
df = DataFrame(list(zip(MAP, name,model_time)), columns=["map", "Names","time"])
write(xl_namefile="[CRAN_new]windwed_h.xlsx", dest_path=dest_path, sheetname="windowed_3_h_aggregate", data=df)
