import tkinter as tk


class Tile:

    def __init__(self,root,board,x,y):
        self.x=x
        self.y=y
        self.board=board

        self.bottom=tk.IntVar()
        self.top=tk.IntVar()
        self.left=tk.IntVar()
        self.right=tk.IntVar()


        self.bottom_input=0
        self.top_input=0
        self.left_input=0
        self.right_input=0


        self.state=0

        self.frame=tk.Frame(master=root)

        self.top_cheack=tk.Checkbutton(master=self.frame,text="Top",variable=self.top)
        self.bottom_cheack=tk.Checkbutton(master=self.frame,text="Bottom",variable=self.bottom)
        self.left_cheack=tk.Checkbutton(master=self.frame,text="Left",variable=self.left)
        self.right_cheack=tk.Checkbutton(master=self.frame,text="Right",variable=self.right)


        self.label=tk.Label(master=self.frame,text=str(self.state))

        self.top_cheack.pack()
        self.bottom_cheack.pack()
        self.left_cheack.pack()
        self.right_cheack.pack()
        self.label.pack()

        self.on_box=self.board.canvas.create_rectangle(self.x*self.board.tile_size,self.y*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")

        self.top_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y)*self.board.tile_size,fill="")
        self.bottom_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="")
        self.left_box=self.board.canvas.create_line((self.x)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="")
        self.right_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="")


        

    def update(self):

        try:
            if(self.state==1 and self.top.get()==1):
                self.board.tiles[self.x][self.y-1].bottom_input=1
            else:
                self.board.tiles[self.x][self.y-1].bottom_input=0
        except IndexError:
            pass

        try:
            if(self.state==1 and self.bottom.get()==1):
                self.board.tiles[self.x][self.y+1].top_input=1
            else:
                self.board.tiles[self.x][self.y+1].top_input=0
        except IndexError:
            pass

        try:
            if(self.state==1 and self.left.get()==1):
                self.board.tiles[self.x-1][self.y].right_input=1
            else:
                self.board.tiles[self.x-1][self.y].right_input=0
        except IndexError:
            pass

        try:
            if(self.state==1 and self.right.get()==1):
                self.board.tiles[self.x+1][self.y].left_input=1
            else:
                self.board.tiles[self.x+1][self.y].left_input=0
        except IndexError:
            pass



        if(self.bottom_input==1 or self.top_input==1 or self.left_input==1 or self.right_input==1):
            self.state=1
            self.board.canvas.itemconfig(self.on_box,fill="#FF0000")
        else:
            self.board.canvas.itemconfig(self.on_box,fill="")
            self.state=0


        if(self.top.get()==1):
            self.board.canvas.itemconfig(self.top_box,fill="#00FF00")
        else:
            self.board.canvas.itemconfig(self.top_box,fill="")

        if(self.bottom.get()==1):
            self.board.canvas.itemconfig(self.bottom_box,fill="#00FF00")
        else:
            self.board.canvas.itemconfig(self.bottom_box,fill="")

        if(self.left.get()==1):
            self.board.canvas.itemconfig(self.left_box,fill="#00FF00")
        else:
            self.board.canvas.itemconfig(self.left_box,fill="")

        if(self.right.get()==1):
            self.board.canvas.itemconfig(self.right_box,fill="#00FF00")
        else:
            self.board.canvas.itemconfig(self.right_box,fill="")


        self.label.config(text=str(self.state))


class TileBoard(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.total_size_x=self.total_size_y=1000
        self.size_x=self.size_y=400
        self.tile_size=50

        self.canvas = tk.Canvas(self, width=self.size_x, height=self.size_y, background="#F0EAD6")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,self.total_size_x,self.total_size_y))



        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.tiles=[[Tile(root,self,r,i) for i in range(self.total_size_y//self.tile_size)] for r in range(self.total_size_x//self.tile_size)]


        self.canvas.bind("<ButtonPress-1>", self.click)
        self.canvas.bind('<Motion>',self.motion)

        self.tiles[0][0].state=1
        self.update_all()


    def click(self, event):

        try:
            self.tiles[self.sel_x][self.sel_y].frame.grid_forget()
        except:
            pass

        global_x=event.x+self.xsb.get()[0]*self.total_size_x
        global_y=event.y+self.ysb.get()[0]*self.total_size_y
        print(global_x,global_y,'glob')


        self.sel_x=int(global_x//self.tile_size)
        self.sel_y=int(global_y//self.tile_size)

        self.canvas.delete("selection_box")
        self.canvas.create_rectangle(self.sel_x*self.tile_size,self.sel_y*self.tile_size,
            self.sel_x*self.tile_size+self.tile_size,self.sel_y*self.tile_size+self.tile_size, tags="selection_box",outline="#0000FF")

        self.tiles[self.sel_x][self.sel_y].frame.grid(column=1,row=0, sticky="nsew")

    def update_all(self):

        self.tiles[0][0].top_input=1
        for a in self.tiles:
            for b in a:
                b.update()

        self.after(10,self.update_all)

# size increase prvision
        # if(global_x>900):
        #     self.canvas.configure(scrollregion=(0,0,1500,1500))
        #     self.total_size_x=self.total_size_y=1500

    def motion(self,event):
        print("Mouse position: (%s %s)" % (event.x, event.y))
        print(self.xsb.get())
        return





if __name__ == "__main__":
    root = tk.Tk()
    can=TileBoard(root)
    can.grid(column=0,row=0, sticky="nsew")

    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=1)

    root.mainloop()