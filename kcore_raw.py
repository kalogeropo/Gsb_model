from math import log, sqrt
import numpy
import sys
import collections
import matplotlib.pyplot as plt
import networkx as nx
import string
from nltk.corpus import stopwords
import csv

translator = str.maketrans('', '', string.punctuation)

postinglist = []
docinfo = []
docs_without_main_core = []


# todo: more efficient way to calculate max length of path it doesnt work on realistic scale (CANT BE DONE BECAUSE THE COMPLEXITY)
# finds the maximum distance which exists in the graph
def findMaxDistance(gr, adjmatrix):
    maxlist = []
    for adi in range(len(adjmatrix)):

        for adj in range(len(adjmatrix)):

            if adj < adi:
                # cut down the number of calculated paths path(i,j) == path(j,i) so we need only the upper
                # or lower  tri of adj_matrix
                path = list(nx.shortest_simple_paths(gr, adj, adi, weight='weight'))
                print('Longest Path for (%d,%d) is: ' % (adj, adi))
                print(path[-1])
                i = 0
                weightsum = 0
                for item in range(len(path[-1]) - 1):
                    indexI = path[-1][i]
                    indexIpp = path[-1][i + 1]
                    i += 1
                    weightsum += adjmatrix[indexI][indexIpp]
                maxlist.append(weightsum)
    print(len(maxlist))
    return max(maxlist)


# finds the maximum and the minimum similarity between the nodes of the graph
def node_simi(adjmatrix):
    max = 0
    min = 1
    for adi in range(len(adjmatrix)):
        for adj in range(len(adjmatrix)):
            if adj < adi:
                temp = cos_sim(adjmatrix[adi], adjmatrix[adj])
                if temp > max:
                    max = temp
                if temp < min:
                    min = temp
    # print(max, min)
    return max, min


# ------------------Graph visualization---------------

def getGraphStats(graph, filename, graphPng, degreePng):
    if nx.is_connected(graph):
        print("IT IS CONNECTED")
    name = filename[10:]
    if graphPng:
        graphToPng(graph=graph, filename=str(name))
    if degreePng:
        plot_degree_dist(graph=graph, filename=str(name))


def plot_degree_dist(graph, *args, **kwargs):
    filename = kwargs.get('filename', None)
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color="b")

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right', fontsize=3)
    ax.set_xticklabels(deg)

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0])
    pos = nx.spring_layout(graph)
    plt.axis("off")
    nx.draw_networkx_nodes(graph, pos, node_size=20)
    nx.draw_networkx_edges(graph, pos, alpha=0.4)

    plt.savefig('figures/allq/' + str(filename) + '_degree.png', format="PNG", dpi=600)


def stopwordsStats(kcore,term_list,file):

    stopword = stopwords.words('english')
    stopword_list = [x.upper() for x in stopword]
    print(stopword)
    stopword_count = 0
    stopwords_in_file = 0
    print(len(kcore.nodes))
    print(len(term_list))

    for i in kcore.nodes:
        #print(term_list[i])
        if term_list[i] in stopword_list:
            stopword_count += 1
            #print(stopword_count)
    for i in term_list:
        if i in stopword_list:
            stopwords_in_file += 1
            #print(i)
    print(stopword_count)
    print(stopwords_in_file)
    stopwords_in_file_per = float(stopword_count/stopwords_in_file)
    stopwords_per = float(stopword_count/len(kcore.nodes))
    #print(stopwords_per)
    fw=open('stopwords_stats.txt','a')
    string_to_write = "File " + str(file) + " stopwords in kcore percentage : " + str(stopwords_per) + " and stopwords percentage in file: "+ str(stopwords_in_file_per) + "\n"
    fw.write(string_to_write)
    fw.close()
    fw=open('stopwords_kcore_stats.txt','a')
    fw.write(str(stopwords_per))
    fw.close()
    fw=open('stopwords_file_stats.txt','a')
    fw.write(str(stopwords_in_file_per))
    fw.close()


def density(A_graph):
    graph_edges = A_graph.number_of_edges()
    # print(graph_edges)
    graph_nodes = len(list(A_graph.nodes))
    # print(graph_nodes)
    dens = graph_edges / (graph_nodes * (graph_nodes - 1))
    return dens


# given points A and B it caluclates the distance of a point P from the line AB
def distance_to_line(starting_point, end_point, point):
    dist = -9999
    # spoint = (x1,y1)
    x1 = starting_point[0]
    y1 = starting_point[1]
    # end point = (x2,y2)
    x2 = end_point[0]
    y2 = end_point[1]
    # point = (x0,y0)
    print(point)
    x0 = point[0]
    y0 = point[1]
    dist = (abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y1 * x1)) / (sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2)))

    return dist


def elbow(listofpoints):
    # at first we need to create a line between first and last element
    if len(listofpoints) == 1:
        bestindex = 0
    elif len(listofpoints) == 2:
        if listofpoints[0] > listofpoints[1]:
            bestindex = 0
        else:
            bestindex = 1
    elif len(listofpoints) > 2:
        # p1 the starting point of line and p2 the last point of line
        # using that we will calulate the distance of each point of our starting list
        # from the line using the known forumla
        p1 = numpy.array([listofpoints[0], 0])
        p2 = numpy.array([listofpoints[-1], (len(listofpoints) - 1)])
        distance = []
        # print(p1,p2)
        # print(listofpoints)
        pnt = []
        for point in listofpoints:
            pnt.append(point)
            pnt.append(listofpoints.index(point) + 1)
            print(pnt)
            distance.append(distance_to_line(p1, p2, pnt))
            pnt = []
        bestdistance = max(distance)
        bestindex = distance.index(bestdistance)
    return bestindex
# test method

def average(lst):
    try:
        return sum(lst)/len(lst)
    except ZeroDivisionError:
        return 0

