import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

with open('data/Queries.txt', encoding='UTF-8') as f:
    queries = [q.split() for q in f.readlines()]


te = TransactionEncoder()
te_ary = te.fit_transform(queries)

df = pd.DataFrame(te_ary, columns=te.columns_)

print(apriori(df, min_support=0.5, use_colnames=True))