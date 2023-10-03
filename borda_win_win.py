from numpy import mean
from pandas import DataFrame

from utilities.Result_handling import expir_start, res_to_excel, write
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount

path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"
testcol, q, r = expir_start(path, path_to_write, col_path)

wind_list = [i for i in range(7,16)]
cnt = 0
map_borda = []
map_windsmall = []
map_windbig = []
for i in wind_list:
    for j in wind_list:
        if i<j:
            cnt += 1
            print(f"{cnt} out of {(len(wind_list)*(len(wind_list)-1))/2}")

            M = WindowedGSBModel(testcol,i)
            M.fit(min_freq=10)
            M.evaluate()
            map_windsmall.append(mean(M.precision))

            N = WindowedGSBModel(testcol,j)
            N.fit(min_freq=10)
            N.evaluate()
            map_windbig.append(mean(N.precision))

            bord = BordaCount(M.ranking, N.ranking, testcol)
            bord.fit()
            bord.evaluate()
            map_borda.append(mean(bord.precision))

            res_to_excel(bord,"bord_win_win.xlsx",dest_path,sheetname=f"w_{i}_{j}")
df = DataFrame(list(zip(map_windsmall,map_windbig,map_borda)), columns=["wind_small","winBig","Borda"])
write(xl_namefile="bord_win_win.xlsx", dest_path=dest_path, sheetname="acc_borda_wins_winb", data=df)