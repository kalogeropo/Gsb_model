from re import findall
from os import getcwd
from os.path import exists
from utilities.document_utls import calculate_tf


class Document:
    def __init__(self, path=''):
        try:
            self.path = path
        except FileNotFoundError:
            raise FileNotFoundError
        try:
            self.doc_id = int(findall(r'\d+', self.path)[0])
        except IndexError:
            self.doc_id = 696969
            # print(self.doc_id)
        self.terms = self.read_document()
        self.docs_text = " ".join(self.terms)
        self.tf = calculate_tf(self.terms)

    def __str__(self):
        return "doc ID: " + str(self.doc_id)
        # return "doc ID: " + str(self.doc_id) + "\n Document term freq: " + str(self.tf)

    def read_document(self):
        try:
            with open(self.path, 'r', encoding='UTF-8') as d:
                # get all terms while checking for blanks and new lines
                return [r.strip().upper() for r in d.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError

    # Split documents in smaller ""Lists"" according to window size.
    # If window size is equal to zero the function calculates
    # the window by taking into account the total length of the
    # file. (minimum window = 8)
    def split_document(self, window, window_cut_off=True):

        num_of_words = len(self.terms)
        # If window is equal to zero get window according to length
        # or if percentage window flag is true
        windowed_doc = []
        """For small collections remove the next 2 lines"""
        if window < 7 and window_cut_off:
            window = 7
        # join words into a window sized text
        for i in range(0, num_of_words, window):
            windowed_doc.append(self.terms[i:i + window])

        return windowed_doc
