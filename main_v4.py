from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from utilities.document_utls import res_to_excel

"""percentage window testing """

path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

for i in range(0,100,5):
    perc = i/100
    N = WindowedGSBModel(testcol,perc)
    N.fit(min_freq=10)
    N.evaluate()
    dest_path="collections/test/debug_res"
    res_to_excel(N,"perc_windowTesting.xlsx",dest_path,sheetname=f"test_{i}")
