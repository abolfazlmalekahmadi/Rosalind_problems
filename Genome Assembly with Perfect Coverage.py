
if __name__ == "__main__":
    
    input_lines = open("rosalind_pcov.txt").read().splitlines()#
    dbgel = set()
    for kmer in input_lines:
        dbgel.add(kmer)

    k = len(input_lines[0])
    dbg = [[elem[0:k - 1], elem[1:k]] for elem in dbgel]

    temp = dbg.pop(0)
    string = temp[0][-1]
    while dbg:
        string += temp[1][-1]
        [index] = [i for i, p in enumerate(dbg) if p[0] == temp[1]]
        temp = dbg.pop(index)

    print(string)