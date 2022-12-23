import os
from time import time

# timelist_perc = []
#
# for per in range(1,11,2):
#     start = time()
#
#     perc =per/100
#     os.system(f'python parser.py --test_name GSBperc_{per} --Model index-constant --Parameters {perc} --path CF' )
#     os.system(f'python parser.py --test_name GSBperc_{per} --Model graph-ext_min_tf --Parameters 2 --path CF')
#     end = time()
#     time_dif = end - start
#     timelist_perc.append(int(time_dif))
#
# timelist_constant =[]
# for per in [5,8,10,12,14,15,16,18,22]:
#     start = time()
#
#     #perc =per/100
#     os.system(f'python parser.py --test_name GSBpecParams{per} --Model index-constant --Parameters {per} --path CF' )
#     os.system(f'python parser.py --test_name GSBpecParams{per} --Model graph-ext_min_tf --Parameters 1 --path CF')
#     end = time()
#     time_dif = end - start
#     timelist_constant.append(int(time_dif))

#########-------------------->1
timelist_gsb=[]
os.system('python parser.py --test_name con_wind_10 --Model index-constant --Parameters 10 --path CF' )
for min_supp in range(1,33):
    start = time()
    os.system(f'python parser.py --test_name con_wind_10 --Model graph-ext_min_tf --Parameters {min_supp} --path CF')
    end = time()
    time_dif = end-start
    timelist_gsb.append(int(time_dif))

#print(list(zip(list(range(30,50)),timelist)))

timelist_set_b=[]
os.system('python parser.py --test_name con_wind_10 --Model index-constant --Parameters 10 --path CF' )
for min_supp in range(1,33):
    start = time()
    os.system(f'python parser.py --test_name con_wind_10 --Model set-based_min_tf --Parameters {min_supp} --path CF')
    end = time()
    time_dif = end-start
    timelist_set_b.append(int(time_dif))


#print(f"time in secs for indexing and retieval of perc_GSB with [1,10,2]% = {timelist_perc}")
#print(f"time in secs for indexing and retieval of constant_GSB with [5,8,10,12,14,15,16,18,22]% = {timelist_constant}")
print(f"time in secs for indexing and retieval of Constant_GSB with dif support = {timelist_gsb}")
print(f"time in secs for indexing and retieval of GSB with dif support = {timelist_set_b}")

"""-------------------tests-------------------------- 




------------------------------------------times
[1,33]
time in secs for indexing and retieval of Constant_GSB with dif support = 
[30, 26, 28, 27, 27, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 28, 26, 26, 25, 26, 25, 25, 25, 26, 26, 25, 25, 28, 26, 25, 28, 26]

time in secs for indexing and retieval of GSB with dif support = 
[31, 27, 28, 27, 27, 26, 26, 27, 27, 27, 26, 26, 26, 27, 27, 27, 26, 26, 26, 26, 26, 25, 25, 26, 25, 26, 26, 25, 26, 26, 26, 26]
"""