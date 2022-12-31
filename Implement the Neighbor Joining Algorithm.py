from collections import defaultdict
import numpy as np


def nghbrjoin(D, n, labels=None):
    if not labels:
        labels = list(range(n))

    if n == 2:
        T = defaultdict(list)
        T[labels[0]].append({"n": labels[1], "w": D[0][1]})
        return T
    
    Node = np.copy(D)
    for i in range(len(D)):
        for j in range(len(D)):
            if i != j:
                Node[i, j] = (n - 2) * D[i, j] - sum(D[i, :]) - sum(D[j, :])

    Node = Node
    Node = np.copy(Node)
    np.fill_diagonal(Node, Node.max() + 1)
    NDR=divmod(Node.argmin(), Node.shape[1])
    i, j = NDR
    dlta = (sum(D[i, :]) - sum(D[j, :])) / (n - 2)
    limb_i = (D[i, j] + dlta) / 2
    limb_j = (D[i, j] - dlta) / 2

    li = labels[i]
    lj = labels[j]

    D = np.append(D, np.zeros((1, len(D))), axis=0)
    D = np.append(D, np.zeros((len(D), 1)), axis=1)
    labels = labels + [max(labels) + 1]

    for k in range(n):
        D[k, n] = (D[k, i] + D[k, j] - D[i, j]) / 2
        D[n, k] = (D[k, i] + D[k, j] - D[i, j]) / 2
    for x in [j, i]:
        D = np.delete(D, x, 0)
        D = np.delete(D, x, 1)
        del labels[x]

    T = nghbrjoin(D, n - 1, labels)

    T[labels[-1]].append({"n": li, "w": limb_i})
    T[labels[-1]].append({"n": lj, "w": limb_j})
    return T


if __name__ == '__main__':
    n, *D = open("rosalind_ba7e.txt").read().splitlines()
    F=[[int(x) for x in y.split()] for y in D]
    D = np.array(F, float)
    
    graph = nghbrjoin(D, int(n))
    with open('rosalind_BA7E_out.txt', 'w') as outFile:
        edges = []
        for k in sorted(graph):
            for v in graph[k]:
                edges += [f"{k}->{v['n']}:{v['w']:.3f}"]
                edges += [f"{v['n']}->{k}:{v['w']:.3f}"]
        se=sorted(edges)

        for edge in se:
            print(edge , file=outFile) 
        