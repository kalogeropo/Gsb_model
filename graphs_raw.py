import nltk
import numpy


##############################################################################################################################
### PART 1: NIKOLAOS SKAMNELOS usefull graph functions:

#CREATES a graph using a fixed sized window, by spliting the original textfile into sub-textfiles
# Split File in smaller files according to window size.
# If window size is equal to zero the function calculates
# the window by taking into account the total length of the
# file. (minimum window = 5)
def splitFileConstantWindow(file, window, per_window):
    # Open the file and split it into words
    inputFile = open(file, 'r').read().split()
    num_of_words = len(inputFile)
    outputFile = []

    # If window is equal to zero get window according to length or if percentage window flag is true
    if window == 0:
        # print(per_window)
        window = int(num_of_words * per_window) + 1
        # print("Window Size: ", window)
        if window < 14:
            window = 14

    # Join words according to window
    for i in range(0, num_of_words, window):
        outputFile.append(' '.join(inputFile[i:i + window]))

    # print(outputData)
    return outputFile



def CreateAdjMatrixFromInvIndexWithWindow(terms, file, window_size, per_window, dot_split):
    # print("Adj_Matrix = %d * %d " % (len(terms), len(tf)))
    # print(terms)
    adj_matrix = numpy.zeros(shape=(len(terms), len(terms)))
    tfi = 0
    if dot_split:
        inputFile = open(file, 'r').read()
        split_file = nltk.tokenize.sent_tokenize(inputFile, language='english')
    else:
        split_file = splitFileConstantWindow(file, window_size, per_window)
    for subfile in split_file:
        window_terms = subfile.split()
        for term in window_terms:
            # print("\n")
            # print(term)
            row_index = terms.index(term)
            # print("TERM:",row_index)
            for x in range(0, len(window_terms)):
                col_index = terms.index(window_terms[x])
                # print("Y TERM:",col_index)
                if col_index == row_index:
                    tfi += 1
                else:
                    adj_matrix[row_index][col_index] += 1
            adj_matrix[row_index][row_index] += tfi * (tfi + 1) / 2
            tfi = 0

    # pen_adj_mat = applyStopwordPenalty(adj_matrix, terms)
    # print(adj_matrix)
    # fullsize = rows.size + row.size + col.size + adj_matrix.size
    # print(fullsize / 1024 / 1024)
    return (adj_matrix)


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
