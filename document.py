from re import findall
from os import getcwd
from os.path import exists


class Collection():
    id = -1
    def __init__(self):
        self.inv_ind ={}


    def add_to_inv_ind(self, term, tf, posting_list, NWk):
        if term not in self.inv_ind.keys():
            temp ={}
            Collection.id += 1
            temp['id'] = Collection.id
            temp['tf'] = tf
            temp['posting_list'] = posting_list
            temp['term'] = term
            self.inv_ind[term] = temp
        else:
            # print("need to update current")
            self.update_inv_index(term, tf, posting_list, NWk)
        return


    def update_inv_index(self, term, tf, posting_list, NWk):
        # get the dict -> key:value for update:
        #print(self.inv_ind[term])
        self.inv_ind[term]['tf'] += tf
        #need to check for duplicates?
        self.inv_ind[term]['posting_list'].extend(posting_list)
        return


    def write_inverted_index_to_file(self):
        pass


class Document(Collection):
    def __init__(self, path=''):
        if exists(path):
            self.path = path
            self.doc_id = int(findall(r'\d+', self.path)[0])
            self.terms = self.read_document()
            self.tf = self.create_tf()
        else:
            self.path = getcwd()
            self.doc_id = 696969
            self.terms = []
            self.tf = {}


    def read_document(self):
        try:
            with open(self.path, 'r', encoding='UTF-8') as d:
                # get all terms while checking for blanks and new lines
                return d.read().strip().split()
        except FileNotFoundError:
            raise ('File does not exist.')


    def create_tf(self):
        tf = {}
        for term in self.terms:
            if term in tf:
                tf[term] += 1
            else:
                tf[term] = 1
        return tf

    
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
        if window < 8:
            window = 8
        # join words into a window sized text
        for i in range(0, num_of_words, window):
            windowed_doc.append(self.terms[i:i + window])

        return windowed_doc

