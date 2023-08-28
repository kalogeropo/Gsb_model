from models.GSB import GSBModel
from models.GoW import Gow
from models.SetBased import SetBasedModel
from utilities.document_utls import res_to_excel
from Preprocess.Collection import Collection
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount

for i in range(0,9):
    path = 'collections/CF/docs'
    path_to_write = 'data/test_docs/tests'
    col_path = 'data'
    testcol = Collection(path, name="test")
    testcol.create_collection()
    testcol.save_inverted_index(path_to_write)
    q, r = testcol.load_collection(col_path)

    N = GSBModel(testcol)
