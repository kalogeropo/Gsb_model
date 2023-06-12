from Preprocess.Collection import Collection
from models.GSB import GSBModel
from models.SetBased import SetBasedModel
from statistics import mean

from models.WindowedGSB import WindowedGSBModel

from timeit import default_timer as timer

support = [1, 2, 5, 10, 15]

av_pre_set = []
set_times = []
av_pre_gsb = []
gsb_times = []
av_pre_wind = []
wind_times = []

path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

for sup in support:

    # set
    start = timer()
    M = SetBasedModel(testcol)
    M.fit(min_freq=sup)
    M.evaluate()
    end = timer()
    av_pre_set.append([mean(i) for i in M.ranking ])
    set_times.append(end - start)

    # GSB
    start = timer()
    N = GSBModel(testcol)
    N.fit(min_freq=sup)
    N.evaluate()
    end = timer()
    av_pre_gsb.append([mean(i) for i in mean(N.ranking)])
    gsb_times.append(end - start)

    # windowed
    start = timer()
    K = WindowedGSBModel(testcol, 7)
    K.fit(min_freq=sup)
    K.evaluate()
    end = timer()
    av_pre_wind.append([mean(i) for i in mean(K.ranking)])
    wind_times.append(end - start)

print(f"set-based: AV Pre: {av_pre_set} \n time: {set_times} \n ------\n"
      f"GSB : AV Pre: {av_pre_gsb} \n time: {gsb_times} \n ------\n"
      f"Windowed GSV: {av_pre_wind} \n time: {wind_times}\n-------")
