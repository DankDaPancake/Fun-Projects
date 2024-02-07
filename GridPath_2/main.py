fi = open('temp.inp', 'r')

import tkinter as Tk
from geometry import intersect, in_polygon, euclidean_dist
from queue import PriorityQueue as priorQ

Map, Graph = [], {}
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
    Tk.Button(map_menu1, text = "Show Graph", command = create_graph).pack(
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
        #fo.write(str(ux) + " " + str(uy) + " " + str(vx) + " " + str(vy) + "\n")
        if ux == -1:
            ux, uy = vx, vy
            continue
        ux, uy = ux * GRID_SZ, uy * GRID_SZ
        vx, vy = vx * GRID_SZ, vy * GRID_SZ
        draw_point((ux, uy), "point")
        draw_point((vx, vy), "point")
        canvas.create_line(ux, uy, vx, vy, fill = "#2563eb", width = GRID_SZ / 10, tags = "line")
        ux, uy = vx // GRID_SZ, vy // GRID_SZ
    #fo.write("\n")
        
def scan_map():
    for line in fi.read().split("\n"):
        ux, uy= map(int, line.split(" "))
        Map.append([ux, uy])
    update_map()
    
def mapclear():
    canvas.delete("point", "line", "graph")
    Map.clear()
    Graph.clear()

def draw_graph():
    canvas.delete("graph")
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
            canvas.create_line(x1 * GRID_SZ, y1 * GRID_SZ, x2 * GRID_SZ, y2 * GRID_SZ, fill = "#000000", width = 1.2, tags = "graph")
    
def addEdge(u, v, p1, q1):
    intersected = False
    p2 = -1, -1
    for q2 in Map:
        if p2 == [-1, -1]:
            p2 = q2
            continue        
        if intersect(p1, q1, p2, q2) or not in_polygon(Map, (p1[0] + q1[0]) / 2, (p1[1] + q1[1]) / 2):
            intersected = True
            break
        p2 = q2    
    if intersected: 
        return
    
    distance = euclidean_dist(p1, q1)
    if u not in Graph: 
        Graph[u] = {}
    Graph[u][v] = distance
    if v not in Graph:
        Graph[v] = {}
    Graph[v][u] = distance

def create_graph():
    if len(Graph): 
        exit
    n = len(Map)
    for i in range(n):
        p1 = Map[i]
        for j in range(i+1, n):
            q1 = Map[j]
            addEdge(i, j, p1, q1)
    draw_graph()

def pin_start():
    global start_pin
    start_pin = True

def pin_end():
    global start_pin
    if start_pin: 
        exit
    global end_pin
    end_pin = True

def draw_point(vertice, tags):
    canvas.delete("graph")
    x, y = vertice
    if tags == "point": canvas.create_oval(x-3, y-3, x+3, y+3, fill="#ff4f00", outline="", tags = "point")
    if tags == "start_point": 
        print(x, y)
        canvas.delete("start_point")
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="#5ec12b", outline="", tags = "start_point")
    if tags == "end_point": 
        print(x, y)
        canvas.delete("end_point")
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="#f2c04f", outline="", tags = "end_point")

def find_path():
    pq = priorQ()
    pq.put((start_coords, 0))
    while len(pq):
        point, dist = pq.get()
        
def draw_path():
    if start_coords == (0, 0) or end_coords == (0, 0):
        print("Pick a start and an end")
        return
    for i in range(len(Map)):
        addEdge(i, -2, Map[i], start_coords)
        addEdge(i, -1, Map[i], end_coords)
    addEdge(-1, -2, start_coords, end_coords)
    Map.append(start_coords)
    Map.append(end_coords)
    create_graph()
    
def left_click(event):
    x, y = float(event.x / GRID_SZ), float(event.y / GRID_SZ)
    if in_polygon(Map, x, y):
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

if __name__ == "__main__":
    main()