fi = open('temp.inp', 'r')

import tkinter as Tk
import time
from presets import *
from geometry import inPolygon, intersect, snapPoint, orientation
from graph import createGraph, find_path, addStartEnd, removeStartEnd

Map, Graph, Path = [], {}, []
editMap = True
startCoord, endCoord = (), ()
isStart, isEnd = False, False

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
        % (
            WIN_WIDTH,
            WIN_HEIGHT,
            window.winfo_screenwidth() / 2 - WIN_WIDTH / 2,
            window.winfo_screenheight() / 2 - WIN_HEIGHT / 2,
        )
    )
    
    root_frame =  Tk.Frame(window).pack(padx = PADDING, pady = PADDING / 2)
    
    menu_frame = Tk.Frame(root_frame)
    menu_frame.pack(side = Tk.TOP, padx = PADDING, pady = PADDING / 2, fill = "x")
    
    map_menu1 = Tk.Frame(menu_frame)
    map_menu1.pack(side = Tk.LEFT)
    
    map_menu2 = Tk.Frame(menu_frame)
    map_menu2.pack(side = Tk.LEFT)
    
    Tk.Button(map_menu1, text = "Edit Map", command = edit_map).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu2, text = "Pick Start", command = pinStart).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu2, text = "Pick End", command = pinEnd).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu1, text = "Find Path", command = findPath).pack(side = Tk.LEFT, padx = PADDING)
    Tk.Button(map_menu1, text = "Reset", command = reset).pack(side = Tk.LEFT, padx = PADDING)
    
    global canvas
    canvas = Tk.Canvas(root_frame, bg = "#ffffff")
    canvas.pack(padx = PADDING, pady = PADDING / 2, expand = True, fill = "both")

    global CAV_WIDTH
    global CAV_HEIGHT
    canvas.update()
    CAV_WIDTH = canvas.winfo_width()
    CAV_HEIGHT = canvas.winfo_height()
    
    log_frame = Tk.Frame(root_frame)
    log_frame.pack(side = Tk.BOTTOM, padx = PADDING, pady = PADDING / 2, fill = "x")
    
    global log
    log = Tk.StringVar()
    Tk.Label(log_frame, textvariable = log).pack(side = Tk.LEFT, padx = PADDING)
    
    global cursor_log
    cursor_log = Tk.StringVar()
    cursor_log.set("(0; 0)")
    Tk.Label(log_frame, textvariable = cursor_log).pack(side = Tk.RIGHT, padx = PADDING)
    
    global startpoint_log
    startpoint_log = Tk.StringVar()
    startpoint_log.set("Start point: (0; 0).")
    Tk.Label(log_frame, textvariable = startpoint_log).pack(side = Tk.RIGHT, padx = PADDING)
    
    global endpoint_log
    endpoint_log = Tk.StringVar()
    endpoint_log.set("End point: (0; 0).")
    Tk.Label(log_frame, textvariable = endpoint_log).pack(side = Tk.RIGHT, padx = PADDING)
    
    canvas.bind("<Motion>", move)
    canvas.bind("<Button-1>", left_click)
    
    drawGrid()
    updateCanvas()
    window.mainloop()

def updateCanvas():
    
    '''if not editMap:
        for u in Graph:
            for v in Graph[u]:
                if v < u: continue
                canvas.create_line(Map[u], Map[v], fill = "#000000", tags = "graph")
    '''
    
    drawLines(Map, "#000000", 2.5, tags = "map")
    if startCoord: drawPoint(startCoord, "start_point")
    if endCoord: drawPoint(endCoord, "end_point")
    
def pinStart():
    canvas.delete("preview")
    global editMap, editStart, editEnd
    editMap = False
    editStart = True
    editEnd = False

def pinEnd():
    canvas.delete("preview")
    global editMap, editStart, editEnd
    editMap = False
    editEnd = True
    editStart = False
    
def drawGrid():
    MAP_WIDTH = CAV_WIDTH // GRID_SIZE
    MAP_HEIGHT = CAV_HEIGHT // GRID_SIZE
    
    for i in range(MAP_WIDTH + 1):
        canvas.create_line(i * GRID_SIZE, 0, i * GRID_SIZE, CAV_HEIGHT, fill = GRID_COLOR, tags = "grid")   
    for i in range(MAP_HEIGHT + 1):
        canvas.create_line(0, i * GRID_SIZE, CAV_WIDTH, i * GRID_SIZE, fill = GRID_COLOR, tags = "grid") 

def drawLines(lines, color, width, tags):
    u = ()
    for v in lines:
        drawPoint(v, tags)
        if u: 
            canvas.create_line(u, v, fill = color, width = width, tags = tags)
        u = v
    
def edit_map():
    global editMap
    if editMap:
        return
    
    reset()
    if Map:
        Map.pop()
    editMap = True
    updateCanvas()
    
def drawGraph(tags):
    canvas.delete(tags)
    if tags == "path":
        global Path
        x1, y1 = (), ()
        for u in Path:
            if u == -2: 
                x2, y2 = startCoord
            elif u == -1:
                x2, y2 = endCoord
            else:
                x2, y2 = Map[u]
            if x1: 
                print(x1, y1, x2, y2)
                canvas.create_line(x1, y1, x2, y2, fill = "#2563eb", width = GRID_SIZE / PADDING, tags = "path")
            x1, y1 = x2, y2
        return

def drawPoint(vertice, tags):
    x, y = vertice
    log.set(f"Point snapped on {x // GRID_SIZE, y / GRID_SIZE}")
    if tags == "map": canvas.create_oval(x-3, y-3, x+3, y+3, fill = MAP_COLOR, outline = "", tags = tags)
    if tags == "start_point": 
        #print(x, y)
        canvas.delete("start_point")
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = START_COLOR, outline = "", tags = "start_point")
    if tags == "end_point": 
        #print(x, y)
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill = END_COLOR, outline = "", tags = "end_point")

def drawCursor(x1, y1):
    x2, y2 = Map[-1]
    canvas.delete("preview")
    canvas.create_line(x1, y1, x2, y2, fill = "#949494", width = 2.5, tags = "preview")
    
def findPath():
    if not startCoord or not endCoord:
        log.set("Pick your starting and ending point!")
        return
    print(startCoord, endCoord)
    addStartEnd(Map, Graph, startCoord, endCoord)
    
    start_time = time.time()
    global Path
    Path = find_path(Graph)
    print(Path)
    taken_time = time.time() - start_time
    log.set(f"Path found in {(taken_time / 3):.10f} ms.")
    drawGraph("path")

def reset(state = True):
    global startCoord, endCoord, Path, Graph, Map
    if state:
        if Map[-2] == startCoord and Map[-1] == endCoord:
            del Map[-2:]
        startCoord = ()
        endCoord = ()
    
    Path = []
    removeStartEnd(Graph)

def left_click(event):
    global editMap
    if editMap:
        coords = snapPoint(event.x, event.y, GRID_SIZE)
        if Map:
            if coords in Map and (len(Map) == 1 or coords != Map[0]):
                while Map[-1] != coords:
                    Map.pop()
                Map.pop()
            else:
                intersected = False
                for i in range(len(Map) - 2):
                    if coords == Map[0] and i == 0:
                        continue
                    if intersect(Map[-1], coords, Map[i], Map[i+1]):
                        intersected = True
                        break
                    
                if not intersected:
                    if len(Map) > 2:
                        if orientation(Map[-2], Map[-1], coords) == 0:
                            Map.pop()
                        if coords == Map[0]:
                            if orientation(Map[-1], Map[0], Map[1]) == 0:
                                Map.pop(0)
                            Map.append(Map[0])
                            
                            editMap = False
                            global Graph
                            Graph = createGraph(Map)
                        else:
                            Map.append(coords)
                    elif coords != Map[0]:
                        Map.append(coords)
                else: 
                    log.set("Line intersected.")
        else: 
            Map.append(coords)
    elif len(Map) > 2:                            
        x, y = event.x, event.y
        if inPolygon(Map, (x, y), (x, y)):
            print(x, y)
            reset(False)
            global editStart
            global editEnd
            if editStart: 
                global startCoord
                startCoord = x, y
                startpoint_log.set(f"Start point: ({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f}).")
            elif editEnd:
                global endCoord
                endCoord = x, y
                endpoint_log.set(f"End point: ({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f}).")
        else:
            log.set("Invalid point!")
    else: 
        editMap = True
    
    updateCanvas()

def move(event):
    x, y = event.x, event.y
    cursor_log.set(f"({(x / GRID_SIZE):.2f}; {(y / GRID_SIZE):.2f})")
    x, y = snapPoint(x, y, GRID_SIZE)
    if Map and editMap: drawCursor(x, y)

if __name__ == "__main__":
    main()