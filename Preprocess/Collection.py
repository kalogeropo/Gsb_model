from json import dumps
from os.path import join
from os import listdir, getcwd, path

from Preprocess.Document import Document
from utilities.document_utls import create_dir


class Collection:
    """ A collection of documents consisted of:

            - path - collection path in disk/project
            - num_docs - the number of documents in the collection
            - docs [] - a list of document ids
            - params {} - some parameters used in ir models (such as window_size ... etc)
            - inv_index {} - a dictionary of inverted indexed terms consisted of
                    'id',
                    'total_tf',
                    'posting_list': [[doc.doc_id, tf]],
                    'term': term
                    *** these depending on the model might be altered or augmented with more information.
    """

    def __init__(self, path, docs=[],name=''):
        self.relevant = None
        self.queries = None
        self.name = name
        self.path = join(getcwd(), path)

        self.num_docs = len(listdir(self.path))

        # can be used to hold different user given information
        self.params = {}

        # List of Document object of each document
        self.docs = docs

        # inverted index
        self.inverted_index = {}

    def create_collection(self):
        if not self.docs:
            # generate file names
            filenames = [join(self.path, id) for id in listdir(self.path)]
            # print(filenames)
            for fn in filenames:
                if not path.isdir(fn):
                    self.docs.append(Document(fn))
            # Create inverted index
            # --->Debug
            # for doc in self.docs:
            #    print(doc.tf)
            self.inverted_index = self.create_inverted_index()
            self.num_docs = self.docs[-1].doc_id

    def create_inverted_index(self):
        inv_index = {}
        id = 0
        error_counter = 0
        try:
            for doc in self.docs:
                for term, tf in doc.tf.items():
                    if term not in inv_index:
                        inv_index[term] = {
                            "id": id,
                            "total_tf": tf,
                            "posting_list": [[doc.doc_id, tf]],
                            "term": term
                        }
                        id += 1
                    elif term in inv_index:
                        inv_index[term]['total_tf'] += tf
                        inv_index[term]['posting_list'] += [[doc.doc_id, tf]]
        except KeyError:
            error_counter += 1
            print(f"Keys not found {error_counter}")
        return inv_index

    def save_inverted_index(self, path=''):
        if not path:
            path=self.path
        print(path)
        create_dir(path)
        with open("".join([path, f'\inverted_index_{self.name}.json']), 'w', encoding='UTF-8') as inv_ind:
            if self.inverted_index:
                inv_ind.write(dumps(self.inverted_index))
            else:
                raise ("Inverted Index Empty.")

    def load_collection(self,coll_path= ''):
        if path.exists(coll_path):
            for item in listdir(coll_path):
                if item == "Queries.txt":
                    with open("".join([coll_path, "/Queries.txt"]), "r") as fd:
                        self.queries = [q.upper().split() for q in fd.readlines()]
                if item == "Relevant.txt":
                    with open("".join([coll_path, "/Relevant.txt"]), "r") as fd:
                        self.relevant = [[int(id) for id in d.split()] for d in fd.readlines()]
        else: print("path issue")
        return self.relevant, self.queries
