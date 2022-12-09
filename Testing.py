
from utilities import parser

test = parser()
test.load_collection("CF")
print(len(test.queries))
print(len(test.relevant))

