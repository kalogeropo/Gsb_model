import os
from argparse import ArgumentParser
from Testing import tester
from os import getcwd, listdir, path


class parser():
    def __init__(self):
        self.coll_path = "".join([getcwd(), "/collections/"])
        self.queries = []
        self.relevant = []
        self.prs = ArgumentParser()
        self.prs.add_argument("--test_name",dest = "test_name",help="Name")
        self.prs.add_argument("--Model",dest="model",help="Model Name")
        self.prs.add_argument("--Parameters",action="append",dest="params",default=[], help="Model Parameters")
        self.prs.add_argument('--version', action='version',version='%(prog)s 0.1')
        self.prs.add_argument("--path",dest="path",help="Set Collection Path")
        args = self.prs.parse_args()
        self.model = args.model
        self.test_name = args.test_name
        self.params = args.params
        #self.coll_path = "".join([self.coll_path, "/",args.path,"/"])
        print(args)


    def load_collection(self, col_path=''):
        self.coll_path = "".join([self.coll_path, col_path])
        if path.exists(self.coll_path):
            for item in listdir(self.coll_path):
                if item == "Queries.txt":
                    with open("".join([self.coll_path, "/Queries.txt"]), "r") as fd:
                        self.queries = [q.upper().split() for q in fd.readlines()]
                if item == "Relevant.txt":
                    with open("".join([self.coll_path, "/Relevant.txt"]), "r") as fd:
                        self.relevant = [[int(id) for id in d.split()] for d in fd.readlines()]
        return self.relevant, self.queries
    def create_test(self):
        #def __init__(self, name, model, params=[], coll_path="/data/docs"):
        test = tester(self.test_name,self.model,self.params,rel_path=self.coll_path)
        test.start_model()

parser = parser()
parser.create_test()
