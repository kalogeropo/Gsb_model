from re import findall
from os import getcwd

class Document():
    def __init__(self, path):
        if path is not None:
            self.path = path
            self.doc_id = int(findall(r'\d+', self.path)[0])
            self.tf = self.create_tf()
        else:
            self.path = getcwd()
            self.doc_id = 696969
            self.tf = {}

    # Split documents in smaller ""Lists"" according to window size.
    # If window size is equal to zero the function calculates
    # the window by taking into account the total length of the
    # file. (minimum window = 8)
    
    def create_tf(self):
        # open document file
        with open(self.path, 'r', encoding='UTF-8') as d:
            # get all terms while checking for blanks and new lines
            terms = d.read().strip().split()

        # create term frequency dictionarys
        tf = {}
        for term in terms:
            if term in tf:
                tf[term] += 1
            else:
                tf[term] = 1

        return tf

