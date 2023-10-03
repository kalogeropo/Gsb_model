from numpy import mean
from pandas import DataFrame

from models.GSB import GSBModel
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.Result_handling import expir_start, res_to_excel, write

'''Borda count  window GSB model testing '''
path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

map_borda = []
map_wind = []
map_gsb = []

for i in range(5,26):
    print(i)
    M = WindowedGSBModel(testcol,i)
    M.fit(min_freq=10)
    M.evaluate()
    map_wind.append(mean(M.precision))

    N = GSBModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()
    map_gsb.append(mean(N.precision))

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    map_borda.append(mean(bord.precision))

    #M
    #res_to_excel(M,"testM.xlsx",dest_path,sheetname="test13")
    #N
    #res_to_excel(N,"testN.xlsx",dest_path,sheetname="test16")
    #bord
    res_to_excel(bord,"Bord_wind_gsb.xlsx",dest_path,sheetname=f"gsb_win_{i}")
df = DataFrame(list(zip(map_gsb,map_wind,map_borda)), columns=["GSB","WIND","Borda"])
write(xl_namefile="Bord_wind_gsb.xlsx", dest_path=dest_path, sheetname="acc_borda_win_gsb", data=df)
