from numpy import mean
from pandas import DataFrame

from models.SetBased import SetBasedModel
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.Result_handling import res_to_excel, expir_start, write

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

wind_list = [8,9,11,12,14,15,17,18,20,21,22,23,24,25]

map_borda = []
map_wind = []
map_set = []

for i in wind_list:
    print(f"{wind_list.index(i)} of {len(wind_list)}")
    M = WindowedGSBModel(testcol,i)
    M.fit(min_freq=10)
    M.evaluate()
    map_wind.append(mean(M.precision))

    N = SetBasedModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()
    map_set.append(mean(N.precision))

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    map_borda.append(mean(bord.precision))
    res_to_excel(bord,"testBord_set_win.xlsx",dest_path,sheetname=f"set_wind_{i}")
df = DataFrame(list(zip(map_set,map_wind,map_borda)), columns=["Set","WIND","Borda"])
write(xl_namefile="testBord_set_win.xlsx", dest_path=dest_path, sheetname="acc_borda_win_set", data=df)
