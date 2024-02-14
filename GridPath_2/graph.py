from geometry import intersect, in_polygon, euclidean_dist
import heapq

INF = float(1e9)

def createGraph(Map):
    graph = {}
    u = len(Map) - 1
    for v in range(len(Map)):
        distance = euclidean_dist(Map[u], Map[v])
        if u not in graph:
            graph[u] = {}
        if v not in graph:
            graph[v] = {}
        graph[u][v] = graph[v][u] = distance
        u = v
                
    for u in range(len(Map) - 2):
        for v in range(u+2, len(Map) - 1):
            graph = addEdge(Map, graph, u, v, Map[u], Map[v])
    return graph    

def addEdge(Map, Graph, u, v, p1, q1):
    if not in_polygon(Map, p1, q1):
        return Graph
    intersected = False
    j = None
    for i in range(len(Map)):
        if not j:
            j = i
            continue
        if u == i or u == j or v == i or v == j:
            j = i
            continue
        if intersect(p1, q1, Map[j], Map[i]):
            intersected = True
            break
        j = i
    if intersected: 
        return Graph

    distance = euclidean_dist(p1, q1)
    if u not in Graph: 
        Graph[u] = {}
    if v not in Graph:
        Graph[v] = {}
    Graph[u][v] = Graph[v][u] = distance
    return Graph

def find_path(Graph):
    dist = {u: INF for u in Graph}
    par = {u: None for u in Graph}
    
    pq = [(0, -2)]
    dist[-2] = 0
    while pq:
        du, u = heapq.heappop(pq)
        for v in Graph[u]:
            if dist[v] > dist[u] + Graph[u][v]:
                dist[v] = dist[u] + Graph[u][v]
                par[v] = u
                if v != -1: 
                    heapq.heappush(pq, (dist[v], v))
    
    path = []
    v = -1
    path.append(v)
    while par[v]:
        v = par[v]
        path.append(v)
    return path
    
    
    