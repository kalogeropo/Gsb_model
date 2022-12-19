from argparse import ArgumentParser
from testing import Tester
from os import getcwd, listdir, path


# TODO: handle incorrect parameters on model
class Parser():
    def __init__(self):
        self.queries = []
        self.relevant = []

        self.prs = ArgumentParser()
        self.prs.add_argument("--test_name", dest="test_name", help="Name")
        self.prs.add_argument("--Model", dest="model", help="Model Name")
        self.prs.add_argument("--Parameters", action="append", dest="params", default=[], help="Model Parameters")
        self.prs.add_argument('--version', action='version', version='%(prog)s 0.1')
        self.prs.add_argument("--path", dest="path", help="Set Collection Path")

        args = self.prs.parse_args()

        self.model = args.model
        self.test_name = args.test_name
        self.params = args.params
        self.coll_path = "".join([getcwd(), "/collections/", args.path])
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
        else: raise 'Path may not be correct.'
        return self.relevant, self.queries


    def create_test(self):
        #     def __init__(self, name, model, params, coll_path="/data/docs", rel=None, quer=None):
        test = Tester(self.test_name, self.model, self.params, self.coll_path, self.relevant, self.queries)
        test.start_model()


if __name__ == "__main__": # is this file directly run by python OR is it being imported?
    parser = Parser()
    parser.load_collection()
    parser.create_test()
