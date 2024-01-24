fi = open('temp.inp', 'r')
fo = open('temp.out', 'w')

import tkinter
import math

Base_Graph, Graph, Prev_Graph = [], [], []

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
    tkinter.Button(map_menu, text="Undo", command=undo).pack(
        side=tkinter.LEFT, padx = 5
    )
    tkinter.Button(map_menu, text="Clear Map", command=mapclear).pack(
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
    
    scan_graph()
    draw_grid()
    update_canvas()
    window.mainloop()
    
def draw_grid():
    MAP_WIDTH = CAV_WIDTH // 20
    MAP_HEIGHT = CAV_HEIGHT // 20
    
    for i in range(MAP_WIDTH + 1):
        canvas.create_line(i * 20, 0, i * 20, CAV_HEIGHT, fill = "#d4d4d4", tags = "grid")   
    for i in range(MAP_HEIGHT + 1):
        canvas.create_line(0, i * 20, CAV_WIDTH, i * 20, fill = "#d4d4d4", tags = "grid") 
    
def update_canvas():
    canvas.delete("point", "line")
    for [ux, uy, vx, vy] in Graph: 
        fo.write(str(ux) + " " + str(uy) + " " + str(vx) + " " + str(vy) + "\n")
        ux, uy = ux * 20, uy * 20
        vx, vy = vx * 20, vy * 20
        canvas.create_oval(ux-3, uy-3, ux+3, uy+3, fill="#ff4f00", outline="", tags = "point")
        canvas.create_oval(vx-3, vy-3, vx+3, vy+3, fill="#ff4f00", outline="", tags = "point")
        canvas.create_line(ux, uy, vx, vy, fill = "#2563eb", width = 2.5, tags = "line")
    fo.write("\n")
        
def scan_graph():
    for line in fi.read().split("\n"):
        ux, uy, vx, vy = map(int, line.split(" "))
        Base_Graph.append([ux, uy, vx, vy])
              
def duplicate():
    Prev_Graph = Graph[:]
    dupes = len(Graph) // 25
    if dupes > 0: 
        del Graph[-7:-4]
    for [ux, uy, vx, vy] in Base_Graph:
        ux, uy = ux + dupes * 9, uy + dupes * 8
        vx, vy = vx + dupes * 9, vy + dupes * 8
        Graph.append([ux, uy, vx, vy])
    if dupes > 0:
        del Graph[-3:]
        dx, dy = (dupes - 1) * 9, (dupes - 1) * 8
        Graph.append([11 + dx, 7 + dy, 11 + dx, 15 + dy])
        Graph.append([10 + dx, 8 + dy, 10 + dx, 16 + dy])
        Graph.append([1, 1, 1, 1])
    update_canvas()

def undo():
    if len(Graph) == 0: exit
    temp = list(Graph)
    Graph = list(Prev_Graph)
    Prev_Graph = list(temp)
    update_canvas()

def mapclear():
    canvas.delete("point", "line")
    Graph.clear()
    
def on_mouse_move(event):
    cursor_coords_log.set(f"({event.x:d}; {event.y:d})")
    
if __name__ == "__main__":
    main()