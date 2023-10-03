from numpy import mean
from pandas import DataFrame

from models.GSB import GSBModel
from models.GoW import Gow
from utilities.Result_handling import expir_start, res_to_excel, write
from models.borda_count import BordaCount

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

map_borda = []
map_gow = []
map_gsb = []

wind_list = [i for i in range(5,26)]
for i in wind_list:
    print(f"{wind_list.index(i)} of {len(wind_list)}")
    M = Gow(testcol, i)
    M.fit()
    M.evaluate()

    map_gow.append(mean(M.precision))

    N = GSBModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()
    map_gsb.append(mean(N.precision))

    # print(M.ranking)
    # print(N.ranking)
    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    map_borda.append(mean(bord.precision))

    res_to_excel(bord, "testBord_vazir_gsb.xlsx", dest_path, sheetname=f"gsb_GoW_{i}")

df = DataFrame(list(zip(map_gow,map_gsb,map_borda)), columns=["gow","gsb","Borda"])
write(xl_namefile="testBord_vazir_gsb.xlsx", dest_path=dest_path, sheetname="acc_borda_gow_gsb", data=df)