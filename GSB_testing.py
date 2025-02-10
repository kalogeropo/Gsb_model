from numpy import mean
from pandas import DataFrame

from models.GSB import GSBModel
from utilities.Result_handling import expir_start, res_to_excel, write

""" complete gsb testing """
#CF
# path = 'experiments/collections/CF/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/CF'
# dest_path = "experiments/paper_results"

#NPL
# path = 'experiments/collections/NPL/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/NPL'
# dest_path = "experiments/paper_results/NPL_results"

#CRAN
path = 'experiments/collections/CRAN/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CRAN'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

list_to_total = []
test_name = []

# for reproducibility
for i in range(0, 5):
    N = GSBModel(testcol)
    N.fit(min_freq=10, stopwords=True)
    N.evaluate()
    list_to_total.append(mean(N.precision))
    name = f"test_{i}"
    test_name.append(name)
    res_to_excel(N, "[CRAN]GSBTesting.xlsx", dest_path, sheetname=name)
    print(mean(N.precision))
df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
write(xl_namefile="[CRAN]GSBTesting.xlsx", dest_path=dest_path, sheetname="aggregate", data=df)
