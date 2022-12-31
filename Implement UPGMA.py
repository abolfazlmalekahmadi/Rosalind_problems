class on_clutr(object):
    def __init__(self, id, age, nodes):
        self.id = id
        self.age = age
        self.nodes = nodes
    
    def cdwc(self, on_clutr, dis_max):
        sum_dis = sum(dis_max[i][j] for i in self.nodes for j in on_clutr.nodes)
        return sum_dis / float(len(self.nodes) * len(on_clutr.nodes))

def mrg_c(c1, c2, id, age):
    return on_clutr(id, age, c1.nodes + c2.nodes)

def cont_n(graph, parent, child):
    distance = parent.age - child.age

    graph[parent.id].append((child.id, distance)) 
    graph[child.id].append((parent.id, distance))

if __name__ == '__main__':
    with open('rosalind_BA7D.txt') as inFile:
        n = int(inFile.readline())
        dis_max = [list(map(int, inFile.readline().split())) for _ in range(n)]
        from collections import defaultdict

        on_clutrList = [on_clutr(id, age=0, nodes=[id]) for id in range(n)]
        all_clus = set([id for id in range(n)])
        graph = defaultdict(list)
        currentId = n
        while len(all_clus) > 1: 
            c1, c2 = min([(c1, c2) for c1 in all_clus for c2 in all_clus if c1 != c2], key=lambda tup: on_clutrList[tup[0]].cdwc(on_clutrList[tup[1]], dis_max))

            c1, c2 = on_clutrList[c1], on_clutrList[c2]

            age = c1.cdwc(c2, dis_max) / 2

            nw_c = mrg_c(c1, c2, currentId, age=age)
            currentId += 1
            distance = nw_c.age - c1.age

            cont_n(graph, nw_c, c1)
            cont_n(graph, nw_c, c2)

            all_clus.remove(c1.id)
            all_clus.remove(c2.id)
            all_clus.add(nw_c.id)
            on_clutrList.append(nw_c)

            
            distances = [nw_c.cdwc(on_clutr, dis_max) for on_clutr in on_clutrList]

            for i in range(len(dis_max)):
                dis_max[i].append(distances[i])

            dis_max.append(distances + [0])
        
 

        
        
       

     
    with open('rosalind_BA7D_out.txt', 'w') as outFile:
        nodeCount = len(graph)
        for u in range(nodeCount):
            for v, w in graph[u]:
                print('%d->%d:%.3f' % (u, v, w), file=outFile)