from numpy import mean
from pandas import DataFrame

from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from utilities.Result_handling import expir_start, res_to_excel, write

"""percentage window testing """
#CF
# path = 'experiments/collections/CF/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/CF'
# dest_path = "experiments/paper_results"
#NPL
path = 'experiments/collections/NPL/docs'
path_to_write = 'experiments/temp'
col_path = 'experiments/collections/NPL'
dest_path = "experiments/paper_results/NPL_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

list_to_total = []
test_name = []
for i in range(0,100,5):
    perc = i/100
    N = WindowedGSBModel(testcol,perc)
    N.fit(min_freq=10)
    N.evaluate()
    list_to_total.append(mean(N.precision))
    name = f"test_{i}"
    test_name.append(name)
    res_to_excel(N,"[NPL]perc_windowTesting.xlsx",dest_path,sheetname=name)

df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
write(xl_namefile="[NPL]perc_windowTesting.xlsx", dest_path=dest_path, sheetname="perc_windowsize_aggregate", data=df)
# for i in range(0, 5,1):
#     perc = i / 100
#     N = WindowedGSBModel(testcol, perc)
#     N.fit(min_freq=10)
#     N.evaluate()
#     dest_path = "collections/test/Results"
#     res_to_excel(N, "perc_windowTesting.xlsx", dest_path, sheetname=f"f_t_test_{i}")
