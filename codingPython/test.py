def dijkstra(graph, start, end, w):
    distance = {}
    queue = []
    path = {}
    for i in graph:
        if i == start:
            distance[i] = 0
        else:
            distance[i] = float('inf')
        queue.append(i)
    node = start
    queue.remove(start)
    while queue:
        mn = float('inf')
        for i in graph[node]:
            next_node = i[0]

            n = distance[node] + i[1] + w[next_node]
            if distance[next_node] > n:
                distance[next_node] = n
                path[next_node] = node
        for i in queue:
            if distance[i] < mn:
                mn = distance[i]
                node = i
        queue.remove(node)
    r = end
    p = end
    while path[p] != start:
        p = path[p]
        r += " " + p
    r += " " + start
    r = r[::-1]
    print(r + " ")
    print(distance[end] - w[end])


a, m = map(int, input().split())
w = {}
name = input().split()
for i in name:
    t = input().split()
    w[t[0]] = int(t[1])

graph = {}
for i in w:
    graph[i] = []

for i in range(m):
    a, b, c = input().split()
    graph[a].append([b, int(c)])
    graph[b].append([a, int(c)])

q = input()
r = input()
dijkstra(graph, q, r, w)