__author__ = 'urvish'

import numpy
import re
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

    print matrix
    print max(matrix[:, matrix.shape[1]/2])
    print matrix[:, matrix.shape[1]/2]

    col =  matrix.shape[1]/2 -1
    row = max( (v, i) for i, v in enumerate(matrix[:, matrix.shape[1]/2]) )[1] -1

    pth = path_taken[row+1, col+1]
    if pth ==3:
        nextrow = row+1
        nextcol = col+1
    if pth ==2:
        nextrow = row
        nextcol = col +1
    if pth ==1:
        nextrow = row+1
        nextcol = col


    print "(" + str(row) + ", " + str(col) + ") " + "(" + str(nextrow) + ", " + str(nextcol) + ")"

    # print int(matrix.max())
    # maxidx = numpy.where(matrix==matrix.max())
    #
    # maxidx =  (maxidx[0][0], maxidx[1][0])
    # i = maxidx[0]
    # j = maxidx[1]
    # strres = ""
    # refres  = ""
    # while True:
    #     if (i == 0 and j==0):
    #         break
    #     if (matrix[i][j] == 0):
    #         break
    #     if matrix[i -1][j] - indelcost == matrix[i][j]:
    #         ##moved down
    #         i=i-1
    #         strres = "-"+strres
    #         refres = ref[i] + refres
    #     elif matrix[i][j-1] - indelcost == matrix[i][j]:
    #         ##moved right
    #         j=j-1
    #         strres = stralign[j] + strres
    #         refres = "-" + refres
    #
    #     else:
    #         i = i-1
    #         j= j-1
    #         strres = stralign[j]+strres
    #         refres = ref[i] + refres
    #
    # print refres
    # print strres



if __name__ == "__main__":
    """
     PLEASANTLY
     MEASNLY
    """
    ref = "NMRMGNWHIIIHLEIGINCDERRMFYGFYYAGEVYVSVSGHMLDTHIKNMVMLSSNWYKQVTDRLHVHQWKMCHCHTKGQNRWHYFSNSDQTLHYISSFFYYDIIHSVWTIYPWLMYQFCMHGLQGSKQRCWYQHIMMRAKGKFRFMVNYIDRVWEACDDSVLYGANFSVEVWDLDWTQHQPRAIGYRHEYWGACDAEKYPRCSFICHPKHHHLHNFNCSEYCEKTHHPQLKWQGKGNSQHIESVRRITPLWKFCSPNWWQRKRLMIEDMNFAMVPGMYKASGYAKKTFKDPAWMASKHADWIWPHYPVDGWGHFGKFRLWACNQPTCPKQKHHIERDASYVCHALHCQWAGQDPDLYKRSSRVSFRGFCLIACEFVPVHGVGGRMTHHNPTFMCIELNCAGYVWVFAECHMTVKCPCERNGEVMVIGQDTMFNTKFIYTQCHDQIGAAGQLTWGGCPCHQGCPPHYKWIHTHAQIWMYCPQWQRTQDETNGQMREVRLFAASVDFGRIDRLPCRKYSRCNGDQREEFCAGQNPIVDLFCQHRVNHEPCFTLIVNGWAKSWFCESKPTCAARAWTYNLIRCCMLRKETRNQTKHRNQEKPYCRLWKIKQEYYIKLDRLDQIPGSNVLALKECIHLILIVSKLVMSTDLNNIGQTACLVSRIEYHGTDQAAKFAKWQYVDFRWFTLMWVVPYSNFPDQCRNELWHVDHKATQIKPYQVPEFIMCRFVYAPGMTQGKTAPIKFYMLSQTKCVQEEGSRCGANWNDRGDMHMLDWNFAVENPSMRTNPTFVFPDNSPQNQNAVNTHDLDEAMSPVGRANVDQGGEMCTVPAYAGASWRYDYNGHRLAMSEQYDQAKEFYYCACFNGIAWHIMVIALGEKPFQTGRSPHDTKHLYEHCMPQVTHSPIYQNPGAMNISSSVDYDFMTPRTAQHQDKGVHVDNTHVNIMNAWYIKNEQSIRPPGGEQSHKQTVECGAFLGHSAMWEWFWTNVRRVAGRLWRSGCNMRRFFKAALRNEPYRSGEFWWWILDTTSFASHYDAQ"
    strtoalign = "NQSPYKNEGAANSYPLWGCQWLGCSNIVSEGPAWLMWEPRFCRGMWPQKDDWGHNWIQKDPELTNMIEFCHAQFYTHWCYTPSFHEARGHGQYAHVTQKYFSHINTDERHQQVDHGLHEVWKTQENGPWWFESCLNPYPEYERSVGAGSSRHLGCACMCMSKCQGYCAEYFLRNKRWVGYMMYWNGAKRAEKHCFKITPKNRNQDHVDQKEIEWCFWCIIMDGVNTDVRISPIRVGAYNNCQSINPVGKQPLMAWFQNCLKAYLCGGDFEPFSSMCFIYHQNWYQVSAFQTRLKAKHEVIQYNMIDMCYMWNSETKKTCEAEGEHTMKMQPNYRYQDCLKGQFHGYWYDINTNTAVVSQDRKFQPIGKSEEFVSSMLGGQTHWPTMNIRKLFLTHHSIKQCAQTGDRLTGGYRIRCWKFVEFHCMVNYWAEAMTVTDYGGNFNPQLWLKVQLTWGGCPPADPCIWMYCTQDDRKEHGKQRTQAHMIWRRKMREVRLFAASVDFGRIPREKGFVFRLPCRKYSRCNGDQRMVENLCEFCAGGLDPSNPDVDLFCQHFTARGIHFCFTLINVAGWAKHWFCESSYWLRRCCMLRPNMTWPRNFMCVKKFPSAPNHWQHQGTETITKDQKHHFNVHVCCLTTYVCLAQAAKDRYMTENDDAITQPLNSVLCLCVDAGVKLYMWQRWETAINVVMTKCGRDFIHIFIFFLHWKVRFPWESKGVNFEAEIMTNCTGHWLKYRWCWGNGWANYNYLMCRYYKAKKGKVARPHMQHFVLFQTGVDQGGTNNEIGDRGHMQHVNHEELSNFCFMMPHRRGDDDFHMDAWWLSGLSSSSATLHCHERMGDMCLRHIYDMHQQQPEKMCFRCDNECGMCGPEHVVPACRQMYNGYKSMIMHIWKWVLPSTYVWPVKLQLWWNQFLCFAQTLLASESCGATSPWCSGHAVIHFTQTKNKHRTRTLWPGINHDFIMDIWHRITACKCKEGCIATEIKPFICPSLWADSPKMIMYPLEKEVEAHAKRYVTSELYSHDKATCFYTHAEFQTYAWMSS"
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
    main(ref,strtoalign, blosum62, 5)
