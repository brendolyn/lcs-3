import pyperclip

__author__ = 'urvishparikh'

import re
Infinity = float('inf')


def make_matrix(sizex, sizey):
    """Creates a sizex by sizey matrix filled with zeros."""
    return [[0]*sizey for i in xrange(sizex)]



def print_matrix(x, y, A):
    """Print the matrix with the (0,0) entry in the top left
    corner. Will label the rows by the sequence and add in the
    0-row if appropriate."""

    # decide whether there is a 0th row/column
    if len(x) == len(A):
        print "%5s" % (" "),
    else:
        print "%5s %5s" % (" ","*"),
        y = "*" + y

    # print the top row
    for c in x:
        print "%5s" % (c),
    print

    if type(A[0][0]) == float:
        for j in xrange(len(A[0])):
            print "%5s" % (y[j]),
            for i in xrange(len(A)):
                print "%5.0f" % (A[i][j]),
            print

    else:
        for j in xrange(len(A[0])):
            print "%5s" % (y[j]),
            for i in xrange(len(A)):
                print "%5s" % (A[i][j]),
            print





def main(x, y, blosum62, gapopen_penalty, gapextension_penalty):
    M = make_matrix(len(x) + 1, len(y) + 1)
    U = make_matrix(len(x) + 1, len(y) + 1)
    D = make_matrix(len(x) + 1, len(y) + 1)
    MB = make_matrix(len(x) + 1, len(y) + 1)
    UB = make_matrix(len(x) + 1, len(y) + 1)
    DB = make_matrix(len(x) + 1, len(y) + 1)
    ###
     ##   if the max value is  lower(i-1, j) - epsilon
#then backtrack-lower(i, j) = 'v' where v indicates down and 'down' we can only move in the lower matrix
#if the max value is  middle(i-1, j) - sigma
#then backtrack-lower(i, j) = '.v' where '.v' indicates a jump from the middle matrix to the lower matrix
    ###

    for i in xrange(1, len(x)+1):
        M[i][0] = gapopen_penalty + ((i-1) * gapextension_penalty)
        U[i][0] = gapopen_penalty + ((i-1) * gapextension_penalty)
        D[i][0] = -Infinity

    for i in xrange(1, len(y)+1):
        M[0][i] = gapopen_penalty + ((i-1) * gapextension_penalty)
        U[0][i] = -Infinity
        D[0][i] = gapopen_penalty + ((i-1) * gapextension_penalty)

    for i in xrange(1, len(x)+1):
        for j in xrange(1, len(y)+1):

            xi = x[i-1]
            yj = y[j-1]
            U[i][j] = max(
                    gapopen_penalty + M[i-1][j],
                    gapextension_penalty + U[i-1][j],
            )

            if U[i][j] == gapextension_penalty + U[i-1][j]:
                #gap open penalty was cheaper so made a jump
                UB[i][j] = ">"
            elif U[i][j] == gapopen_penalty + M[i-1][j]:
                #means we are already in the upper matrix and just V
                UB[i][j] = '.>'


            D[i][j] = max(
                    gapopen_penalty +  M[i][j-1],
                    gapextension_penalty + D[i][j-1]
            )

            if D[i][j] == gapextension_penalty + D[i][j-1]:
                DB[i][j] = 'v'
            elif D[i][j] == gapopen_penalty +  M[i][j-1]:
                DB[i][j] = '.v'


            M[i][j] = max(int(blosum62[x[i-1], y[j-1]]) +
                    M[i-1][j-1],
                    U[i][j],
                    D[i][j]
            )

            blosumscore = blosum62[x[i-1], y[j-1]]
            if M[i][j]== int(blosum62[x[i-1], y[j-1]]) + M[i-1][j-1]:
                MB[i][j] = "\\"
                # if x[i-1] == 'R' and y[j-1]=='R' and x[i-2]=='G' and y[j-2]=='G':
                #     print x[i]
                #     print y[j]
                #     print_matrix(x,y, MB)
                #     print "something"

                #print_matrix(x, y, MB)
            elif M[i][j]==D[i][j]:
                MB[i][j] = "v."
            elif M[i][j]==U[i][j]:
                MB[i][j] = ">."



    opt = max(M[len(x)][len(y)], U[len(x)][len(y)], D[len(x)][len(y)])
    matrixToUse = None
    if opt == M[len(x)][len(y)]:
        #startFrom M
        matrixToUse = MB
    elif opt == U[len(x)][len(y)]:
        #start from U
        matrixToUse = UB
    elif opt==D[len(x)][len(y)]:
        #start from D
        matrixToUse = DB


    refbuilder = ""
    strbuilder = ""
    i = len(x)
    j= len(y)
    while True:
        if i==0 and j==0:
            break
        if matrixToUse[i][j] == 0:
            while j>0:
                refbuilder+="-"
                strbuilder+=y[j-1]
                j-=1
            while i >0:
                strbuilder+="-"
                refbuilder+=x[i-1]
                i-=1
            break
        if matrixToUse[i][j] == ".v":

            refbuilder += "-" #deletion
            strbuilder+=y[j-1]
            matrixToUse = DB
            j-=1
        elif matrixToUse[i][j] == "v.":
            #deletionstill

            refbuilder+="-"
            strbuilder+=y[j-1]
            matrixToUse=MB
            j-=1
        elif matrixToUse[i][j] == "\\":
            #match
            refbuilder+=x[i-1]
            strbuilder+=y[j-1]
            i-=1
            j-=1
            matrixToUse = MB
            assert matrixToUse==MB, "shoulb be MB"
        elif matrixToUse[i][j] == "v":
            refbuilder+="-"
            strbuilder+=y[j-1]
            j-=1
            assert matrixToUse==DB
        elif matrixToUse[i][j] == ">":
            refbuilder+=x[i-1]
            strbuilder+="-"
            i-=1
        elif matrixToUse[i][j] == ".>":
            refbuilder+=x[i-1]
            strbuilder+="-"
            i-=1
            matrixToUse=UB
        elif matrixToUse[i][j] == ">.":
            refbuilder+=x[i-1]
            strbuilder+="-"
            i-=1
            matrixToUse=MB


    res = ""
    res += str(opt) + "\n"
    print opt
    res += strbuilder[::-1] + "\n"
    res += refbuilder[::-1] + "\n"
    print strbuilder[::-1]
    print refbuilder[::-1]
    pyperclip.copy(res)
    # print "M matrix ="
    # print_matrix(x,y,M)
    # print "U matrix ="
    # print_matrix(x,y,U)
    # print "D matrix ="
    # print_matrix(x,y,D)
    # #print opt
    # print [row for row in UB]
    # print MB
    # print DB






if __name__ == "__main__":
    ref = "ATLHWCPTGDFEVFRSPACCLDHNSMQGASTKQRGNMQHTLNIHVSIRDKLVFRRPYRSMHNKRLSPFGHNYKLFS"
    strtoalign = "ATLHWAPTGDFEVFWCHHRSTKNPTTQRIMCRGNMQHTLNRSMHNKRLSPFHHKYKLFS"
    #ref = "AACCTTGG"
    #strtoalign = "ACACTGTGA"
    i = 0
    cols = []
    blosum62 = dict()
    with open("BLOSUM62.txt") as f:
        for line in f:
            line = line.strip()

            if i == 0:
                split_line = line.split("  ")
                cols = split_line

            else:
                p = re.compile(r'\s*')
                split_line  = p.split(line)
                indexer = split_line[0]
                for num, col in  (zip(split_line[1:], cols)):
                    blosum62[(indexer, col)] = num
            i = i + 1
    #test = {("A", "B"): 1, ("B","A"): 2}
    #print test[("A", "B")]
    #print test["B", "A"]
    #print blosum62
    main(strtoalign,ref, blosum62, -11, -1)

