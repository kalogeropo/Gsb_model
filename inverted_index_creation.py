from models.GSB import GSBModel
from utilities.document_utls import res_to_excel, json_to_dat
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel

path = 'collections/CF/docs'
# path = 'collections/test/docs'
path_to_write = 'data/test_docs/tests'
col_path = 'data'
testcol = Collection(path, name="test")
testcol.create_collection()
testcol.save_inverted_index(path_to_write)
q, r = testcol.load_collection(col_path)

M = WindowedGSBModel(testcol,7)

json_to_dat(testcol,filename="window7invertedindex.dat")

M = GSBModel(testcol)

json_to_dat(testcol,filename="GSBinvertedindex.dat")