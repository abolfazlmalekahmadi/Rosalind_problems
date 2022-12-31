def intre(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    ALPHABET = ['A', 'C', 'G', 'T']
    
    with open('rosalind_BA7f.txt') as inFile:
        lines = inFile.read().splitlines()
       
        adj_list = []
        for row in lines[1:]:
            temp = row.rstrip().split('->')
            adj_list.append(temp)
  
        Tag = {}
        S = {}
        nodes = [item for sublist in adj_list for item in sublist]
        nodes = list(set(nodes))
        for v in nodes:
            S[v] = {}
            Tag[v] = 0
            if not intre(v):
                Tag[v] = 1
                len_dna = len(v)
                for pos in range(len_dna):
                    S[v][pos] = {}
                    char = v[pos]
                    for k in ALPHABET:
                        if char == k:
                            S[v][pos][k] = 0
                        else:
                            S[v][pos][k] = 1e6
        while any(x == 0 for x in list(Tag.values())):
            zero = [node for node, tag in Tag.items() if tag == 0]
            for zn in zero:
                children = [child for parent, child in adj_list if parent == zn]
                if all([Tag[child] == 1 for child in children]):
                    v = zn
                    break
            Tag[v] = 1
            S[v] = {}
            for pos in range(len_dna):
                S[v][pos] = {}
                for k in ALPHABET:
                    temp = []
                    for i, score in S[children[0]][pos].items():
                        if i == k:
                            temp.append(score)
                        else:
                            temp.append(score + 1)
                    scd = min(temp)
                    temp = []
                    for i, score in S[children[1]][pos].items():
                        if i == k:
                            temp.append(score)
                        else:
                            temp.append(score + 1)
                    ss = min(temp)
                    S[v][pos][k] = scd + ss
        score_dict = S
    with open('rosalind_BA7f_out.txt', 'w') as outFile:
            nodes = [item for sublist in adj_list for item in sublist]
            nodes = list(set(nodes))
            chn = [child for parent, child in adj_list]
            root = nodes[0]
            idx = 1
            while root in chn:
                root = nodes[idx]
                idx += 1
            label_dict = {}
            label_dict[root] = ''
            mps = 0
            for pos, scores in score_dict[root].items():
                label_dict[root] += min(scores, key=scores.get)
                mps += min(scores.values())
            Tag = {}
            for node in nodes:
                if not intre(node):
                    Tag[node] = 1
                else:
                    Tag[node] = 0
            Tag[root] = 1
            while any(x == 0 for x in list(Tag.values())):
                one_nodes = [node for node, tag in Tag.items() if tag == 1]
                for node in one_nodes:
                    children = [child for parent, child in adj_list if parent == node]
                    if intre(node) and all([Tag[child] == 0 for child in children]):
                        v = node
                        break
                dl = ''
                ds = score_dict[children[0]]
                for pos, daughter_score in ds.items():
                    parent_letter = label_dict[v][pos]
                    min_nucs = [nuc for nuc, val in daughter_score.items() if val == min(daughter_score.values())]
                    if parent_letter in min_nucs:
                        dl += parent_letter
                    else:
                        dl += min_nucs[0]
                label_dict[children[0]] = dl
                Tag[children[0]] = 1
                son_label = ''
                son_scores = score_dict[children[1]]
                for pos, son_score in son_scores.items():
                    parent_letter = label_dict[v][pos]
                    min_nucs = [nuc for nuc, val in son_score.items() if val == min(son_score.values())]
                    if parent_letter in min_nucs:
                        son_label += parent_letter
                    else:
                        son_label += min_nucs[0]
                label_dict[children[1]] = son_label
                Tag[children[1]] = 1
            final_adj_list = []
            for edge in adj_list:
                if intre(edge[0]):
                    node0 = label_dict[edge[0]]
                else:
                    node0 = edge[0]
                if intre(edge[1]):
                    node1 = label_dict[edge[1]]
                else:
                    node1 = edge[1]
                mm = [node0[i] != node1[i] for i in range(len(node0))]
                final_adj_list.append([node0, node1, sum(mm)])
                final_adj_list.append([node1, node0, sum(mm)])
                final_adj_list, mps = [final_adj_list, mps]
                print(mps , file=outFile)
                for edge in final_adj_list:
                    print(str(edge[0]) + '->' + str(edge[1]) + ':' + str(edge[2]) , file=outFile)