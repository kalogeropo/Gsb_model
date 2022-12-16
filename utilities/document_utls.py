from os import makedirs
from os.path import exists


def calculate_tf(terms):
    tf = {}
    for term in terms:
        if term not in tf:
            tf[term] = 1
        elif term in tf:
            tf[term] += 1
    return tf

def create_dir(path):
    if not exists(path):
        makedirs(path)
        print("Directories Created")

