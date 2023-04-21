from networkx import info

from Preprocess.Collection import Collection
from Preprocess.Document import Document
from models.GoW import Gow
from models.SetBased import SetBasedModel
from models.GSB import GSBModel
from models.WindowedGSB import WindowedGSBModel
path = 'collections/CF/docs'
#path = 'collections/test/docs'
path_to_write ='data/test_docs/tests'
col_path = 'data'
testcol = Collection(path,name = "test")
#print(testcol)
testcol.create_collection()
#print(testcol.inverted_index)
testcol.save_inverted_index(path_to_write)
q,r = testcol.load_collection(col_path)
#print(q)
# print(len(testcol.inverted_index))
# M = WindowedGSBModel(testcol,10)
# print(M.get_model())
# print(info(M.graph))
# M.fit(min_freq=10)
# M.evaluate()

testing = Gow(testcol)
testing.fit()