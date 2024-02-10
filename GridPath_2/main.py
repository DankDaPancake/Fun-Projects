fi = open('temp.inp', 'r')

import tkinter as Tk
from geometry import in_polygon, intersect
from graph import addEdge, createGraph, find_path

Map, Graph, Path = [], {}, []
Vertices = []
GRID_SZ = 25

def main():
    window = Tk.Tk()
    window.title('Draw Graph')
    global WIN_WIDTH
    global WIN_HEIGHT
    WIN_WIDTH = window.winfo_screenwidth() * 2 / 3
    WIN_HEIGHT = window.winfo_screenheight() * 2 / 3
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

    Tk.Button(map_menu1, text = "Clear Map", command = mapclear).pack(
        side = Tk.LEFT, padx = 10
    )
    Tk.Button(map_menu1, text = "Show Graph", command = MapToEdge).pack(
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
    
    status_frame = Tk.Frame(root_frame)
    status_frame.pack(side = Tk.BOTTOM, padx = 5, pady = 5, fill = "x")
    
    global cursor_coords_log
    cursor_coords_log = Tk.StringVar()
    cursor_coords_log.set("(0; 0)")
    Tk.Label(
        status_frame, textvariable=cursor_coords_log
    ).pack(side=Tk.RIGHT, padx = 5)
    
    global start_pin
    start_pin = False
    global start_coords
    start_coords = (0, 0)
    
    global end_pin
    end_pin = False
    global end_coords 
    end_coords = (0, 0)
    
    canvas.bind("<Motion>", move)
    canvas.bind("<Button-1>", left_click)
    
    draw_grid()
    scan_map()
    update_map()
    window.mainloop()

def pin_start():
    global start_pin
    start_pin = True

def pin_end():
    global start_pin
    if start_pin: 
        exit
    global end_pin
    end_pin = True
    
def draw_grid():
    MAP_WIDTH = CAV_WIDTH // GRID_SZ
    MAP_HEIGHT = CAV_HEIGHT // GRID_SZ
    
    for i in range(MAP_WIDTH + 1):
        canvas.create_line(i * GRID_SZ, 0, i * GRID_SZ, CAV_HEIGHT, fill = "#d4d4d4", tags = "grid")   
    for i in range(MAP_HEIGHT + 1):
        canvas.create_line(0, i * GRID_SZ, CAV_WIDTH, i * GRID_SZ, fill = "#d4d4d4", tags = "grid") 
    
def update_map():
    canvas.delete("point", "line")
    ux, uy = -1, -1
    for [vx, vy] in Map: 
        if ux == -1:
            ux, uy = vx, vy
            continue
        ux, uy = ux * GRID_SZ, uy * GRID_SZ
        vx, vy = vx * GRID_SZ, vy * GRID_SZ
        canvas.create_line(ux, uy, vx, vy, fill = "#000000", width = GRID_SZ / 10, tags = "line")
        draw_point((ux, uy), "point")
        draw_point((vx, vy), "point")
        ux, uy = vx // GRID_SZ, vy // GRID_SZ
        
def scan_map():
    for line in fi.read().split("\n"):
        ux, uy= map(int, line.split(" "))
        Map.append([ux, uy])
    update_map()
    
def mapclear():
    canvas.delete("point", "line", "graph")
    Map.clear()
    Graph.clear()

def left_click(event):
    x, y = float(event.x / GRID_SZ), float(event.y / GRID_SZ)
    if in_polygon(Map, (x, y), (x, y)):
        global start_pin
        global end_pin
        if start_pin: 
            global start_coords
            start_coords = x, y
            draw_point((x * GRID_SZ, y * GRID_SZ), "start_point")
            start_pin = False
        elif end_pin:
            global end_coords
            end_coords = x, y
            draw_point((x * GRID_SZ, y * GRID_SZ), "end_point")
            end_pin = False
            
def move(event):
    cursor_coords_log.set(f"({event.x:d}; {event.y:d})")
    
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

def MapToEdge():
    createGraph(Map, Graph)
    draw_graph("graph")

def draw_point(vertice, tags):
    canvas.delete("graph")
    x, y = vertice
    if tags == "point": canvas.create_oval(x-3, y-3, x+3, y+3, fill="#ff4f00", outline="", tags = "point")
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
    if start_coords == (0, 0) or end_coords == (0, 0):
        print("Pick your starting and ending point!")
        return
    
    createGraph(Map, Graph)     
    for i in range(len(Map)):
        addEdge(Map, Graph, -2, i, start_coords, Map[i])
        addEdge(Map, Graph, -1, i, end_coords, Map[i])
    addEdge(Map, Graph, -2, -1, start_coords, end_coords)
    Map.append(start_coords)
    Map.append(end_coords)
    global Path
    Path = find_path(Graph)
    draw_graph("path")

def reset():
    Graph.clear()
    Path.clear()
    start_coords = (0, 0)
    end_coords = (0, 0)
    canvas.delete("graph", "path", "start_point", "end_point")
    if Map[-2] == start_coords and Map[-1] == end_coords:
        Map.pop()
        Map.pop()
    

if __name__ == "__main__":
    main()