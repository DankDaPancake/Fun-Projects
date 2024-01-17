fi = open('temp.inp', 'r')

import tkinter

graph = []
dupes = 0

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
    update_canvas()
    window.mainloop()
    
def draw_grid():
    MAP_WIDTH = CAV_WIDTH // 20
    MAP_HEIGHT = CAV_HEIGHT // 20
    print(CAV_WIDTH, CAV_HEIGHT)
    
    for i in range(MAP_WIDTH + 1):
        canvas.create_line(i * 20, 0, i * 20, CAV_HEIGHT, fill = "#d4d4d4")   
    for i in range(MAP_HEIGHT + 1):
        canvas.create_line(0, i * 20, CAV_WIDTH, i * 20, fill = "#d4d4d4") 
    
def update_canvas():
    n = int(fi.readline())
    ux, uy = None, None
    for _ in range(n): 
        vx, vy = map(int, fi.readline().split())
        vx *= 20
        vy *= 20
        graph.append((vx, vy))
        canvas.create_oval(vx-3, vy-3, vx+3, vy+3, fill="#2563eb", outline="")
        if ux != None:
            canvas.create_line(ux, uy, vx, vy, fill = "#2563eb", width = 2.5)
        ux, uy = vx, vy

def duplicate():
    dupes += 1
    print(dupes)
    n = graph.len()
    for _ in range(n): 
        vx, vy = map(int, fi.readline().split())
        vx *= 20 + (dupes * 10)
        vy *= 20 + (dupes * 9)
        graph.append((vx, vy))
        canvas.create_oval(vx-3, vy-3, vx+3, vy+3, fill="#2563eb", outline="")
        if ux != None:
            canvas.create_line(ux, uy, vx, vy, fill = "#2563eb", width = 2.5)
        ux, uy = vx, vy
    
def on_mouse_move(event):
    cursor_coords_log.set(f"({event.x:d}; {event.y:d})")
    
if __name__ == "__main__":
    main()