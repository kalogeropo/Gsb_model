from numpy import mean

from Preprocess.Collection import Collection
from models.GSB import GSBModel
from utilities.document_utls import res_to_excel

""" complete gsb testing """

path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)
# for reproducibility
for i in range(0, 5):
    perc = i / 100
    N = GSBModel(testcol)
    N.fit(min_freq=10)
    N.evaluate()
    dest_path = "collections/test/Results"
    res_to_excel(N, "GSBTesting.xlsx", dest_path, sheetname=f"test_{i}")
    print(mean(N.precision))
