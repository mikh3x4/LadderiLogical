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

        self.connect=[]

    def generate_shortcuts(self):
        #warning input ints are broken due to list dulpicating
        if(self.y!=0):
            self.connect.append(["top",self.board.tiles[self.x][self.y-1],self.board.tiles[self.x][self.y-1].bottom_input])
        if(len(self.board.tiles[self.x])!=self.y+1):
            self.connect.append(["bottom",self.board.tiles[self.x][self.y+1],self.board.tiles[self.x][self.y+1].top_input])
        if(self.x!=0):
            self.connect.append(["left",self.board.tiles[self.x-1][self.y],self.board.tiles[self.x-1][self.y].right_input])
        if(len(self.board.tiles)!=self.x+1):
            self.connect.append(["right",self.board.tiles[self.x+1][self.y],self.board.tiles[self.x+1][self.y].left_input])

    def clean_delete(self):

        for graphic in self.graphics:
            self.board.canvas.delete(graphic)

        self.frame.grid_forget()        

    def update(self):

        self.output_update()
        self.graphic_update()
        self.bottom_input=self.top_input=self.left_input=self.right_input=0


    def input_update(self):
        pass

    def output_update(self):
        pass

    def graphic_update(self):
        pass

class Relay(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        self.bottom=tk.IntVar()
        self.top=tk.IntVar()
        self.left=tk.IntVar()
        self.right=tk.IntVar()

        self.state_index=0


        self.top_cheack=tk.Checkbutton(master=self.frame,text="Top",variable=self.top)
        self.bottom_cheack=tk.Checkbutton(master=self.frame,text="Bottom",variable=self.bottom)
        self.left_cheack=tk.Checkbutton(master=self.frame,text="Left",variable=self.left)
        self.right_cheack=tk.Checkbutton(master=self.frame,text="Right",variable=self.right)


        self.label=tk.Label(master=self.frame,text=str(0))

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



    def reintegrate(self):


        try:
            connected=self.board.tiles[self.x][self.y-1]
            if(type(connected)==Relay):
                if(self.top.get()==1 and connected.bottom.get()==1):
                    s=0
                    while(self not in self.board.relay_groups[s]):
                        s+=1

                    if(connected not in self.board.relay_groups[s]):
                        copy_s=self.board.relay_groups[s].copy()
                        self.board.relay_groups.pop(s)

                        k=0
                        while(connected not in self.board.relay_groups[k]):
                            k+=1

                        
                        copy_k=self.board.relay_groups[k].copy()
                        self.board.relay_groups.pop(k)
                        l=[]

                        for x in copy_s:
                            l.append(x)

                        for x in copy_k:
                            l.append(x)

                        
                        try:
                            assert(len(set(l))==len(l))
                        except AssertionError:
                            print("assertion",l)
                            raise AssertionError
                        self.board.relay_groups.append(l)
        except AttributeError:
            pass

        try:    
            connected=self.board.tiles[self.x][self.y+1]
            if(type(connected)==Relay):
                if(self.bottom.get()==1 and connected.top.get()==1):
                    s=0
                    while(self not in self.board.relay_groups[s]):
                        s+=1

                    if(connected not in self.board.relay_groups[s]):
                        copy_s=self.board.relay_groups[s].copy()
                        self.board.relay_groups.pop(s)

                        k=0
                        while(connected not in self.board.relay_groups[k]):
                            k+=1

                        
                        copy_k=self.board.relay_groups[k].copy()
                        self.board.relay_groups.pop(k)
                        l=[]

                        for x in copy_s:
                            l.append(x)

                        for x in copy_k:
                            l.append(x)

                        
                        try:
                            assert(len(set(l))==len(l))
                        except AssertionError:
                            print("assertion",l)
                            raise AssertionError
                        self.board.relay_groups.append(l)
        except AttributeError:
            pass

        try:    
            connected=self.board.tiles[self.x-1][self.y]
            if(type(connected)==Relay):
                if(self.left.get()==1 and connected.right.get()==1):
                    s=0
                    while(self not in self.board.relay_groups[s]):
                        s+=1

                    if(connected not in self.board.relay_groups[s]):
                        copy_s=self.board.relay_groups[s].copy()
                        self.board.relay_groups.pop(s)

                        k=0
                        while(connected not in self.board.relay_groups[k]):
                            k+=1

                        
                        copy_k=self.board.relay_groups[k].copy()
                        self.board.relay_groups.pop(k)
                        l=[]

                        for x in copy_s:
                            l.append(x)

                        for x in copy_k:
                            l.append(x)

                        
                        try:
                            assert(len(set(l))==len(l))
                        except AssertionError:
                            print("assertion",l)
                            raise AssertionError
                        self.board.relay_groups.append(l)
        except AttributeError:
            pass

        try:    
            connected=self.board.tiles[self.x+1][self.y]
            if(type(connected)==Relay):
                if(self.right.get()==1 and connected.left.get()==1):
                    s=0
                    while(self not in self.board.relay_groups[s]):
                        s+=1

                    if(connected not in self.board.relay_groups[s]):
                        copy_s=self.board.relay_groups[s].copy()
                        self.board.relay_groups.pop(s)

                        k=0
                        while(connected not in self.board.relay_groups[k]):
                            k+=1

                        
                        copy_k=self.board.relay_groups[k].copy()
                        self.board.relay_groups.pop(k)
                        l=[]

                        for x in copy_s:
                            l.append(x)

                        for x in copy_k:
                            l.append(x)

                        
                        try:
                            assert(len(set(l))==len(l))
                        except AssertionError:
                            print("assertion",l)
                            raise AssertionError
                        self.board.relay_groups.append(l) 
        except AttributeError:
            pass

    def update(self):

        self.graphic_update()
        self.output_update()

        

    def input_update(self):

        if(self.bottom_input==1 or self.top_input==1 or self.left_input==1 or self.right_input==1):
            self.board.relay_states[self.state_index]=1

        


    def graphic_update(self):


        if(self.board.relay_states[self.state_index]==1):
            self.board.canvas.itemconfig(self.on_box,fill="#FF0000")
        else:
            print(self,'removing onness')
            self.board.canvas.itemconfig(self.on_box,fill="")


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



        self.label.config(text=str(self)+str(len(self.connect)))

    def output_update(self):

        try:
            if(self.board.relay_states[self.state_index]==1 and self.top.get()==1 and type(self.board.tiles[self.x][self.y-1])!=Relay):
                self.board.tiles[self.x][self.y-1].bottom_input=1
        except IndexError:
            pass

        try:
            if(self.board.relay_states[self.state_index]==1 and self.bottom.get()==1 and type(self.board.tiles[self.x][self.y+1])!=Relay):
                self.board.tiles[self.x][self.y+1].top_input=1
        except IndexError:
            pass

        try:
            if(self.board.relay_states[self.state_index]==1 and self.left.get()==1 and type(self.board.tiles[self.x-1][self.y])!=Relay):
                self.board.tiles[self.x-1][self.y].right_input=1
        except IndexError:
            pass

        try:
            if(self.board.relay_states[self.state_index]==1 and self.right.get()==1 and type(self.board.tiles[self.x+1][self.y])!=Relay):
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


    
    def graphic_update(self):
        
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

    def output_update(self):
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