import tkinter as tk


class Tile:

    def __init__(self,root,board,x,y):
        self.x=x
        self.y=y
        self.root=root
        self.board=board


        self.bottom_input=0
        self.top_input=0
        self.left_input=0
        self.right_input=0

        self.frame=tk.Frame(master=root)


        self.tile_convert=tk.Button(self.frame,text="Tile",command=lambda :self.board.convert_tile(self.x,self.y,Tile))
        self.relay_convert=tk.Button(self.frame,text="Relay",command=lambda :self.board.convert_tile(self.x,self.y,Relay))
        self.source_convert=tk.Button(self.frame,text="Source",command=lambda :self.board.convert_tile(self.x,self.y,Source))
        self.flag_convert=tk.Button(self.frame,text="Flag",command=lambda :self.board.convert_tile(self.x,self.y,Flag))
        self.switch_convert=tk.Button(self.frame,text="Switch",command=lambda :self.board.convert_tile(self.x,self.y,Switch))

        self.tile_convert.pack()
        self.relay_convert.pack()
        self.source_convert.pack()
        self.flag_convert.pack()
        self.switch_convert.pack()

        self.graphics=[]

    def clean_delete(self):

        for graphic in self.graphics:
            self.board.canvas.delete(graphic)

        self.frame.grid_forget()        

    def update(self):

        self.input_update()

        self.output_update()

        self.bottom_input=self.top_input=self.left_input=self.right_input=0


    def input_update(self):
        pass

    def output_update(self):
        pass


class Relay(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        self.bottom=tk.IntVar()
        self.top=tk.IntVar()
        self.left=tk.IntVar()
        self.right=tk.IntVar()

        self.state=0


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


        self.relay_box=self.board.canvas.create_rectangle(self.x*self.board.tile_size,self.y*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#D0EAC0",outline="")
        self.on_box=self.board.canvas.create_rectangle(self.x*self.board.tile_size,self.y*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")

        self.top_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y)*self.board.tile_size,fill="")
        self.bottom_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="")
        self.left_box=self.board.canvas.create_line((self.x)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="")
        self.right_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="")

        self.graphics=[self.on_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.relay_box]

    def input_update(self):

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

    def output_update(self):

        try:
            if(self.state==1 and self.top.get()==1):
                self.board.tiles[self.x][self.y-1].bottom_input=1
        except IndexError:
            pass

        try:
            if(self.state==1 and self.bottom.get()==1):
                self.board.tiles[self.x][self.y+1].top_input=1
        except IndexError:
            pass

        try:
            if(self.state==1 and self.left.get()==1):
                self.board.tiles[self.x-1][self.y].right_input=1
        except IndexError:
            pass

        try:
            if(self.state==1 and self.right.get()==1):
                self.board.tiles[self.x+1][self.y].left_input=1
        except IndexError:
            pass

class Source(Tile):

    def __init__(self, *args):

        super().__init__(*args)




        self.on_box=self.board.canvas.create_rectangle(self.x*self.board.tile_size,self.y*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")

        self.top_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#00FF00")
        self.bottom_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#00FF00")
        self.left_box=self.board.canvas.create_line((self.x)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="#00FF00")
        self.right_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="#00FF00")

        self.graphics=[self.on_box,self.top_box,self.bottom_box,self.left_box,self.right_box]

    def output_update(self):

        try:
            self.board.tiles[self.x][self.y-1].bottom_input=1
        except IndexError:
            pass

        try:
            self.board.tiles[self.x][self.y+1].top_input=1
        except IndexError:
            pass

        try:
            self.board.tiles[self.x-1][self.y].right_input=1
        except IndexError:
            pass

        try:
            self.board.tiles[self.x+1][self.y].left_input=1
        except IndexError:
            pass

class Flag(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        vcmd = (self.root.register(self.validate), '%P', '%s')


        self.name_string=tk.StringVar()
        self.publish_name=tk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd,invalidcommand=self.invcmd,textvariable=self.name_string)
        self.publish_name.pack()

        self.on_box=self.board.canvas.create_rectangle(self.x*self.board.tile_size,self.y*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")
        self.pub_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="#0000FF",outline="")

        self.graphics=[self.on_box,self.pub_box]

        self.name=""

        self.board.flags[self.name]=[self,0]

    def invcmd(self):

        print('invalide')            
        # self.name_string.set(self.name) BREAKS validation for unknow resons

    def validate(self, P, s):
        print('validation run')

        if(self.name!=P and self.board.flags[self.name][0]==self):
            del self.board.flags[self.name]
            self.name=P 

        try:
            self.board.flags[self.name]

            if(self.board.flags[self.name][0]!=self):
                # raise IndexError Causes update loops to stop
                print("WARNING MULTIPLE NAMES USED")
                self.name=s
                self.board.flags[self.name]=[self,0]

                return False

        except KeyError:
            self.board.flags[self.name]=[self,0]

        return True


    def clean_delete(self):

        del self.board.flags[self.name]
        super().clean_delete()


    def input_update(self):

        if(self.bottom_input==1 or self.top_input==1 or self.left_input==1 or self.right_input==1):

            self.board.canvas.itemconfig(self.on_box,fill="#FF0000")
            self.board.flags[self.name][1]=1


        else:
            self.board.canvas.itemconfig(self.on_box,fill="")
            self.board.flags[self.name][1]=0

class Switch(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        self.bottom=tk.IntVar()
        self.top=tk.IntVar()
        self.left=tk.IntVar()
        self.right=tk.IntVar()


        self.top_cheack=tk.Checkbutton(master=self.frame,text="Top",variable=self.top)
        self.bottom_cheack=tk.Checkbutton(master=self.frame,text="Bottom",variable=self.bottom)
        self.left_cheack=tk.Checkbutton(master=self.frame,text="Left",variable=self.left)
        self.right_cheack=tk.Checkbutton(master=self.frame,text="Right",variable=self.right)

        self.top_cheack.pack()
        self.bottom_cheack.pack()
        self.left_cheack.pack()
        self.right_cheack.pack()


        self.invert=tk.IntVar()
        self.invert_cheack=tk.Checkbutton(master=self.frame,text="Invert",variable=self.invert,onvalue='0',offvalue='1')

        self.invert.set(1)
        self.invert_cheack.pack()

        self.subscribe_name=tk.Entry(master=self.frame,width=10)
        self.subscribe_name.pack()

        self.on_box=self.board.canvas.create_rectangle(self.x*self.board.tile_size,self.y*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")
        self.sub_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#00FF00",outline="")

        self.top_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y)*self.board.tile_size,fill="")
        self.bottom_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="")
        self.left_box=self.board.canvas.create_line((self.x)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="")
        self.right_box=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="")

        self.graphics=[self.on_box,self.sub_box,self.top_box,self.bottom_box,self.left_box,self.right_box]


        self.name=""


    def output_update(self):

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

        try:

            try:
                if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() and self.top.get()==1):
                    self.board.tiles[self.x][self.y-1].bottom_input=1
            except IndexError:
                pass

            try:
                if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() and self.bottom.get()==1):
                    self.board.tiles[self.x][self.y+1].top_input=1
            except IndexError:
                pass

            try:
                if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() and self.left.get()==1):
                    self.board.tiles[self.x-1][self.y].right_input=1
            except IndexError:
                pass

            try:
                if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() and self.right.get()==1):
                    self.board.tiles[self.x+1][self.y].left_input=1
            except IndexError:
                pass

        except KeyError:
            print('Switch has no input')

class TileBoard(tk.Frame):
    def __init__(self, root,app):
        tk.Frame.__init__(self, root)
        self.root=root
        self.app=app

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


        self.tiles=[[Source(root,self,r,i) if r==0 else Relay(root,self,r,i) for i in range(self.total_size_y//self.tile_size)] for r in range(self.total_size_x//self.tile_size)]

        self.flags={}


        self.canvas.bind("<ButtonPress-1>", self.click)
        self.canvas.bind("<Shift-ButtonPress-1>", self.shift_click)

        self.canvas.bind("<Control-ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<Control-B1-Motion>", self.scroll_move)
        # self.canvas.bind('<Motion>',self.motion)

        self.tiles[0][0].state=1
        self.update_all()


    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)


    def convert_tile(self,x,y,typ):

        self.tiles[x][y].clean_delete()
        self.tiles[x][y]=typ(self.root,self,x,y)

        if(x==self.sel_x and y==self.sel_y):
            self.tiles[x][y].frame.grid(column=1,row=1, sticky="nsew")


    def click(self,event):
        self.shift_click(event)

        self.app.tools.tool="select"

    def shift_click(self,event):

        if(self.app.tools.tool=='select'):
            self.select(event)

        elif(self.app.tools.tool=='horizontal'):
            self.horizontal(event)
        else:
            print('Unrecognised tool')

    def horizontal(self,event):

        coords=self.find_tile_coords(event)

        x=coords[0]
        y=coords[1]

        self.convert_tile(x,y,Relay)

        self.tiles[x][y].left.set(1)
        self.tiles[x][y].right.set(1)

    def select(self, event):

        try:
            self.tiles[self.sel_x][self.sel_y].frame.grid_forget()
        except AttributeError:
            print('Caugth error - no tile selected yet!')
        except IndexError:
            print("Unwelcome ERROR! Something wrong with selection")

        coords=self.find_tile_coords(event)

        self.sel_x=coords[0]
        self.sel_y=coords[1]

        self.canvas.delete("selection_box")
        self.canvas.create_rectangle(self.sel_x*self.tile_size,self.sel_y*self.tile_size,
            self.sel_x*self.tile_size+self.tile_size,self.sel_y*self.tile_size+self.tile_size, tags="selection_box",outline="#0000FF")

        self.tiles[self.sel_x][self.sel_y].frame.grid(column=1,row=1, sticky="nsew")

    def find_tile_coords(self,event):
        global_x=event.x+self.xsb.get()[0]*self.total_size_x
        global_y=event.y+self.ysb.get()[0]*self.total_size_y
        print(global_x,global_y,'glob')


        x=int(global_x//self.tile_size)
        y=int(global_y//self.tile_size)

        return (x,y)

    def update_all(self):

        for a in self.tiles:
            for b in a:
                b.update()

        try:
            self.app.io.update()
        except AttributeError:
            print('initialy no board existant')

        print(self.flags)
        self.after(25,self.update_all)

        
        # size increase prvision
        # if(global_x>900):
        #     self.canvas.configure(scrollregion=(0,0,1500,1500))
        #     self.total_size_x=self.total_size_y=1500



class IOBoard(tk.Frame):


    def __init__(self,root,app):
        tk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.output_list=[]

        for x in range(8):
            a=tk.Entry(master=self,width=10)
            a.grid(column=0,row=x)
            b=tk.Label(master=self,text='0')
            b.grid(column=1,row=x)
            self.output_list.append([a,b])


    def update(self):

        for x in self.output_list:
            try:
                x[1].config(text=str(self.app.board.flags[x[0].get()][1]))
            except KeyError:
                # print(x[0].get()+" flag non existant")
                pass

class ToolBox(tk.Frame):


    def __init__(self,root,app):
        tk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.tool="select"

        self.select=tk.Button(master=self,text="Select",command=lambda:self.change_tool("select"))
        self.horizontal=tk.Button(master=self,text="Horizontal",command=lambda:self.change_tool("horizontal"))

        self.select.grid(row=0,column=0)
        self.horizontal.grid(row=0,column=1)


    def change_tool(self,name):
        print("changed to "+name)
        self.tool=name




class LadderLogic:

    def __init__(self):

        self.root=tk.Tk()
        self.root.title('LadderLogic')

        self.io=IOBoard(self.root,self)
        self.io.grid(column=2,row=1, sticky="nsew")

        self.board=TileBoard(self.root,self)
        self.board.grid(column=0,row=1, sticky="nsew")

        self.tools=ToolBox(self.root,self)
        self.tools.grid(column=0,row=0, sticky="nsew")

        self.root.grid_rowconfigure(1,weight=0)
        self.root.grid_rowconfigure(1,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=0)
        self.root.grid_columnconfigure(2,weight=0)


if __name__ == "__main__":

    l=LadderLogic()


    l.root.mainloop()