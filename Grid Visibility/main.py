fi = open('lee.inp', 'r')

import tkinter as Tk
import time
from presets import *
from geometry import inPolygon
from graph import createGraph, findPath, addStartEnd, removeStartEnd

BaseMap, Map, Graph, Path = [], [], {}, []
editingMap = True
startCoord, endCoord = (), ()
editStart, editEnd = True, False

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
    
    root_frame =  Tk.Frame(window).pack(padx = PADDING, pady = PADDING / 2)
    
    menu_frame = Tk.Frame(root_frame)
    menu_frame.pack(side = Tk.TOP, padx = PADDING, pady = PADDING / 2, fill = "y")
    
    map_menu = Tk.Frame(menu_frame)
    map_menu.pack(side = Tk.LEFT)
    
    log_frame = Tk.Frame(root_frame)
    log_frame.pack(side = Tk.BOTTOM, padx = PADDING, pady = PADDING / 2, fill = "x")
    
    Tk.Button(map_menu, text = "Pick Start", bg = BUTTON_COLOR, command = pinStart).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu, text = "Pick End", bg = BUTTON_COLOR, command = pinEnd).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu, text = "Show Graph", bg = BUTTON_COLOR, command = drawGraph).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu, text = "Find Path", bg = BUTTON_COLOR, command = drawPath).pack(side = Tk.LEFT, padx = PADDING)
    #Tk.Button(map_menu, text = "Reset", bg = BUTTON_COLOR, command = reset).pack(side = Tk.LEFT, padx = PADDING)
    
    Tk.Label(map_menu, text = "Duplicates:").pack(side = Tk.LEFT)
    global textvalue, textentry
    textvalue = Tk.IntVar()
    textentry = Tk.Entry(map_menu, width = 10, textvariable = textvalue, bg = BUTTON_COLOR).pack(side = Tk.LEFT)
    textvalue.trace_add("write", on_value_changes)
    
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
    
    drawGrid()
    scanMap()
    updateCanvas()
    window.mainloop()

def updateCanvas():
    if startCoord: drawPoint(startCoord, "start_point")
    if endCoord: drawPoint(endCoord, "end_point")
    
def scanMap():
    global editingMap, Map, BaseMap, Graph
    editingMap = False
    for readline in fi.read().split("\n"):
        ux, uy = map(int, readline.split(" "))
        BaseMap.append((ux * GRID_SIZE, uy * GRID_SIZE))
    #print(BaseMap)

def on_value_changes(*args):
    canvas.delete("graph")
    global textvalue
    textK = textvalue.get()
    if textK == "": return
    K = textK
    print(K)
    duplicateBase(K)
    
def duplicateBase(k):
    global Map, BaseMap, Graph
    Graph.clear()
    Map.clear()
    canvas.delete("map")
    
    print(len(BaseMap))
    for i in range(k):
        ii = (0 if i == 0 else 2) 
        for j in range(ii, len(BaseMap) - 5):
            x, y = BaseMap[j]
            x, y = x + 9*i * GRID_SIZE, y + 7*i * GRID_SIZE
            Map.append((x, y))
    
    x, y = BaseMap[-5]
    x, y = x + 9*(k-1) * GRID_SIZE, y + 7*(k-1) * GRID_SIZE
    Map.append((x, y))
    x, y = BaseMap[-4]
    x, y = x + 9*(k-1) * GRID_SIZE, y + 7*(k-1) * GRID_SIZE
    Map.append((x, y))
    
    for i in range(k-1, -1, -1):
        for j in range(len(BaseMap)-3, len(BaseMap)):
            x, y = BaseMap[j]
            x, y = x + 9*i * GRID_SIZE, y + 7*i * GRID_SIZE
            Map.append((x, y))
            
    drawLines(Map, color = "#000000", width = 2.5, tags = "map")

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
    start_time = time.time()
    if not Graph: Graph = createGraph(Map)
    #print(startCoord, endCoord)
    addStartEnd(Map, Graph, startCoord, endCoord)
    
    global Path
    Path, Distance = findPath(Graph)
    #print(Path)
    taken_time = time.time() - start_time
    status_log.set(f"Created graph and found shortest path found in {(taken_time):.5f} s. Distance: {(Distance / GRID_SIZE):.2f}")
    drawGraph("path")
    
def drawGraph(tags = "graph"):
    canvas.delete(tags)
    if tags == "path":
        global Path
        x1, y1 = (), ()
        for u in Path:
            if u == -2: x2, y2 = startCoord
            elif u == -1: x2, y2 = endCoord
            else: x2, y2 = Map[u]
            if x1: 
                #print(x1, y1, x2, y2)
                canvas.create_line(x1, y1, x2, y2, fill = "#2563eb", width = GRID_SIZE / PADDING, tags = "path")
            x1, y1 = x2, y2
    elif tags == "graph":
        if not Map: return
        global Graph
        if not Graph: Graph = createGraph(Map)
        for u in Graph:
            for v in Graph[u]:
                if v < u: continue
                canvas.create_line(Map[u], Map[v], fill = "#000000", tags = "graph")
        

def drawGrid():
    MAP_WIDTH = CAV_WIDTH // GRID_SIZE
    MAP_HEIGHT = CAV_HEIGHT // GRID_SIZE
    
    for i in range(MAP_WIDTH + 1):
        canvas.create_line(i * GRID_SIZE, 0, i * GRID_SIZE, CAV_HEIGHT, fill = GRID_COLOR, tags = "grid")   
    for i in range(MAP_HEIGHT + 1):
        canvas.create_line(0, i * GRID_SIZE, CAV_WIDTH, i * GRID_SIZE, fill = GRID_COLOR, tags = "grid") 

def drawLines(verts, color, width, tags):
    #canvas.create_polygon(Map[:-1], fill = "#ddeeff", tags = "map")
    u = ()
    for v in verts:
        #print(v)
        drawPoint(v, tags)
        if u: 
            canvas.create_line(u, v, fill = color, width = width, tags = tags)
        u = v
        
def drawPoint(vertice, tags):
    x, y = vertice
    if tags == "start_point": 
        #print(x, y)
        canvas.delete("start_point")
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = START_COLOR, outline = "", tags = "start_point")
    if tags == "end_point": 
        #print(x, y)
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = END_COLOR, outline = "", tags = "end_point")

def drawCursor(x, y):
    global editStart, editEnd
    canvas.delete("cursor_preview")
    if not editStart and not editEnd: return
    if editStart:
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = "#9fff93", outline = "", tags = "cursor_preview")
    elif editEnd:
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = "#ffd7a6", outline = "", tags = "cursor_preview")
    
def on_left_click(event):
    if len(Map) > 2:                            
        x, y = event.x, event.y
        if inPolygon(Map, (x, y), (x, y)):
            #print(x, y)
            global editStart, editEnd
            if editStart: 
                global startCoord
                startCoord = x, y
                startpoint_log.set(f"Start point: ({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f}).")
                editStart = False
            elif editEnd:
                global endCoord
                endCoord = x, y
                endpoint_log.set(f"End point: ({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f}).")
                editEnd = False
        else:
            status_log.set("Invalid point!")
    updateCanvas()

def on_cursor_move(event):
    x, y = event.x, event.y
    cursor_log.set(f"Cursor: ({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f}).")
    drawCursor(x, y)

if __name__ == "__main__":
    main()