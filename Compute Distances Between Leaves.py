from queue import Queue
from collections import defaultdict
import re

def bfs(graph, root):
	curr = root
	d = [-1] * len(graph)
	d[curr] = 0

	q = Queue()
	for neighbor, weight in graph[curr]:
		d[neighbor] = weight + d[curr]
		q.put(neighbor)

	while not q.empty():
		curr = q.get()
		for neighbor, weight in graph[curr]:
			if d[neighbor] != -1:
				continue
			else:
				d[neighbor] = weight + d[curr]
				q.put(neighbor)

	return d

if __name__ == '__main__':
    # Load the data.
    with open('rosalind_BA7A.txt') as inFile:
        leaf_count = int(inFile.readline())

        graph = defaultdict(list)
        for line in inFile.readlines():
        	src, dst, weight = list(map(int, re.split('->|:', line.strip())))
        	graph[src].append((dst, weight))

    # Print output
    with open('rosalind_BA7A_out.txt', 'w') as outFile:
        for leaf in range(leaf_count):
        	print(' '.join(list(map(str, bfs(graph, leaf)[:leaf_count]))), file=outFile)