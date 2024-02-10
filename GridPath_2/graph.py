from geometry import intersect, in_polygon, euclidean_dist
import heapq

INF = float(1e9)

def createGraph(Map, Graph):
    for i in range(len(Map)):
        for j in range(i+1, len(Map)):
            addEdge(Map, Graph, i, j, Map[i], Map[j])
        
def addEdge(Map, Graph, u, v, p1, q1):
    if not in_polygon(Map, p1, q1):
        return
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
        return

    distance = euclidean_dist(p1, q1)
    if u not in Graph: 
        Graph[u] = {}
    Graph[u][v] = distance
    if v not in Graph:
        Graph[v] = {}
    Graph[v][u] = distance

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
    
    
    