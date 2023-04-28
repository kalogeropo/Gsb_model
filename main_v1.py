from networkx import info

from Preprocess.Collection import Collection
from models.GoW import Gow
from models.WindowedGSB import WindowedGSBModel
from utilities.ExcelWriter import ExcelWriter

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
M = WindowedGSBModel(testcol,10)
print(M.get_model())
print(info(M.graph))
M.fit(min_freq=10)
M.evaluate()
df = M.results_to_df()

# testing = Gow(testcol)
# testing.fit()
# testing.evaluate()
# df = testing.results_to_df()

writer = ExcelWriter('example.xlsx','collections/test/debug_res')
for i in range(1,5):
    writer.add_sheet(f"test{i}")
    writer.write_data(df)
    writer.save()
writer.append_all_sheets("all_tests")
