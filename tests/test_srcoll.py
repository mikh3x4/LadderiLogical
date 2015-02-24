import tkinter as tk
import random

class Example(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(self, width=400, height=400, background="bisque")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,1000,1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        for n in range(50):
            x0 = random.randint(0, 900)
            y0 = random.randint(50, 900)
            x1 = x0 + random.randint(50, 100)
            y1 = y0 + random.randint(50,100)
            color = ("red", "orange", "yellow", "green", "blue")[random.randint(0,4)]
            self.canvas.create_rectangle(x0,y0,x1,y1, outline="black", fill=color)
        self.canvas.create_text(50,10, anchor="nw", 
                                text="Click and drag to move the canvas")

        # This is what enables scrolling with the mouse:
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind('<Motion>',self.motion)



    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def motion(self,event):
        print("Mouse position: (%s %s)" % (event.x, event.y))
        return


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()