from Preprocess.Collection import Collection
from Preprocess.Document import Document
from models.setbased import SetBased_model

path = 'collections/CF/docs'
path_to_write ='data/test_docs/tests'
col_path = 'data'
testcol = Collection(path,name = "test")
#print(testcol)
testcol.create_collection()
#print(testcol.inverted_index)
testcol.save_inverted_index(path_to_write)
q,r = testcol.load_collection(col_path)
#print(q)

M = SetBased_model(testcol)
print(M.get_model())
M.fit(min_freq=10)
M.evaluate()
