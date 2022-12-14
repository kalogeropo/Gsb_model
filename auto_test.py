import os
from time import time

timelist = []

#########-------------------->1
os.system('python parser.py --test_name apriori --Model index-constant --Parameters 0.05 --path CF' )
for min_supp in range(1,10):
    start = time()
    os.system(f'python parser.py --test_name apriori --Model graph-ext_sum_tfs --Parameters {min_supp} --path CF')
    os.system(f'python parser.py --test_name apriori --Model set-based_sum_tfs --Parameters {min_supp} --path CF')
    end = time()
    time_dif = end-start
    timelist.append(time_dif)

print(zip(list(range(1,10)),timelist))



"""-------------------tests-------------------------- 
1. influence of min support on apriori: min_sup[1,10] Model: index-constant Parameters:0.05 Collection: CF'

"""