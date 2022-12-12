import json
from os import getcwd, listdir, path

import numpy as np

#on creating a graph index, to cast int32 to int for JSON graph indexing
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

#Here is the queries and relevant parser. It is important to notice that, this class does NOT handle the collection
#parsing, but the *.txt files which are created by the neccessary collection parsing scripts
class parser():
    def __init__(self):
        self.coll_path = "".join([getcwd(), "/collections/"])
        self.queries = []
        self.relevant = []
    def load_collection(self,col_path=''):
        self.coll_path="".join([self.coll_path,col_path])
        if path.exists(self.coll_path):
            for item in listdir(self.coll_path):
                if item == "Queries.txt":
                    with open("".join([self.coll_path,"/Queries.txt"]),"r") as fd:
                        self.queries= [q.upper().split() for q in fd.readlines()]
                if item == "Relevant.txt":
                    with open("".join([self.coll_path,"/Relevant.txt"]),"r") as fd:
                        self.relevant=[[int(id) for id in d.split()] for d in fd.readlines()]
        return self.relevant,self.queries