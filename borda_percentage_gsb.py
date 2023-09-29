from numpy import mean
from pandas import DataFrame

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.Result_handling import res_to_excel, expir_start, write

"""percentage window testing """

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

list_of_prec = [i for i in range(0,100,5)]
map_perc_wind =[]
map_borda = []
for i in list_of_prec:
    print(f"{list_of_prec.index(i)+1} of {len(list_of_prec)}")
    perc = i/100
    M = WindowedGSBModel(testcol,perc)
    M.fit(min_freq=10)
    M.evaluate()
    map_perc_wind.append(mean(M.precision))

    N = GSBModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()

    bord = BordaCount(M.ranking, N.ranking, testcol)
    bord.fit()
    bord.evaluate()
    map_borda.append(mean(bord.precision))

    #res_to_excel(bord,"testBord_percentage_Gsb.xlsx",dest_path,sheetname=f"gsb_perc_{i}")

df = DataFrame(list(zip(map_perc_wind,map_borda)), columns=["Perc","Borda"])
write(xl_namefile="testBord_percentage_Gsb.xlsx", dest_path=dest_path, sheetname="acc_borda_perc_gsb", data=df)