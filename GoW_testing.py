from numpy import mean
from pandas import DataFrame

from models.GoW import Gow
from utilities.Result_handling import expir_start, res_to_excel, write

#CF
path = 'experiments/collections/CF/docs'
path_to_write = 'experiments/temp'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)
list_to_total = []
test_name = []
wind_list = [i for i in range(5,26)]

for i in wind_list:
    print(f"{wind_list.index(i)+1} of {len(wind_list)}")
    M = Gow(testcol, i)
    M.fit()
    M.evaluate()
    name = f"GoW_{i}"
    list_to_total.append(mean(M.precision))
    test_name.append(name)
    res_to_excel(M, "test_GoW.xlsx", dest_path, sheetname=name)
df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
write(xl_namefile="test_GoW.xlsx", dest_path=dest_path, sheetname="GoW_aggregate", data=df)
#NPL
path = 'experiments/collections/NPL/docs'
path_to_write = 'experiments/temp'
col_path = 'experiments/collections/NPL'
dest_path = "experiments/paper_results/NPL_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

list_to_total = []
test_name = []

wind_list = [i for i in range(5,26)]
for i in wind_list:
    print(f"{wind_list.index(i)+1} of {len(wind_list)}")
    M = Gow(testcol, i)
    M.fit()
    M.evaluate()
    name = f"GoW_{i}"
    list_to_total.append(mean(M.precision))
    test_name.append(name)
    res_to_excel(M, "[NPL]test_GoW.xlsx", dest_path, sheetname=name)
df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
write(xl_namefile="[NPL]test_GoW.xlsx", dest_path=dest_path, sheetname="GoW_aggregate", data=df)