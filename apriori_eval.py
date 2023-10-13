from timeit import default_timer as timer

from numpy import mean
from pandas import DataFrame

from models.GSB import GSBModel
from models.SetBased import SetBasedModel
from models.WindowedGSB import WindowedGSBModel
from utilities.Result_handling import expir_start, res_to_excel, write

support = [1, 2, 3, 4, 5, 10, 15, 20]

set_times = []
gsb_times = []
wind_times = []
set_pre = []
gsb_pre = []
wind_pre = []

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)


for sup in support:
    print(f"{support.index(sup) + 1} out of {len(support)}")
    # set
    start = timer()
    M = SetBasedModel(testcol)
    M.fit(min_freq=sup)
    M.evaluate()
    end = timer()
    #res_to_excel(M, "apriori_set.xlsx", dest_path, sheetname=f"sup_{sup}")
    set_times.append(end - start)
    set_pre.append(mean(M.precision))
    # GSB
    start = timer()
    N = GSBModel(testcol)
    N.fit(min_freq=sup)
    N.evaluate()
    end = timer()
    #res_to_excel(N, "apriori_gsb.xlsx", dest_path, sheetname=f"sup_{sup}")
    gsb_times.append(end - start)
    gsb_pre.append(mean(N.precision))

    # windowed
    start = timer()
    K = WindowedGSBModel(testcol, 7)
    K.fit(min_freq=sup)
    K.evaluate()
    end = timer()
    #res_to_excel(K, "apriori_win_7.xlsx", dest_path, sheetname=f"sup_{sup}")
    wind_times.append(end - start)
    wind_pre.append(mean(K.precision))

df = DataFrame(list(zip(set_times,set_pre,gsb_times,gsb_pre,wind_times,wind_pre)), columns=["set_times","set_pre","gsb_times","gsb_pre","wind_times","wind_pre"])
write(xl_namefile="stats.xlsx", dest_path=dest_path, sheetname="set_gsb_wgsb", data=df)
print(f"set-based time: {set_times} \n ------\n"
      f"GSB time: {gsb_times} \n ------\n"
      f"Windowed GSB - 7 time: {wind_times}\n-------")
