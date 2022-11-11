from re import findall
from os import getcwd

class Document():
    def __init__(self, path):
        if isinstance(path, str):
            self.path = path
            self.doc_id = int(findall(r'\d+', self.path)[0])
            try:
                with open(self.path, 'r', encoding='UTF-8') as d:
                    # get all terms while checking for blanks and new lines
                    self.terms = d.read().strip().split()
            except FileNotFoundError:
                raise ('File does not exist.')
            self.tf = self.create_tf()

        else:
            self.path = getcwd()
            self.doc_id = 696969
            self.tf = {}
            self.terms = ["696969"]

    # Split documents in smaller ""Lists"" according to window size.
    # If window size is equal to zero the function calculates
    # the window by taking into account the total length of the
    # file. (minimum window = 8)
    def split_documents(self, window):

        num_of_words = len(self.terms)
        # If window is equal to zero get window according to length
        # or if percentage window flag is true
        output_list = []
        if window < 8:
            window = 8
        # join words into a window sized text
        for i in range(0, num_of_words, window):
            output_list.append(" ".join(self.terms[i:i + window]))
        return output_list


    def create_tf(self):
        tf = {}
        for term in self.terms:
            if term in tf:
                tf[term] += 1
            else:
                tf[term] = 1
        return tf

