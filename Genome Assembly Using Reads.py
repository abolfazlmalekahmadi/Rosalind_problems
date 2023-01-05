
if __name__ == "__main__":

    input_lines = open("rosalind_gasm.txt").read().splitlines()
    ########
    for kval in range(1, len(input_lines[0])):
        dbgel = set()
        for kmer in input_lines:
            for i in range(kval):
                dbgel.add(kmer[i:len(kmer) + i - kval + 1])
                revc_seq = kmer[i:len(kmer) - kval + i + 1]
                revc_seq1=revc_seq[::-1].translate(str.maketrans("ACGT", "TGCA"))
                dbgel.add(revc_seq1)

        k = len(list(dbgel)[0])
        edge = lambda elmt: [elmt[0:k - 1], elmt[1:k]]
        dbg = [edge(elmt) for elmt in dbgel]

        clist = []
        for repeat in range(2):
            tmk = dbg.pop(0)
            cyclic = tmk[0][-1]
            while tmk[1] in [item[0] for item in dbg]:
                cyclic += tmk[1][-1]
                [index] = [i for i, pair in enumerate(dbg) if pair[0] == tmk[1]]
                tmk = dbg.pop(index)
            clist.append(cyclic)

        if len(dbg) == 0:
            break
    result1, result2 = clist

    print(result1)