from timeit import default_timer as timer

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from models.SetBased import SetBasedModel
from models.WindowedGSB import WindowedGSBModel
from utilities.document_utls import res_to_excel

support = [1, 2, 5, 10, 15]

set_times = []
gsb_times = []
wind_times = []

path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

dest_path = "collections/test/Results"


for sup in support:
    print(f"{support.index(sup) + 1} out of {len(support)}")
    # set
    start = timer()
    M = SetBasedModel(testcol)
    M.fit(min_freq=sup)
    M.evaluate()
    end = timer()
    res_to_excel(M, "apriori_set.xlsx", dest_path, sheetname=f"sup_{sup}")
    set_times.append(end - start)

    # GSB
    start = timer()
    N = GSBModel(testcol)
    N.fit(min_freq=sup)
    N.evaluate()
    end = timer()
    res_to_excel(N, "apriori_gsb.xlsx", dest_path, sheetname=f"sup_{sup}")
    gsb_times.append(end - start)

    # windowed
    start = timer()
    K = WindowedGSBModel(testcol, 7)
    K.fit(min_freq=sup)
    K.evaluate()
    end = timer()
    res_to_excel(K, "apriori_win_7.xlsx", dest_path, sheetname=f"sup_{sup}")
    wind_times.append(end - start)

print(f"set-based time: {set_times} \n ------\n"
      f"GSB time: {gsb_times} \n ------\n"
      f"Windowed GSB - 7 time: {wind_times}\n-------")
