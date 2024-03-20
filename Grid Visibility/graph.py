from geometry import intersect, inPolygon, euclideanDistance
import heapq

INF = float(1e9)

def createGraph(Map):
    graph = {}
    u = len(Map) - 1
    for v in range(len(Map)):
        distance = euclideanDistance(Map[u], Map[v])
        if u not in graph: graph[u] = {}
        if v not in graph: graph[v] = {}
        graph[u][v] = graph[v][u] = distance
        u = v
                
    for u in range(len(Map) - 2):
        for v in range(u+2, len(Map) - 1):
            graph = addEdge(Map, graph, u, v, Map[u], Map[v])
    return graph    

def addStartEnd(Map, Graph, startCoord, endCoord):
    for i in range(len(Map)):
        addEdge(Map, Graph, -2, i, startCoord, Map[i])
        addEdge(Map, Graph, -1, i, endCoord, Map[i])
    addEdge(Map, Graph, -2, -1, startCoord, endCoord)
    Map.append(startCoord)
    Map.append(endCoord)

def removeStartEnd(Graph):
    if -1 in Graph: del Graph[-1]
    if -2 in Graph: del Graph[-2]
    for u in Graph:
        if -1 in Graph[u]: del Graph[u][-1]
        if -2 in Graph[u]: del Graph[u][-2]
    
def addEdge(Map, Graph, u, v, p1, q1):
    
    if not inPolygon(Map, p1, q1): return Graph
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
    if intersected: return Graph

    distance = euclideanDistance(p1, q1)
    if u not in Graph: Graph[u] = {}
    if v not in Graph: Graph[v] = {}
    Graph[u][v] = Graph[v][u] = distance
    return Graph

def findPath(Graph):
    Dist = {u: INF for u in Graph}
    Par = {u: None for u in Graph}
    
    pq = [(0, -2)]
    Dist[-2] = 0
    while pq:
        du, u = heapq.heappop(pq)
        for v in Graph[u]:
            if Dist[v] > Dist[u] + Graph[u][v]:
                Dist[v] = Dist[u] + Graph[u][v]
                Par[v] = u
                if v != -1: heapq.heappush(pq, (Dist[v], v))
    
    path = []
    v = -1
    dist = 0
    path.append(v)
    while Par[v]:
        dist += Graph[v][Par[v]]
        v = Par[v]
        path.append(v)
    return path, dist
    
    
    