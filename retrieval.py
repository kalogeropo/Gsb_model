import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

with open('data/Queries.txt', encoding='UTF-8') as f:
    queries = [q.split() for q in f.readlines()][:1]

with open('data/Relevant.txt', encoding='UTF-8') as f:
    docs = [d.split() for d in f.readlines()][:1]

te = TransactionEncoder()
te_ary = te.fit_transform(docs)

print(te_ary)
df = pd.DataFrame(te_ary, columns=te.columns_)

print(apriori(df, min_support=0.2, use_colnames=True))

############################ FOR INVERTED INDEX ###################################
""" 
docs = []
for query in queries:
    for term in query:
        d  = [id for id, tf in inv_index[term]['posting_list']]
        docs.append(d)

print(docs)

te = TransactionEncoder()
te_ary = te.fit_transform(docs)
print(te_ary)
df = pd.DataFrame(te_ary, columns=te.columns_)

print(apriori(df, min_support=0.2, use_colnames=True))
"""
