
def paget(graph, src, dst, visited):

    visited[src] = True
    for v, w in graph[src]:
        if visited[v]:
            continue

        if v == dst:
            return [(src, w), (dst, 0)]

        path = paget(graph, v, dst, visited)
        if path is not None:
            return [(src, w)] + path

    return None


def phadd(diM, n , nName):

    nName=2 * len(diM) - 3
    if n == 2:
        distance = diM[0][1]
        return { 0:[(1, distance)], 1:[(0, distance)] }
    j=n-1
    p = min(diM[i][j] + diM[k][j] - diM[i][k] \
		for i in range(n) for k in range(n) if i != j and k != j) // 2
    limbLength = p
    for i in range(n-1):
        diM[i][n-1] -= limbLength
        diM[n-1][i] = diM[i][n-1]
    for i in range(n-1):
        for j in range(i+1, n-1):
            if diM[i][j] == diM[i][n-1] + diM[j][n-1]:
                x = diM[i][n-1]
                src, dst = i, j  
                break
    
    graph = phadd(diM, n-1, nName=nName-1)

    visited = [False] * (2 * len(diM))
    
    path = paget(graph, src, dst, visited)

    curr = 0  
    elength = path[0][1]
    rlength = distance

    while rlength >= elength:
        rlength -= elength
        curr += 1
        elength = path[curr][1]

    cNode = path[curr][0]
    nNode = path[curr+1][0]

    graph[cNode].append((nName, rlength))
    graph[nNode].append((nName, elength - rlength))
    graph[nName] = [(cNode, rlength), (nNode, elength - rlength)]

    for i, (neighbor, length) in enumerate(graph[cNode]):
        if neighbor == nNode:
            break
    del graph[cNode][i]

    for i, (neighbor, length) in enumerate(graph[nNode]):
        if neighbor == cNode:
            break
    del graph[nNode][i]
    
    
    graph[n-1] = [(nName, limbLength)]
    graph[nName].append((n-1, limbLength))

    return graph





if __name__ == '__main__':
    # Load the data.
    with open('rosalind_BA7C.txt') as inFile:
        n = int(inFile.readline())
        diM = [list(map(int, line.split())) for line in inFile.readlines()]
        phadd(diM, n, nName=2 * len(diM) - 3)
        graph = phadd(diM, n)

    # Print output
    with open('rosalind_BA7C_out.txt', 'w') as outFile:
        for src in graph:
            for dst, length in graph[src]:
                print('%d->%d:%d' % (src, dst, length), file=outFile)