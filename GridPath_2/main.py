fi = open('temp.inp', 'r')

import tkinter as Tk
import time
from geometry import in_polygon, intersect, snap_point, orientation
from graph import addEdge, createGraph, find_path

Map, Graph, Path = [], {}, []
GRID_SZ = 25
editing_map = True
start_coords, end_coords = (), ()

def main():
    window = Tk.Tk()
    window.title('Draw Graph')
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
    
    root_frame =  Tk.Frame(window).pack(padx = 5, pady = 5)
    
    menu_frame = Tk.Frame(root_frame)
    menu_frame.pack(side = Tk.TOP, padx = 5, pady = 5, fill = "x")
    
    map_menu1 = Tk.Frame(menu_frame)
    map_menu1.pack(side = Tk.LEFT)
    
    map_menu2 = Tk.Frame(menu_frame)
    map_menu2.pack(side = Tk.LEFT)
    
    Tk.Button(map_menu1, text = "Edit Map", command = edit_map).pack(
        side = Tk.LEFT, padx = 10
    )
    Tk.Button(map_menu2, text = "Pick Start", command = pin_start).pack(
        side = Tk.LEFT, padx = 10
    )
    Tk.Button(map_menu2, text = "Pick End", command = pin_end).pack(
        side = Tk.LEFT, padx = 10
    )
    Tk.Button(map_menu1, text = "Find Path", command = draw_path).pack(
        side = Tk.LEFT, padx = 10
    )
    Tk.Button(map_menu1, text = "Reset", command = reset).pack(
        side = Tk.LEFT, padx = 10
    )
    
    global canvas
    canvas = Tk.Canvas(root_frame, bg = "#ffffff")
    canvas.pack(padx = 5, pady = 5, expand = True, fill = "both")

    global CAV_WIDTH
    global CAV_HEIGHT
    canvas.update()
    CAV_WIDTH = canvas.winfo_width()
    CAV_HEIGHT = canvas.winfo_height()
    
    log_frame = Tk.Frame(root_frame)
    log_frame.pack(side = Tk.BOTTOM, padx = 5, pady = 5, fill = "x")
    
    global log
    log = Tk.StringVar()
    Tk.Label(log_frame, textvariable = log).pack(side = Tk.LEFT, padx = 5)
    
    global cursor_log
    cursor_log = Tk.StringVar()
    cursor_log.set("(0; 0)")
    Tk.Label(log_frame, textvariable = cursor_log).pack(side = Tk.RIGHT, padx = 5)
    
    global startpoint_log
    startpoint_log = Tk.StringVar()
    Tk.Label(log_frame, textvariable = startpoint_log).pack(side = Tk.RIGHT, padx = 5)
    
    global endpoint_log
    endpoint_log = Tk.StringVar()
    Tk.Label(log_frame, textvariable = endpoint_log).pack(side = Tk.RIGHT, padx = 5)
    
    canvas.bind("<Motion>", move)
    canvas.bind("<Button-1>", left_click)
    
    drawGrid()
    updateCanvas()
    window.mainloop()

def updateCanvas():
    '''
    if not editing_map:
        for u in Graph:
            for v in Graph[u]:
                if v < u: continue
                canvas.create_line(Map[u], Map[v], fill = "#000000", tags = "graph")
    '''
    drawLines(Map, "#000000", 2.5, tags = "map")
    
def pin_start():
    global start_pin
    start_pin = True

def pin_end():
    global start_pin
    if start_pin: 
        exit
    global end_pin
    end_pin = True
    
def drawGrid():
    MAP_WIDTH = CAV_WIDTH // GRID_SZ
    MAP_HEIGHT = CAV_HEIGHT // GRID_SZ
    
    for i in range(MAP_WIDTH + 1):
        canvas.create_line(i * GRID_SZ, 0, i * GRID_SZ, CAV_HEIGHT, fill = "#d4d4d4", tags = "grid")   
    for i in range(MAP_HEIGHT + 1):
        canvas.create_line(0, i * GRID_SZ, CAV_WIDTH, i * GRID_SZ, fill = "#d4d4d4", tags = "grid") 

def drawLines(lines, color, width, tags):
    u = ()
    for v in lines:
        drawPoint(v, tags)
        if u: 
            canvas.create_line(u, v, fill = color, width = width, tags = tags)
        u = v
    
def edit_map():
    global editing_map
    if editing_map:
        return
    
    reset(True)
    if map:
        map.pop()
    editing_map = True
    draw_graph()
    
def draw_graph(tags):
    canvas.delete(tags)
    if tags == "path":
        global Path
        x1, y1 = None, None
        for u in Path:
            if u == -2: 
                x2, y2 = start_coords
            elif u == -1:
                x2, y2 = end_coords
            else:
                x2, y2 = Map[u]
            if x1: 
                canvas.create_line(x1 * GRID_SZ, y1 * GRID_SZ, x2 * GRID_SZ, y2 * GRID_SZ, fill = "#2563eb", width = GRID_SZ / 10, tags = "path")
            x1, y1 = x2, y2
        return
                
    for u in Graph:
        if u == -2: 
            x1, y1 = start_coords
        elif u == -1:
            x1, y1 = end_coords
        else:
            x1, y1 = Map[u]
        for v in Graph[u]:
            if v < u: continue
            if v == -2:
                x2, y2 = start_coords
            elif v == -1:
                x2, y2 = end_coords
            else:
                x2, y2 = Map[v]
            canvas.create_line(x1 * GRID_SZ, y1 * GRID_SZ, x2 * GRID_SZ, y2 * GRID_SZ, fill = "#ff4f00", width = 1.25, tags = "graph")

def drawPoint(vertice, tags):
    x, y = vertice
    log.set(f"Point snapped on {x / GRID_SZ, y / GRID_SZ}")
    if tags == "map": canvas.create_oval(x-3, y-3, x+3, y+3, fill="#ff4f00", outline="", tags = tags)
    if tags == "start_point": 
        #print(x, y)
        canvas.delete("start_point")
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="#5ec12b", outline="", tags = "start_point")
    if tags == "end_point": 
        #print(x, y)
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="#f2c04f", outline="", tags = "end_point")
        
def draw_path():
    if not start_coords or not end_coords:
        log.set("Pick your starting and ending point!")
        return
    
    createGraph(Map, Graph)     
    for i in range(len(Map)):
        addEdge(Map, Graph, -2, i, start_coords, Map[i])
        addEdge(Map, Graph, -1, i, end_coords, Map[i])
    addEdge(Map, Graph, -2, -1, start_coords, end_coords)
    Map.append(start_coords)
    Map.append(end_coords)
    start_time = time.time()
    global Path
    Path = find_path(Graph)
    taken_time = time.time() - start_time
    log.set(f"Path found in {taken_time:.5f}s.")
    draw_graph("path")

def reset(state = True):
    global start_coords, end_coords, Path, Graph
    Graph.clear()
    Path.clear()
    if state:
        start_coords = ()
        end_coords = ()
    canvas.delete("graph", "path", "start_point", "end_point")
    if Map[-2] == start_coords and Map[-1] == end_coords:
        Map.pop()
        Map.pop()

def left_click(event):
    global editing_map
    if editing_map:
        coords = snap_point(event.x, event.y, GRID_SZ)
        if Map:
            if coords in Map and (len(Map) == 1 or coords != Map[0]):
                while Map[-1] != coords:
                    map.pop()
                map.pop()
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
                            
                            editing_map = False
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
    else:                            
        x, y = float(event.x / GRID_SZ), float(event.y / GRID_SZ)
        if in_polygon(Map, (x, y), (x, y)):
            reset(False)
            global start_pin
            global end_pin
            if start_pin: 
                global start_coords
                start_coords = x, y
                start_pin = False
            elif end_pin:
                global end_coords
                end_coords = x, y
                end_pin = False
        else:
            log.set("Invalid point!")
    
    updateCanvas()

            
def move(event):
    cursor_log.set(f"({event.x:d}; {event.y:d})")

if __name__ == "__main__":
    main()