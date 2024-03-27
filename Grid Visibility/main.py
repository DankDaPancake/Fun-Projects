fi = open('lee.inp', 'r')

import tkinter as Tk
import time
from presets import *
from geometry import inPolygon, euclideanDistance
from graph import createGraph, findPath, addStartEnd, removeStartEnd

BaseMap, BaseGraph = [], {}
Map, MapRootId, Graph, Path = [], [], {}, []
startCoord, endCoord = (), ()
editStart, editEnd = True, False
inCanvas, isDragging = True, False
newScale = GRID_SIZE
counter, Ox, Oy, offsetX, offsetY = 0, 0, 0, 0, 0

def main():
    window = Tk.Tk()
    window.title('Visibility Graph and Shortest Path')
    global WIN_WIDTH
    global WIN_HEIGHT
    WIN_WIDTH = window.winfo_screenwidth() * 3 / 4
    WIN_HEIGHT = window.winfo_screenheight() * 3 / 4
    window.resizable(False, False)
    
    window.geometry(
        "%dx%d+%d+%d"
        % (WIN_WIDTH, WIN_HEIGHT, window.winfo_screenwidth() / 2 - WIN_WIDTH / 2, window.winfo_screenheight() / 2 - WIN_HEIGHT / 2,)
    )
    
    root_frame = Tk.Frame(window).pack(padx = PADDING, pady = PADDING / 2)
    
    menu_frame = Tk.Frame(root_frame)
    menu_frame.pack(side = Tk.TOP, padx = PADDING, pady = PADDING / 2, fill = "x")
    
    map_menu = Tk.Frame(menu_frame)
    map_menu.pack(side = Tk.LEFT)
    
    log_frame = Tk.Frame(root_frame)
    log_frame.pack(side = Tk.BOTTOM, padx = PADDING, pady = PADDING / 2, fill = "x")

    Tk.Button(map_menu, text = "Pick Start", bg = BUTTON_COLOR, command = pinStart).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu, text = "Pick End", bg = BUTTON_COLOR, command = pinEnd).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu, text = "Find Path", bg = BUTTON_COLOR, command = drawPath).pack(side = Tk.LEFT, padx = PADDING)

    global displayGraph
    displayGraph = Tk.BooleanVar()
    Tk.Checkbutton(map_menu, text="Show Graph", command=on_tick, variable=displayGraph).pack(side = Tk.LEFT, padx = PADDING)

    global textvalue, textentry
    textvalue = Tk.IntVar()
    textentry = Tk.Entry(menu_frame, width = 8, textvariable = textvalue, bg = BUTTON_COLOR).pack(side = Tk.RIGHT, padx = PADDING)
    textvalue.trace_add("write", on_value_changes)
    Tk.Label(menu_frame, text = "Duplicates:").pack(side = Tk.RIGHT)

    global scalevalue, scaleentry
    scalevalue = Tk.IntVar()
    scaleentry = Tk.Entry(menu_frame, width = 8, textvariable = scalevalue, bg = BUTTON_COLOR).pack(side = Tk.RIGHT, padx = PADDING)
    scalevalue.trace_add("write", on_scale_changes)
    Tk.Label(menu_frame, text = "Scale:").pack(side = Tk.RIGHT)

    global canvas
    canvas = Tk.Canvas(root_frame, bg = "#ffffff")
    canvas.pack(padx = PADDING, pady = PADDING / 2, expand = True, fill = "both")

    global CAV_WIDTH, CAV_HEIGHT
    canvas.update()
    CAV_WIDTH, CAV_HEIGHT = canvas.winfo_width(), canvas.winfo_height()
    
    global status_log, cursor_log, startpoint_log, endpoint_log
    status_log = Tk.StringVar()
    Tk.Label(log_frame, textvariable = status_log).pack(side = Tk.LEFT, padx = PADDING)
    
    cursor_log = Tk.StringVar()
    cursor_log.set("Cursor: (0; 0)")
    Tk.Label(log_frame, textvariable = cursor_log).pack(side = Tk.RIGHT, padx = PADDING)
    
    endpoint_log = Tk.StringVar()
    endpoint_log.set("End point: (0; 0).")
    Tk.Label(log_frame, textvariable = endpoint_log).pack(side = Tk.RIGHT, padx = PADDING)
    
    startpoint_log = Tk.StringVar()
    startpoint_log.set("Start point: (0; 0).")
    Tk.Label(log_frame, textvariable = startpoint_log).pack(side = Tk.RIGHT, padx = PADDING)
    
    canvas.bind("<Motion>", on_cursor_move)
    canvas.bind("<Button-1>", on_left_click)
    canvas.bind("<Button-3>", on_right_click)
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<B3-Motion>", on_drag)
    
    scanMap()
    drawGrid()
    window.mainloop()
    
def scanMap():
    global BaseMap, BaseGraph, GRID_SIZE
    for readline in fi.read().split("\n"):
        ux, uy = map(int, readline.split(" "))
        BaseMap.append((ux * GRID_SIZE, uy * GRID_SIZE))
    BaseGraph = createGraph(BaseMap)

def duplicateBase(k):
    '''
    vis = []
    for i in range(mul):
        w, h = 9 * i, 8 * i
        for j in range(len(base_vis) - 2 * (i != mul - 1)):
            vis.append(((base_vis[j][0][0] + w, 
                         base_vis[j][0][1] + h - (j + 1 if j < 2 and i else 0)), 
                        (base_vis[j][1][0] + w, 
                         base_vis[j][1][1] + h)))
    '''
    
    global BaseMap, BaseGraph, Map, MapRootId, Graph 
    Graph.clear()
    Map.clear()
    MapRootId.clear()
    if k == 0: return
    
    n = len(BaseMap)
    
    global GRID_SIZE
    start_time = time.time()
    
    for i in range(k):
        ii = (0 if i == 0 else 2) 
        for j in range(ii, n - 5):
            x, y = BaseMap[j]
            x, y = x + 9*i * GRID_SIZE, y + 7*i * GRID_SIZE
            Map.append((x, y))
            MapRootId.append((j, i+1))
    
    x, y = BaseMap[-5]
    x, y = x + 9*(k-1) * GRID_SIZE, y + 7*(k-1) * GRID_SIZE
    if (x, y) != Map[-1]: 
        Map.append((x, y))
        MapRootId.append((n-5, k))
    x, y = BaseMap[-4]
    x, y = x + 9*(k-1) * GRID_SIZE, y + 7*(k-1) * GRID_SIZE
    if (x, y) != Map[-1]: 
        Map.append((x, y))
        MapRootId.append((n-4, k))
        
    for i in range(k-1, -1, -1):
        for j in range(n-3, n):
            x, y = BaseMap[j]
            x, y = x + 9*i * GRID_SIZE, y + 7*i * GRID_SIZE
            if (x, y) != Map[-1]: 
                Map.append((x, y))
                MapRootId.append((j, i+1))

    for u in range(len(Map)):
        #print(Map[u][0] // GRID_SIZE, Map[u][1] // GRID_SIZE, MapRootId[u])
        uu, uk = MapRootId[u]
        for v in range(u+1, len(Map)):
            vv, vk = MapRootId[v]
            #print(u, v, uu, vv)      
            if uu == vv or uk != vk: continue
            if vv not in BaseGraph[uu]: continue
            if u not in Graph: Graph[u] = {}
            if v not in Graph: Graph[v] = {}
            Graph[u][v] = Graph[v][u] = BaseGraph[uu][vv]
    
    u = len(Map) - 1
    for i in range(k-1):
        u -= 2
        Graph[u][u+1] = Graph[u+1][u] = euclideanDistance(Map[u], Map[u+1])
        v = 2 + i * 22
        Graph[u][v] = Graph[v][u] = euclideanDistance(Map[u], Map[v])
        v = 3 + i * 22
        Graph[u][v] = Graph[v][u] = euclideanDistance(Map[u], Map[v])
        v = 12 + i * 22
        Graph[u][v] = Graph[v][u] = euclideanDistance(Map[u], Map[v])
        v = 13 + i * 22
        Graph[u][v] = Graph[v][u] = euclideanDistance(Map[u], Map[v])
        v = 22 + i * 22
        Graph[u][v] = Graph[v][u] = euclideanDistance(Map[u], Map[v])
        v = 23 + i * 22
        Graph[u][v] = Graph[v][u] = euclideanDistance(Map[u], Map[v])
        v = 24 + i * 22
        Graph[u][v] = Graph[v][u] = euclideanDistance(Map[u], Map[v])
        v = 23 + i * 22
        Graph[u-1][v] = Graph[v][u-1] = euclideanDistance(Map[u-1], Map[v])
        Graph[v][v+1] = Graph[v+1][v] = euclideanDistance(Map[v], Map[v+1])
    
    drawLines(Map, color = "black", width = GRID_SIZE / 10, tags = "map")
    status_log.set(f"Map generated in {(time.time() - start_time):.5f} s.")

def pinStart():
    global editStart, editEnd
    editStart = True
    editEnd = False

def pinEnd():
    global editStart, editEnd
    editEnd = True
    editStart = False

def drawPath():
    if not startCoord or not endCoord:
        status_log.set("Pick your starting and ending point!")
        return
    global Graph, Map
    addStartEnd(Map, Graph, startCoord, endCoord)
    
    global Path
    start_time = time.time()
    Path, Distance = findPath(Graph)
    status_log.set(f"Found shortest path found in {((time.time() - start_time) * 1000):.5f} ms. Distance: {(Distance / GRID_SIZE):.2f}")
    drawGraph("path")
    
def drawGraph(tags = "graph"):
    offset = newScale / GRID_SIZE
    canvas.delete(tags)
    if tags == "path":
        global Path, startCoord, endCoord
        x1, y1 = (), ()
        for u in Path:
            if u == -2: x2, y2 = startCoord
            elif u == -1: x2, y2 = endCoord
            else: x2, y2 = Map[u]
            if x1: 
                canvas.create_line(x1 * offset, y1 * offset, x2 * offset, y2 * offset, fill = "#2563eb", width = newScale / PADDING, tags = "path")
            x1, y1 = x2, y2
            
    elif tags == "graph":
        if not Map: return
        global Graph
        if not Graph: Graph = createGraph(Map)
        for u in Graph:
            for v in Graph[u]:
                if v < u: continue
                canvas.create_line(Map[u][0] * offset, Map[u][1] * offset, Map[v][0] * offset, Map[v][1] * offset, fill = "grey", width = newScale / 20, tags = "graph")

def drawGrid(offsetX = 0, offsetY = 0):
    MAP_WIDTH = CAV_WIDTH // newScale
    MAP_HEIGHT = CAV_HEIGHT // newScale
    for i in range(MAP_WIDTH):
        canvas.create_line(i * newScale + offsetX, offsetY, i * newScale + offsetX, CAV_HEIGHT + offsetY, fill = GRID_COLOR, tags = "grid")   
    for i in range(MAP_HEIGHT):
        canvas.create_line(offsetX, i * newScale + offsetY, CAV_WIDTH + offsetX, i * newScale + offsetY, fill = GRID_COLOR, tags = "grid") 

def drawLines(verts, color, width, tags):
    #canvas.create_polygon(Map[:-1], fill = "#ddeeff", tags = "map")
    if not verts: return
    offset = newScale / GRID_SIZE
    ux, uy = verts[0]
    for i in range(1, len(verts)):
        vx, vy = verts[i]
        drawPoint((ux, uy), tags, offset)
        canvas.create_line(ux * offset, uy * offset, vx * offset, vy * offset, fill = color, width = width, tags = tags)
        ux, uy = vx, vy
        
def drawPoint(vertice, tags, offset):
    x, y = vertice
    if tags == "map":
        global counter 
        counter += 1
        #canvas.create_text((x-7) * offset, (y-7) * offset, text = str(counter), tags = "label")
        canvas.create_oval((x-3) * offset, (y-3) * offset, (x+3) * offset, (y+3) * offset, fill = "black", outline = "", tags = tags)
        
    if tags == "start_point": 
        canvas.delete("start_point")
        canvas.delete("end_point")
        canvas.create_oval((x-3) * offset, (y-3) * offset, (x+3) * offset, (y+3) * offset, fill = START_COLOR, outline = "", tags = tags)
        
    if tags == "end_point": 
        canvas.delete("end_point")
        canvas.create_oval((x-3) * offset, (y-3) * offset, (x+3) * offset, (y+3) * offset, fill = END_COLOR, outline = "", tags = tags)

def drawCursor(x, y):
    canvas.delete("cursor_preview")
    global editStart, editEnd
    if not editStart and not editEnd: return
    if editStart:
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = "#9fff93", outline = "", tags = "cursor_preview")
    elif editEnd:
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = "#ffd7a6", outline = "", tags = "cursor_preview")

def on_value_changes(*args):
    canvas.delete("graph", "map", "path", "start_point", "end_point", "label")
    global textvalue
    try: 
        k = textvalue.get()
    except: 
        k = 0
    if k > 75: k = 75
    global counter
    counter = 0
    duplicateBase(k)

def on_scale_changes(*args):
    global scalevalue, GRID_SIZE
    try:
        k = scalevalue.get()
    except:
        k = GRID_SIZE
    
    if k == 0: k = GRID_SIZE
    
    global newScale, counter, Ox, Oy
    Ox, Oy = 0, 0
    newScale = k
    counter = 0
    canvas.delete("grid", "graph", "map", "path", "start_point", "end_point", "label")
    removeStartEnd(Graph)
    drawGrid()
    
    drawLines(Map, "black", newScale / 10, "map")

def on_tick():
    state = displayGraph.get()
    if state:
        drawGraph("graph")
    else:
        canvas.delete("graph")

def on_drag(event):

    global Ox, Oy, offsetX, offsetY, isDragging
    if isDragging:
        
        dx = event.x - Ox

        dy = event.y - Oy

        offsetX += dx
        offsetY += dy
        canvas.delete("grid")
        drawGrid(offsetX % newScale, offsetY % newScale)
        # print(offset_x, offset_y)
        print(dx, dy)
        canvas.move("all", dx, dy)
        Ox, Oy = event.x, event.y
                    
def on_left_click(event):
    global startCoord, endCoord, editStart, editEnd
    
    offset = newScale / GRID_SIZE
    if len(Map) > 2:                            
        x, y = event.x / offset, event.y / offset
        if inPolygon(Map, (x, y), (x, y)):
            if editStart: 
                startCoord = x, y
                drawPoint(startCoord, "start_point", offset)
                startpoint_log.set(f"Start point: ({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f}).")
                editStart = False
                if not endCoord: editEnd = True
            elif editEnd:
                endCoord = x, y
                drawPoint(endCoord, "end_point", offset)
                endpoint_log.set(f"End point: ({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f}).")
                editEnd = False
                if not startCoord: editStart = True
        else:
            status_log.set("Invalid point!")

def on_right_click(event):
    global isDragging, Ox, Oy
    Ox, Oy = event.x, event.y
    print(isDragging)
    isDragging = True
    
def on_cursor_move(event):
    global inCanvas
    if not inCanvas: return
    cursor_log.set(f"Cursor: ({((event.x - Ox) / newScale):.2f}; {((event.y - Oy) / newScale):.2f}).")
    drawCursor(event.x, event.y)
    
def on_enter(event):
    global inCanvas
    inCanvas = True
    
def on_leave(event):
    global inCanvas
    inCanvas = False
    canvas.delete("cursor_preview")
    cursor_log.set(f"Cursor: out of canvas")

if __name__ == "__main__":
    main()