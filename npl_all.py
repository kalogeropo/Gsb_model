from timeit import default_timer as timer

from numpy import mean
from pandas import DataFrame

from models.GSB import GSBModel
from models.SetBased import SetBasedModel
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from utilities.Result_handling import expir_start, res_to_excel, write


#apriori --->
#support = [1, 2, 3, 4, 5, 10, 15, 20]
support = [ 3, 4, 5, 10, 15, 20]

set_times = []
gsb_times = []
wind_times = []
set_pre = []
gsb_pre = []
wind_pre = []

#NPL
path = 'experiments/collections/NPL/docs'
path_to_write = 'experiments/temp'
col_path = 'experiments/collections/NPL'
dest_path = "experiments/paper_results/NPL_results"
testcol, q, r = expir_start(path, path_to_write, col_path)


for sup in support:
    print(f"{support.index(sup) + 1} out of {len(support)}")
    # set
    start = timer()
    M = SetBasedModel(testcol)
    M.fit(min_freq=sup)
    M.evaluate()
    end = timer()
    res_to_excel(M, "[NPL]apriori_set.xlsx", dest_path, sheetname=f"sup_{sup}")
    set_times.append(end - start)
    set_pre.append(mean(M.precision))
    # GSB
    start = timer()
    N = GSBModel(testcol)
    print(N.collection.inverted_index)
    N.fit(min_freq=sup)
    N.evaluate()
    end = timer()
    res_to_excel(N, "[NPL]apriori_gsb.xlsx", dest_path, sheetname=f"sup_{sup}")
    gsb_times.append(end - start)
    gsb_pre.append(mean(N.precision))

    # windowed
    start = timer()
    K = WindowedGSBModel(testcol, 3,window_cut_off=False)
    K.fit(min_freq=sup)
    K.evaluate()
    end = timer()
    res_to_excel(K, "[NPL]apriori_win_3.xlsx", dest_path, sheetname=f"sup_{sup}")
    wind_times.append(end - start)
    wind_pre.append(mean(K.precision))

df = DataFrame(list(zip(set_times,set_pre,gsb_times,gsb_pre,wind_times,wind_pre)), columns=["set_times","set_pre","gsb_times","gsb_pre","wind_times","wind_pre"])
write(xl_namefile="[NPL]stats.xlsx", dest_path=dest_path, sheetname="set_gsb_wgsb", data=df)
print(f"set-based time: {set_times} \n ------\n"
      f"GSB time: {gsb_times} \n ------\n"
      f"Windowed GSB - 3 time: {wind_times}\n-------")

#borda win win
wind_list = [i for i in range(3,13)]
cnt = 0
map_borda = []
map_windsmall = []
map_windbig = []
for i in wind_list:
    for j in wind_list:
        if i<j:
            cnt += 1
            print(f"{cnt} out of {(len(wind_list)*(len(wind_list)-1))/2}")

            M = WindowedGSBModel(testcol,i,window_cut_off=False)
            M.fit(min_freq=1)
            M.evaluate()
            map_windsmall.append(mean(M.precision))

            N = WindowedGSBModel(testcol,j,window_cut_off=False)
            N.fit(min_freq=1)
            N.evaluate()
            map_windbig.append(mean(N.precision))

            bord = BordaCount(M.ranking, N.ranking, testcol)
            bord.fit()
            bord.evaluate()
            map_borda.append(mean(bord.precision))

            res_to_excel(bord,"[npl]bord_win_win.xlsx",dest_path,sheetname=f"w_{i}_{j}")
df = DataFrame(list(zip(map_windsmall,map_windbig,map_borda)), columns=["wind_small","winBig","Borda"])
write(xl_namefile="[npl]bord_win_win.xlsx", dest_path=dest_path, sheetname="acc_borda_wins_winb", data=df)


list_to_total = []
test_name = []
c=0
#for i in range(3,6):
for i in range(3,25):
    print(f"{c} of { len(range(3, 25))}")
    c += 1
    N = WindowedGSBModel(testcol,i,window_cut_off=False)
    N.fit(min_freq=1)
    N.evaluate()
    list_to_total.append(mean(N.precision))
    name = f"test_{i}"
    test_name.append(name)
    res_to_excel(N,"[NPL]windowTesting.xlsx",dest_path,sheetname=name)

df = DataFrame(list(zip(list_to_total, test_name)), columns=["map", "Names"])
write(xl_namefile="[NPL]windowTesting.xlsx", dest_path=dest_path, sheetname="windowsize_aggregate", data=df)
