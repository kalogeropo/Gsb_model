from Preprocess.Collection import Collection
from models.GoW import Gow
from utilities.document_utls import res_to_excel

path = 'collections/CF/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)
wind_list = [i for i in range(5,26)]
for i in wind_list:
    print(f"{wind_list.index(i)+1} of {len(wind_list)}")
    M = Gow(testcol, i)
    M.fit()
    M.evaluate()

    dest_path = "collections/test/Results"
    res_to_excel(M, "test_GoW.xlsx", dest_path, sheetname=f"GoW_{i}")