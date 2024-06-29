import random
from _csv import writer
from json import dumps
from os.path import join, exists
from os import listdir, getcwd, path

import nltk

from Preprocess.Document import Document
from utilities.document_utls import create_dir, remove_punctuation, write_to_tsv
from pandas import DataFrame


def update_index(document, inv_index):
    id = len(inv_index)
    for term, tf in document.tf.items():
        if term not in inv_index:
            inv_index[term] = {
                "id": id,
                "total_tf": tf,
                "posting_list": [[document.doc_id, tf]],
                "term": term
            }
            id += 1
        elif term in inv_index:
            inv_index[term]['total_tf'] += tf
            inv_index[term]['posting_list'] += [[document.doc_id, tf]]
    return inv_index


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

    def __init__(self, path, docs=None, name=''):
        if docs is None:
            docs = []
        self.relevant = None
        self.queries = None
        self.name = name
        self.path = join(getcwd(), path)

        if exists(self.path):
            self.num_docs = len(listdir(self.path))
        else:
            print(self.path)
            # create_dir(self.path)
        # can be used to hold different user given information
        self.params = {}

        # List of Document object of each document
        self.docs = docs

        # inverted index
        self.inverted_index = {}

    def create_col_from_list(self, dict_of_docs, preproccess=False, list_of_q=None, list_of_rel=None, coll_path=None):
        for doc in dict_of_docs:
            # print(doc['doc_id'])
            with open("".join([self.path, '/', str(doc['doc_id']), '.txt']), 'w', encoding='UTF-8') as fd:
                doc_to_write = doc['text']
                if preproccess:
                    doc_to_write = remove_punctuation(doc_to_write).upper().split(" ")
                    # print(doc_to_write)
                fd.write('\n'.join(doc_to_write))

            # create txts

        if list_of_rel is None:
            list_of_rel = []
        else:
            # print(list_of_rel)
            with open("".join([coll_path, "/Relevant.txt"]), 'w', encoding='UTF-8') as fd:
                for item in list_of_rel:
                    fd.write(' '.join(str(i) for i in item))
                    fd.write('\n')
        if list_of_q is None:
            list_of_q = []
        else:
            with open("".join([coll_path, "/Queries.txt"]), 'w', encoding='UTF-8') as fd:
                fd.write("\n".join(list_of_q))
        return 0

    def create_collection(self):
        self.num_docs = 0
        if not self.docs:
            # generate file names
            # print(listdir(self.path))
            filenames = [join(self.path, id) for id in listdir(self.path)]
            #print(filenames)
            max_id = max([int(id) for id in listdir(self.path)])
            self.num_docs = int(max_id)
            print(self.num_docs)
            # print(filenames)
            self.add_batch_docs(filenames)

            # Create inverted index
            # --->Debug
            # for doc in self.docs:
            #    print(doc.tf)
            self.inverted_index = self.create_inverted_index()

    def add_batch_docs(self, filenames):
        for fn in filenames:
            update_index(Document(fn),self.inverted_index)
            self.docs.append(Document(fn))

    def create_inverted_index(self):
        inv_index = {}
        error_counter = 0
        try:
            for doc in self.docs:
                update_index(doc, inv_index)
        except KeyError:
            error_counter += 1
            print(f"Keys not found {error_counter}")
        return inv_index

    def save_inverted_index(self, path=''):
        if not path:
            path = self.path
        print(path)
        create_dir(path)
        with open("".join([path, f'\inverted_index_{self.name}.json']), 'w', encoding='UTF-8') as inv_ind:
            if self.inverted_index:
                inv_ind.write(dumps(self.inverted_index))
            else:
                raise ("Inverted Index Empty.")

    def load_collection(self, coll_path=''):
        if path.exists(coll_path):
            for item in listdir(coll_path):
                if item == "Queries.txt":
                    with open("".join([coll_path, "/Queries.txt"]), "r") as fd:
                        self.queries = [q.upper().split() for q in fd.readlines()]
                if item == "Relevant.txt":
                    with open("".join([coll_path, "/Relevant.txt"]), "r") as fd:
                        self.relevant = [[int(id) for id in d.split()] for d in fd.readlines()]
        else:
            print("path issue")
        return self.relevant, self.queries

    def q_r_stats(self):
        from nltk.corpus import stopwords
        try:
            stop_words = set(stopwords.words('english'))
        except LookupError:
            import nltk
            nltk.download('stopwords')
            stop_words = set(stopwords.words('english'))

        df = DataFrame(columns=["Q", "R", "Q_size", "rel_list_size", "No_of_stop", "Core Q len"])
        for i, (q, r) in enumerate(zip(self.queries, self.relevant)):
            filtered_sentence = [w for w in q if not w.lower() in stop_words]
            df.loc[i] = (
                {"Q": ' '.join(q), "R": " ".join(map(str, r)), "Q_size": len(q), "rel_list_size": len(r),
                 "No_of_stop": len(q) - len(filtered_sentence),
                 "Core Q len": len(filtered_sentence)})
        return df

    def collection_to_tsv(self, create_triplets=False, qrel=False, docs_filename="docs.tsv",
                          query_filename="Queries.tsv",
                          triplet_filename="triplets.tsv", qrel_filename="Qrels.tsv"):
        # self.docs_to_tsv(docs_filename)
        # self.queries_to_tsv(query_filename)
        if create_triplets:
            self.debug_triplets_generate(triplet_filename)
        if qrel:
            self.qrels_to_tsv(qrel_filename)
        return 1

    def docs_to_tsv(self, filename):
        open(filename, 'w').close()
        for doc in self.docs:
            data = [doc.doc_id, doc.docs_text]
            write_to_tsv(data, filename)
        return 1

    def qrels_to_tsv(self, qrel_filename):
        for q_text in self.queries:
            qid = self.queries.index(q_text)
            rels = self.relevant[qid]
            for r in rels:
                data = [f"<query ID,{qid},passage ID,{r}>"]
                print(f" <query ID,{qid},passage ID,{r}>\n")
                write_to_tsv(data, qrel_filename)

    def queries_to_tsv(self, filename):
        open(filename, 'w').close()
        for i, q in enumerate(self.queries):
            data = [i, " ".join(q)]
            write_to_tsv(data, filename)
        return 1

    def triplets_generate(self, filename):

        for q_text in self.queries:
            qid = self.queries.index(q_text)
            relevants = self.relevant[qid]
            stop_counter = 1  # int(len(relevants) / 2)
            rel_text = []
            negative_sample = []
            for r in relevants:
                random_negative_id = random.randrange(1, self.num_docs)
                while random_negative_id in relevants:
                    random_negative_id = random.randrange(1, self.num_docs)
                rel_text.append(self.docs[r].docs_text)
                negative_sample.append(self.docs[random_negative_id].docs_text)
                stop_counter -= 1
                if stop_counter <= 0: break
            print(f"{qid} \t {len(relevants)}\t {len(rel_text)}\t{len(negative_sample)}\n")
            for i in range(len(negative_sample)):
                data = [" ".join(q_text).lower(), rel_text[i].lower(), negative_sample[i].lower()]
                write_to_tsv(data, filename)

    def debug_triplets_generate(self, filename):
        for q_text in self.queries:
            qid = self.queries.index(q_text)
            relevants = self.relevant[qid]
            stop_counter = 1  # int(len(relevants) / 2)
            rel_text = []
            negative_sample = []
            for r in relevants:
                random_negative_id = random.randrange(1, self.num_docs)
                while random_negative_id in relevants:
                    random_negative_id = random.randrange(1, self.num_docs)
                rel_text.append(q_text)
                negative_sample.append(self.docs[random_negative_id].docs_text)
                stop_counter -= 1
                if stop_counter <= 0: break
            print(f"{qid} \t {len(relevants)}\t {len(rel_text)}\t{len(negative_sample)}\n")
            for i in range(len(negative_sample)):
                data = [" ".join(q_text).lower(), " ".join(q_text).lower(), negative_sample[i].lower()]
                write_to_tsv(data, filename)
