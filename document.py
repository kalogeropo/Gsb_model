from re import findall
from os import getcwd
from os.path import exists
from retrieval import calculate_tf


class Document():
    def __init__(self, path=''):
        if exists(path):
            self.path = path
            self.doc_id = int(findall(r'\d+', self.path)[0])
            self.terms = self.read_document()
            self.tf = calculate_tf(self.terms)


    def read_document(self):
        try:
            with open(self.path, 'r', encoding='UTF-8') as d:
                # get all terms while checking for blanks and new lines
                return [r.strip() for r in d.readlines()]
        except FileNotFoundError:
            raise ('File does not exist.')

    
    def set_terms(self, terms):
        self.terms = terms
        return self
        

    # Split documents in smaller ""Lists"" according to window size.
    # If window size is equal to zero the function calculates
    # the window by taking into account the total length of the
    # file. (minimum window = 8)
    def split_document(self, window):

        num_of_words = len(self.terms)
        # If window is equal to zero get window according to length
        # or if percentage window flag is true
        windowed_doc = []
        if window < 7:
            window = 7
        # join words into a window sized text
        for i in range(0, num_of_words, window):
            windowed_doc.append(self.terms[i:i + window])

        return windowed_doc

