from numpy import mean
from pandas import DataFrame

from models.WindowedGSB import WindowedGSBModel
from utilities.Result_handling import res_to_excel, expir_start, write

'''Constant window testing '''
# CF
path = 'experiments/collections/CF/docs'
path_to_write = 'experiments/temp'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results/CF_results"

testcol, q, r = expir_start(path, path_to_write, col_path)


list_to_total = []
test_name = []
#for i in range(3,7):
for i in range(3,25):
    N = WindowedGSBModel(testcol,i,window_cut_off=True)
    N.fit(min_freq=1,stopwords=True )
    N.evaluate()
    list_to_total.append(mean(N.precision))
    name = f"test_{i}"
    test_name.append(name)
    res_to_excel(N,"[CF_new]windowTesting.xlsx",dest_path,sheetname=name)

df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
write(xl_namefile="[CF_new]windowTesting.xlsx", dest_path=dest_path, sheetname="windowsize_aggregate", data=df)
#NPL
# path = 'experiments/collections/NPL/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/NPL'
# dest_path = "experiments/paper_results/NPL_results"
# testcol, q, r = expir_start(path, path_to_write, col_path)
testcol, q, r = expir_start(path, path_to_write, col_path)

# CRAN
path = 'experiments/collections/CRAN/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CRAN'
dest_path = "experiments/paper_results"



list_to_total = []
test_name = []
#for i in range(3,7):
for i in range(3,25):
    N = WindowedGSBModel(testcol,i,window_cut_off=True)
    N.fit(min_freq=1,stopwords=True )
    N.evaluate()
    list_to_total.append(mean(N.precision))
    name = f"test_{i}"
    test_name.append(name)
    res_to_excel(N,"[CRAN_new]windowTesting.xlsx",dest_path,sheetname=name)

df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
write(xl_namefile="[CRAN_new]windowTesting.xlsx", dest_path=dest_path, sheetname="windowsize_aggregate", data=df)

# path = 'experiments/collections/NPL/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/NPL'
# dest_path = "experiments/paper_results/NPL_results"
# testcol, q, r = expir_start(path, path_to_write, col_path)

# list_to_total = []
# test_name = []
# #for i in range(3,6):
# for i in range(3,25):
#     N = WindowedGSBModel(testcol,i)
#     N.fit(min_freq=10)
#     N.evaluate()
#     list_to_total.append(mean(N.precision))
#     name = f"test_{i}"
#     test_name.append(name)
#     res_to_excel(N,"[NPL]windowTesting.xlsx",dest_path,sheetname=name)

# df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
# write(xl_namefile="[NPL]windowTesting.xlsx", dest_path=dest_path, sheetname="windowsize_aggregate", data=df)

