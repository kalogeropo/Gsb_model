from networkx import info
from numpy import mean
from pandas import DataFrame

from models.SetBased import SetBasedModel
from utilities.Result_handling import expir_start, write, res_to_excel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

map_borda = []
map_wind7 = []
map_set = []
support = [2, 3, 4, 5, 10, 15,20]
for sup in support:
    print(f"{support.index(sup) + 1} out of {len(support)}")

    M = WindowedGSBModel(testcol,7)
    M.fit(min_freq=sup)
    M.evaluate()
    map_wind7.append(mean(M.precision))

    N = SetBasedModel(testcol)
    N.fit(min_freq=sup)
    N.evaluate()
    map_set.append(mean(N.precision))

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    map_borda.append(mean(bord.precision))

    res_to_excel(bord,"borda_set_wind7_apriori.xlsx",dest_path,sheetname=f"set_wind7_apri_{sup}")

df = DataFrame(list(zip(map_set,map_wind7,map_borda)), columns=["set","win7","Borda"])
write(xl_namefile="borda_set_wind7_apriori.xlsx", dest_path=dest_path, sheetname="acc_borda_perc_gsb", data=df)

