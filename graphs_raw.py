import nltk
import numpy

def graphToIndex(id, terms, calc_term_w, plist, *args, **kwargs):
    filename = kwargs.get('filename', None)
    if not filename:
        filename = 'inverted index.dat'
    f = open(filename, "a+")
    data = ','.join(
        [str(i) for i in plist])  # join list to a string so we can write it in the inv index and load it with ease
    f.write('%d;%s;%f;%s;\n' % (id, terms, calc_term_w, data))
    f.close()
    return 1



# calculating the weight and write the inverted index file using graphToIndex method
# NO USE
def w_and_write_to_file(listofdeg, Umatrix, collection_terms, union_graph_termlist_id, collection_term_freq):
    print('here')
    for i in range(len(listofdeg[0])):
        Wout = listofdeg[0][i]
        Win = collection_term_freq[i]
        nbrs = numpy.count_nonzero(Umatrix[i])
        VarA = 1
        VarB = 10
        Alog = 1 + VarA * ((Wout / (nbrs + 1)) / (Win + 1))
        Blog = 1 + VarB * (1 / (nbrs + 1))
        temp = log(Alog) * log(Blog)
        print(temp)

        indexofw = postinglist.index(collection_terms[i])  # maybe not the best way of implementing the
        graphToIndex(union_graph_termlist_id[i], collection_terms[i], temp, postinglist[indexofw + 1])
    return 1

    #plt.savefig('figures/allq/' + str(filename) + '.png', format="PNG", dpi=600)
##############################################################################################################################
### PART 1: NIKOLAOS SKAMNELOS usefull graph functions:

# The idea behind this function is to get two adjacency matrices(one for sentences and one for paragraphs)
# using CreateAdjMatrixFromInvIndexWithWindow and then combine them into a single matrix using two weight
# coefficients a and b, which will determine the importance of each matrix.
def CreateAdjMatrixFromInvIndexWithSenParWindow(terms, file, sen_window_size, par_window_size, dot_split):
    matrix_size = len(terms)

    # Create the matrices
    sen_adj_matrix = numpy.zeros(shape=(matrix_size, matrix_size,))
    par_adj_matrix = numpy.zeros(shape=(matrix_size, matrix_size))

    # Get the adjacency matrix for each window
    sen_adj_matrix = CreateAdjMatrixFromInvIndexWithWindow(terms, file, sen_window_size, 0, dot_split)
    par_adj_matrix = CreateAdjMatrixFromInvIndexWithWindow(terms, file, par_window_size, 0, dot_split)

    # Create the final Matrix
    final_adj_matrix = numpy.zeros(shape=(matrix_size, matrix_size))

    # Create coefficients a and b
    a = 1.0
    b = 0.05

    # Add the two matrices
    final_adj_matrix = [[a * sen_adj_matrix[r][c] + b * par_adj_matrix[r][c] for c in range(len(sen_adj_matrix[0]))] for
                        r in range(matrix_size)]
    # print(final_adj_matrix)

    return final_adj_matrix




#here the graph is created using a overlapping sliding window as Graph of word dictates
def CreateAdjMatrix_Vazirgiannis_implementation(terms, file, window_size):
    # print("Adj_Matrix = %d * %d " % (len(terms), len(tf)))
    #print(terms)
    adj_matrix = numpy.zeros(shape=(len(terms),len(terms)))
    split_file = open(file, 'r').read().split() #splitFileConstantWindow(file, window_size)
    counter = 0
    for term in split_file:
        row_index = terms.index(term)
        for x in range(0, window_size):
            try:
                col_index = terms.index(split_file[counter + x])
                adj_matrix[row_index][col_index] += 1
            except IndexError:
                break
        counter+=1
        adj_matrix[row_index][row_index]-=1

    return (adj_matrix)
########################################################################################################################
######### PART 2:KALOGEROPOULOS graph creation proccess and usefull graph functions


# computes the degree of every node using adj matrix
def Woutdegree(mat):
    list_of_degrees = numpy.sum(mat, axis=0)
    list_of_degrees = numpy.asarray(list_of_degrees)
    id = []
    # print(list_of_degrees)
    # print(numpy.size(list_of_degrees))
    for k in range(numpy.size(list_of_degrees)):
        id.append(k)
        list_of_degrees[k] -= mat[k][k]
    list_of_degrees.tolist()
    return list_of_degrees, id


def sortByDegree(val):
    return val[0]


# deletes by re drawing the graph edges of the graph given a minimum weight !needs fix but dont work
def pruneGraphbyWeight(aMatrix, termlist, S):
    print('pruning the graph')
    temp = Woutdegree(aMatrix) #[list of weight sums of each node]
    maxval = (sum(temp[0]) / (len(temp[0]) * len(temp[0]))) #avarage weight of node
    #maxval = (maxval * (+0.5)) + maxval #average weight of
    gr = nx.Graph()
    for i in range(len(aMatrix)):
        gr.add_node(i, term=termlist[i])
        for j in range(len(aMatrix)):
            if i > j:
                if aMatrix[i][j] >=  S * maxval: #S is the persentage of the allowed weight based on maxval
                    # print("i = %d j=%d weight  = %d" % (i, j, aMatrix[i][j]))
                    gr.add_edge(i, j, weight=aMatrix[i][j])
                elif maxval < 1:
                    gr.add_edge(i, j, weight=1)#used because we had implemented a precentange on average
    return (gr)
