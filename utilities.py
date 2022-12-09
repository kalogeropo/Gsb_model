import json
from os import getcwd, listdir, path

import numpy as np


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
                        self.queries=(fd.read().strip().lower().split("\n"))
                if item == "Relevant.txt":
                    with open("".join([self.coll_path,"/Relevant.txt"]),"r") as fd:
                        self.relevant=(fd.read().strip().split("\n"))