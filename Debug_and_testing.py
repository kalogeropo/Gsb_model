import time
from os import listdir
from os.path import join

from networkx import info, draw, draw_networkx_labels, spring_layout

from models.DocGraph import DocGraph
from models.GSB import GSBModel
from models.GoW import Gow
from models.WindowedGSB import WindowedGSBModel
from models.borda_count import BordaCount
from models.ΒΜ25 import BM25Model
from utilities.Result_handling import res_to_excel, expir_start, write
from models.onlineGSB import onlineGSB, profile_create_or_update_graph_index
import matplotlib.pyplot as plt

from utilities.document_utls import json_to_dat

#CF
path = 'experiments/collections/CF/docs'
path_to_write = 'Gsb_model/data/test_docs/tests'
col_path = 'experiments/collections/CF'
dest_path = "experiments/paper_results"

#path = "C:/Users/nrk_pavilion/PycharmProjects/Gsb_model/experiments/collections/baeza/docs"
testcol, q, r = expir_start(path, path_to_write, col_path)
print(type(testcol))
N = DocGraph(testcol)
print(testcol.inverted_index)

print(N.get_model())
# N.fit()
# N.evaluate()

# test = onlineGSB(path,name="sad")
# test.create_or_update_graph_index()
# Assuming 'instance' is an instance of the class containing the create_or_update_graph_index method
# # And you want to profile it with a specific set of filenames
# profile_result = profile_create_or_update_graph_index(test)
#
# # Print the result
# print(profile_result)

# print(test.num_docs)
# lab ={}
# for node,data in test.union_graph.nodes(data=True):
#     lab.update({node:data})
#
# pos = spring_layout(test.union_graph)  # Positions for all nodes
#
# plt.figure(figsize=(10,10))
# draw(test.union_graph,with_labels=True,pos=pos, node_size=2000, node_color="skyblue", font_size=15, font_weight="bold")
# offset_pos = {node: (coords[0], coords[1] + 0.05) for node, coords in pos.items()}
# draw_networkx_labels(test.union_graph,labels=lab,font_size=13,pos=offset_pos)
# # Set title
# plt.title("Union Graph with Node Labels")
#
# # Save the figure
# plt.savefig("graph_with_labels.png", format="png")
# plt.show()

# testing = []
# path = "C:/Users/nrk_pavilion/PycharmProjects/Gsb_model/experiments/collections/CF/docs"
# filenames = [join(path, id) for id in listdir(path)]
# test = onlineGSB(path,name="sad")
# for i in range(0, len(filenames),200):
#     starting_time = time.time()
#     test.create_or_update_graph_index(filenames[i:i+200])
#     end_time = time.time()
#     elapsed_time = end_time - starting_time
#     testing.append(elapsed_time)
#     print(test.union_graph)
# print(testing)


#NPL
# path = 'experiments/collections/NPL/docs'
# path_to_write = 'experiments/temp'
# col_path = 'experiments/collections/NPL'
# dest_path = "experiments/paper_results/NPL_results"
# print(q)
# print(len(testcol.inverted_index))

# testing = []
# sorting_by =[]
# path_col = 'C:/Users/nrk_pavilion\PycharmProjects\Gsb_model\experiments\collections\Cf_splited'
# folders = listdir(path_col)
# for folder in listdir(path_col):
#     starting_time = time.time()
#     path = join(path_col, folder)
#     sorting_by.append(folder)
#     testcol, q, r = expir_start(path, path_to_write, col_path)
#     N = GSBModel(testcol)
#     testcol.save_inverted_index('C:/Users/nrk_pavilion\PycharmProjects\Gsb_model\experiments/temp')
#     end = time.time()
#     testing.append(end-starting_time)
# print(sorting_by)
# print(testing)


# path = "C:/Users/nrk_pavilion\PycharmProjects\Gsb_model\experiments\collections/NPL\docs"
# start = time.time()
# test = onlineGSB(path,name="sad")
# starting_time = time.time()
# test.create_or_update_graph_index()
# end = time.time()
# elapsed = end - start
#
# print("onlineGSB: Elapsed Time: " + str(elapsed))
#
# testcol, q, r = expir_start(path, path_to_write, col_path)
# N = GSBModel(testcol)
# print("GSB: Elapsed Time: " + str(N.elapsed_time))
#
# testcol, q, r = expir_start(path, path_to_write, col_path)
# N = WindowedGSBModel(testcol,4)
# print("Windowed GSB: Elapsed Time: " + str(N.elapsed_time))

#print(testcol.inverted_index)
#testcol.collection_to_tsv(qrel=True,create_triplets=True,triplet_filename="debug_with_neg.tsv")

# for i,q in enumerate(testcol.queries):
#     print(i, " ".join(q)," ".join(q), "1" )
#     with open("debug.tsv", "a") as fd:
#         fd.write(f"{' '.join(q)}\t{' '.join(q)}\t{' '.join(q)}\n")


#df = testcol.q_r_stats()
#write(xl_namefile='example.xlsx', dest_path="experiments/paper_results", sheetname="cf_queries", data=df)

# testcol, q, r = expir_start(path, path_to_write, col_path)
# N = GSBModel(testcol)
# json_to_dat(testcol, "complete_index.dat")
# print(N.get_model())
# N.fit()
# N.evaluate()

# df = M.results_to_df()
# print(len(N.ranking))
# df = N.results_to_df()
# write(xl_namefile='example.xlsx', dest_path="experiments/paper_results", sheetname="cf_supp_1", data=df)

# testbm25 = BM25Model(testcol)
# testbm25.fit()
# testbm25.evaluate()
#print(testbm25.precision)

# testing = Gow(testcol)
# testing.fit()
# testing.evaluate()
# print(len(testing.ranking))
# df = testing.results_to_df()
# write(xl_namefile='example.xlsx', dest_path="experiments/collections/test", sheetname="test2", data=df)

# bord = BordaCount(testbm25.ranking, N.ranking, testcol)
# bord.fit()
# bord.evaluate()
# res_to_excel(bord,"[cf]Bm25_windows7.xlsx",dest_path,sheetname="bm25_win7")

#M
#res_to_excel(M,"testM.xlsx",dest_path,sheetname="test13")
# #N
# res_to_excel(N,"testN.xlsx",dest_path,sheetname="test16")
# #bord
# res_to_excel(bord,"testBord.xlsx",dest_path,sheetname="test13_16")
