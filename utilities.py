import json
from os import getcwd, listdir, path

from pandas import ExcelWriter
import numpy as np



# on creating a graph index, to cast int32 to int for JSON graph indexing
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.int32):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


# Here is the queries and relevant parser. It is important to notice that, this class does NOT handle the collection
# parsing, but the *.txt files which are created by the neccessary collection parsing scripts



#TODO: CREATE file with test name as name if not exists, Fix warning on writer.save()
class excelwriter():
    def __init__(self):
        self.res_path = "".join([getcwd(), "/results/"])

    def write_results(self,path,df):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = ExcelWriter("".join([self.res_path,'pandas_simple.xlsx']), engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
