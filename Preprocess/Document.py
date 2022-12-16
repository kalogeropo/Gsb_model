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
        self.tf = calculate_tf(self.terms)

    def read_document(self):
        try:
            with open(self.path, 'r', encoding='UTF-8') as d:
                # get all terms while checking for blanks and new lines
                return [r.strip() for r in d.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError
