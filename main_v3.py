from utilities.document_utls import res_to_excel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel

'''Constant window testing '''
path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

for i in range(5,20):
    N = WindowedGSBModel(testcol,i)
    N.fit(min_freq=10)
    N.evaluate()
    dest_path= "collections/test/Results"
    res_to_excel(N,"windowTesting.xlsx",dest_path,sheetname=f"test_{i}")
