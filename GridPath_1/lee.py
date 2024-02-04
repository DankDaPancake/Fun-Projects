fi = open('temp.inp', 'r')
fo = open('temp.out', 'w')

import tkinter
import math

Base_Map, Map, Graph = [], [], []
Vertices = []

def main():
    window = tkinter.Tk()
    window.title('Draw Graph')
    global WIN_WIDTH
    global WIN_HEIGHT
    WIN_WIDTH = window.winfo_screenwidth() * 4 / 5
    WIN_HEIGHT = window.winfo_screenheight() * 4 / 5
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
    
    root_frame =  tkinter.Frame(window).pack(padx = 5, pady = 5)
    
    menu_frame = tkinter.Frame(root_frame)
    menu_frame.pack(side = tkinter.TOP, padx = 5, pady = 5, fill = "x")
    
    map_menu = tkinter.Frame(menu_frame)
    map_menu.pack(side = tkinter.LEFT)

    tkinter.Button(map_menu, text="Duplicate", command=duplicate).pack(
        side=tkinter.LEFT, padx = 5
    )
    tkinter.Button(map_menu, text="Clear Map", command=mapclear).pack(
        side=tkinter.LEFT, padx = 5
    )
    tkinter.Button(map_menu, text="Show Graph", command=create_graph).pack(
        side=tkinter.LEFT, padx = 5
    )
    
    global canvas
    canvas = tkinter.Canvas(root_frame, bg = "#ffffff")
    canvas.pack(padx = 5, pady = 5, expand = True, fill = "both")

    global CAV_WIDTH
    global CAV_HEIGHT
    canvas.update()
    CAV_WIDTH = canvas.winfo_width()
    CAV_HEIGHT = canvas.winfo_height()
    
    status_frame = tkinter.Frame(root_frame)
    status_frame.pack(side = tkinter.BOTTOM, padx = 5, pady = 5, fill = "x")
    
    global cursor_coords_log
    cursor_coords_log = tkinter.StringVar()
    cursor_coords_log.set("(0; 0)")
    tkinter.Label(
        status_frame, textvariable=cursor_coords_log
    ).pack(side=tkinter.RIGHT, padx = 5)
    
    canvas.bind("<Motion>", on_mouse_move)
    
    draw_grid()
    scan_map()
    update_map()
    window.mainloop()
    
def draw_grid():
    MAP_WIDTH = CAV_WIDTH // 20
    MAP_HEIGHT = CAV_HEIGHT // 20
    
    for i in range(MAP_WIDTH + 1):
        canvas.create_line(i * 20, 0, i * 20, CAV_HEIGHT, fill = "#d4d4d4", tags = "grid")   
    for i in range(MAP_HEIGHT + 1):
        canvas.create_line(0, i * 20, CAV_WIDTH, i * 20, fill = "#d4d4d4", tags = "grid") 
    
def update_map():
    canvas.delete("point", "line")
    for [ux, uy, vx, vy] in Map: 
        #fo.write(str(ux) + " " + str(uy) + " " + str(vx) + " " + str(vy) + "\n")
        ux, uy = ux * 20, uy * 20
        vx, vy = vx * 20, vy * 20
        canvas.create_oval(ux-3, uy-3, ux+3, uy+3, fill="#ff4f00", outline="", tags = "point")
        canvas.create_oval(vx-3, vy-3, vx+3, vy+3, fill="#ff4f00", outline="", tags = "point")
        canvas.create_line(ux, uy, vx, vy, fill = "#2563eb", width = 2.5, tags = "line")
    #fo.write("\n")
        
def scan_map():
    for line in fi.read().split("\n"):
        ux, uy, vx, vy = map(int, line.split(" "))
        if ux > vx: 
            ux, uy, vx, vy = vx, vy, ux, uy 
        if ux == vx and uy > vy:
            uy, vy = vy, uy
        Base_Map.append([ux, uy, vx, vy])
              
def duplicate():
    dupes = len(Map) // 25
    if dupes > 0: 
        del Map[-7:-4]
    for [ux, uy, vx, vy] in Base_Map:
        ux, uy = ux + dupes * 9, uy + dupes * 8
        vx, vy = vx + dupes * 9, vy + dupes * 8
        Map.append([ux, uy, vx, vy])
    if dupes > 0:
        del Map[-3:]
        dx, dy = (dupes - 1) * 9, (dupes - 1) * 8
        Map.append([11 + dx, 7 + dy, 11 + dx, 15 + dy])
        Map.append([10 + dx, 8 + dy, 10 + dx, 16 + dy])
        Map.append([1, 1, 1, 1])
    update_map()

def mapclear():
    canvas.delete("point", "line", "graph")
    Map.clear()
    Graph.clear()

def draw_graph():
    canvas.delete("graph")
    for [ux, uy, vx, vy] in Graph:
        fo.write(str(ux) + " " + str(uy) + " " + str(vx) + " " + str(vy) + "\n")
        ux, uy = ux * 20, uy * 20
        vx, vy = vx * 20, vy * 20
        canvas.create_line(ux, uy, vx, vy, fill = "#000000", width = 1, tags = "graph")

def orientation(a, b, c):
    xa, ya = a
    xb, yb = b
    xc, yc = c
    val = (xc - xb) * (yb - ya) - (xb - xa) * (yc - yb)
    return 1 if val > 0 else 2 if val < 0 else 0


def on_segment(a, b, c):
    xa, ya = a
    xb, yb = b
    xc, yc = c
    return (
        xb <= max(xa, xc)
        and xb >= min(xa, xc)
        and yb <= max(ya, yc)
        and yb >= min(ya, yc)
    )


def intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def addEdge(p1, q1):
    for [p2, q2] in Map:
        if intersect(p1, q1, p2, q2):
            return
    fo.write(str(p1[0]) + " " + str(p1[1]) + " " + str(q1[0]) + " " + str(q1[1]) + "\n")
    Graph.append([p1[0], p1[1], q1[0], q1[1]])

def create_graph():
    for [ux, uy, vx, vy] in Map:
        Vertices.append([ux, uy])
        Vertices.append([vx, vy])
    #for [ux, uy] in Vertices:
        #fo.write(str(ux) + " " + str(uy) + "\n")
    
    n = len(Vertices)
    fo.write(str(n) + "\n")
    Vertices = sorted(Vertices)
    for i in range(n):
        if i > 0 and Vertices[i] == Vertices[i-1]: continue
        for j in range(i+1, n):
            if j > 1 and Vertices[j] == Vertices[j-1]: continue
            #fo.write(str(ux) + " " + str(uy) + " " + str(vx) + " " + str(vy) + "\n")    
            addEdge(Vertices[i], Vertices[j])
    draw_graph()
    
def on_mouse_move(event):
    cursor_coords_log.set(f"({event.x:d}; {event.y:d})")
    
if __name__ == "__main__":
    main()