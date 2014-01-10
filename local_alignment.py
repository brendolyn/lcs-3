__author__ = 'mansi'
import numpy
import re


import sys
sys.setrecursionlimit(10000)


def main(ref, stralign, pam250, indelcost):
    matrix = numpy.zeros((len(ref) + 1, len(stralign)+ 1))
    path_taken = numpy.zeros((len(ref) + 1, len(stralign)+ 1))
    #0 is null
    #1 is down
    #2 is right
    #3 is diag
    #for i  in range(0, matrix.shape[0]):
    #    matrix[i][0] = i * -indelcost
    #
    #for i in range(0, matrix.shape[1]):
    #    matrix[0][i] = i * -indelcost

    for i in range(0, path_taken.shape[0]):
        path_taken[i][0] = 1

    for i in range(0, path_taken.shape[1]):
        path_taken[0][i] = 2
    #print matrix.shape[1]
    #print matrix.shape
    for i in range(1,matrix.shape[0]):
        for k in range(1, matrix.shape[1]):

            #if ref[k -1] == stralign[i-1]:
            #    matrix[i][k] = max(matrix[i - 1][k -1] + 1, matrix[i -1][k]-indelcost, matrix[i][k-1]-indelcost)
            #    if matrix[i][k] == matrix[i - 1][k -1] + 1:
            #        path_taken[i][k] = 3
            #    if matrix[i][k] == matrix[i-1][k] - indelcost:
            #        path_taken[i][k] = 1
            #    if matrix[i][k] == matrix[i][k-1] - indelcost:
            #        path_taken[i][k] = 2
            #else:
            matrix[i][k] = max(0, matrix[i -1][k]-indelcost, matrix[i][k-1]-indelcost, matrix[i-1][k-1] +int(pam250[(ref[i-1], stralign[k-1])]))
            if matrix[i][k] == matrix[i-1][k] - indelcost:
                path_taken[i][k] = 1
            if matrix[i][k] == matrix[i][k-1] - indelcost:
                path_taken[i][k] = 2
            if matrix[i][k] == matrix[i-1][k-1] +int(pam250[(ref[i-1], stralign[k-1])]):
                path_taken[i][k] = 3

    #print matrix
    print int(matrix.max())
    maxidx = numpy.where(matrix==matrix.max())

    maxidx =  (maxidx[0][0], maxidx[1][0])
    i = maxidx[0]
    j = maxidx[1]
    strres = ""
    refres  = ""
    while True:
        if (i == 0 and j==0):
            break
        if (matrix[i][j] == 0):
            break
        if matrix[i -1][j] - indelcost == matrix[i][j]:
            ##moved down
            i=i-1
            strres = "-"+strres
            refres = ref[i] + refres
        elif matrix[i][j-1] - indelcost == matrix[i][j]:
            ##moved right
            j=j-1
            strres = stralign[j] + strres
            refres = "-" + refres

        else:
            i = i-1
            j= j-1
            strres = stralign[j]+strres
            refres = ref[i] + refres

    print refres
    print strres


if __name__ == "__main__":
    ref = "WLTTTKEWTRVCVWCNMNPASNYNYFEGWPEPDCELMEVCKHYPCRECAEDCHWNICLPSEKFNEDVDDGMTDRSWMISREAMNMSIYPGPYNIYTSPSMDHAVGKVFVSIYQARLQATFPGIHIIWNNHNCIQKLWDPVSAMMDVVNHICNWYIAWVWMFANRWGTHCTWYLIEHHQTVMKLTFYEVWTSRCVDANVSMIERHPKTRYPPNMWSNNLGAMYHESCCVRMTEVNETHRCYKSGQLAGIREKEGRWNEWVGAVAHHCILHKEFTNPDISSWCMEDIIPQDLGWDLRACAHQDFEQEPKLCVWIRAYRYPACHHESTVPRQCIFTAKMQDPHQSMTYRKCGRRSGTFCPTTERWWCNNPTTIVYEGTENYETFFVTVNGRVWYRIERKSVREKNVLESLSNFTTYYPGPCAHITSRHVDNLVFMDKLGVFYCTGDDTEWLNLIHKAEPSNMCSHKRVEGRDHVEINNCQVCPNHNSIAEDIKHFPRQWECDGFVNRSECSGVIFHGFCCQVGANYLKGDHPCDVCQHKLLHATVLEHCTWRFCPNYTPTMDDCACCYQICMHSADDSKRVNKVCLSVMPWTCAKKCLGNPVFWERYERNKGQTTCMPEPNYMSPIWQGDMPDTTIEYKMHYFTQQMEWYYWQNARGCWLIPVGDCPCKGWFVMSPLISERWPMFNSEVSPRIFQVVIQNIGTNIRWHHRKWITSIRCEVTPSHEYLLTICFGQHAELMWWRDTHLTPGDDYMWKQITFNWFKDYAVKLCCHAHVLFMVVCAVYQENLVGIQYICKLCHQCKTKVWAFKMPHRCTPPWDEWQMTWNLMTDHMQNECFLLWMCNHGHWETHEWFGHAQQQRKSPDVDRNKTVRFRAMTTPCRDMNLWQKCGFEFKCCMTMGFDQ"
    strtoalign = "YIICADQMVFYYLPLPHMACFIQSNDYWSNIHDMIIGDYPRFEIHYHTSNFLPLHEPQMGKYDEFCKHSLIDGTMMTELMQCTHYRGRTDTAARCSIHWDLAMRYPTRKEETGSNPRKPMRACGTSPCHGYRAIKVGIRHEEFWCIPVTFTQQRNPENDKYWDYDMYIRYQMFAFTYNCMPDQKKAMTHHAGSIGVNCCSNAVRQQKTRTDWWAIMTVALNVLHCLVFMPVFRCYTTRVWAPSSMGHDKRMGSLKFNMGGWSYHNKAFFGCKRQQSIQLAGIRSKEGRWNLEVSWPWVVANAHHNTLNFAILHYEIYSSDLGWDLRAFAHQDFEQEPKLCVWIRAHRNVRRRYPAQKFHQTEAKGIESTKIFTAKMLAPHQSMTYRKHGRRVTHGTPGPTTERWWCNNPTTITFFVETWEIWGPTVNKQTWYMLRYRVWYRIERVNFTTMYPGPCAHGTSRHVDNLVVMDKLGVFAMASTGWDTEWLNLIRAWFRKPDNMCSHKRVEGRDHVEINNCLVCPNHNSIAEDICDGFVGVISFCCNVGNYLKGDHNCDVCHHKLLFSGKATLDHCTWRFCPDDCACCPECFFQSSWICMHEADDSKRVNKVCLSNNKGQTTCMPEPNYCSPIFQGDMPDTTILTTWACDAIQYHGPEPRIIHDMWAHIHAWGHTWAEDPNTKMALVTPKCNHLHLAAMPMWVEIRCPWSEPEKMREGEATFADFEHLLDPVFWVEQSCTASMWKHYGILQPKPHYPFGTPHSGEPPCEQEKGDVPGWHPNYMVGAFCCGMSEWKPGVNMETYWSCCHHGFCKPTNHAVCIKYLRETVLAMRMVMKQPCHNVQNLEEYQINACKWGLFNPPKWLDCNLWNASTDYDTEHIAWRVEAKRHFLQRVFEGILKFTEGRQCANMWEFCIGFWRMYIPFDSWVNHA"
    #ref = "AACCTTGG"
    #strtoalign = "ACACTGTGA"
    i = 0
    cols = []
    pam250 = dict()
    with open("PAM250_1.txt") as f:
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
                    pam250[(indexer, col)] = num
            i = i + 1
    #test = {("A", "B"): 1, ("B","A"): 2}
    #print test[("A", "B")]
    #print test["B", "A"]
    #print blosum62
    main(ref, strtoalign, pam250, 5)


