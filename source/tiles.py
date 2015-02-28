import tkinter as tk

class Tile:

    def __init__(self,root,board,x,y):
        self.x=x
        self.y=y
        self.root=root
        self.board=board

        self.inputs=[0,0,0,0]

        self.frame=tk.Frame(master=root)


        self.tile_convert=tk.Button(self.frame,text="Tile",command=lambda :self.board.convert_tile(self.x,self.y,Tile))
        self.relay_convert=tk.Button(self.frame,text="Relay",command=lambda :self.board.convert_tile(self.x,self.y,Relay))
        self.source_convert=tk.Button(self.frame,text="Source",command=lambda :self.board.convert_tile(self.x,self.y,Source))
        self.flag_convert=tk.Button(self.frame,text="Flag",command=lambda :self.board.convert_tile(self.x,self.y,Flag))
        self.generator_convert=tk.Button(self.frame,text="Generator",command=lambda :self.board.convert_tile(self.x,self.y,Generator))

        self.tile_convert.pack()
        self.relay_convert.pack()
        self.source_convert.pack()
        self.flag_convert.pack()
        self.generator_convert.pack()

        self.graphics=[]

        

    def generate_shortcuts(self):

        self.adj_ind=[]

        if(self.y!=0):
            self.adj_ind.append((self.x,self.y-1))
        else:
            self.adj_ind.append(None)


        if(len(self.board.tiles)!=self.x+1):
            self.adj_ind.append((self.x+1,self.y))
        else:
            self.adj_ind.append(None)


        if(len(self.board.tiles[self.x])!=self.y+1):
            self.adj_ind.append((self.x,self.y+1))
        else:
            self.adj_ind.append(None)

        if(self.x!=0):
            self.adj_ind.append((self.x-1,self.y))
        else:
            self.adj_ind.append(None)


    def clean_delete(self):

        for graphic in self.graphics:
            self.board.canvas.delete(graphic)

        self.frame.grid_forget()        

    def update(self):

        self.output_update()
        self.graphic_update()

        self.inputs=[0,0,0,0]


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

        self.conector_checks=[self.top,self.right,self.bottom,self.left]

        self.state_index=0.5 #Float to throw error if not assigened

        self.top_cheack=tk.Checkbutton(master=self.frame,text="Top",variable=self.top)
        self.bottom_cheack=tk.Checkbutton(master=self.frame,text="Bottom",variable=self.bottom)
        self.left_cheack=tk.Checkbutton(master=self.frame,text="Left",variable=self.left)
        self.right_cheack=tk.Checkbutton(master=self.frame,text="Right",variable=self.right)

        

        self.top_cheack.pack()
        self.bottom_cheack.pack()
        self.left_cheack.pack()
        self.right_cheack.pack()

        self.label=tk.Label(master=self.frame,text=str(0))
        self.label.pack()


        self.relay_box=self.board.canvas.create_rectangle(self.x*self.board.tile_size,self.y*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#D0EAC0",outline="")

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]
        self.graphics=[self.on_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.relay_box]


    def reintegrate(self):

        for ind, check, direction in zip(self.adj_ind,self.conector_checks,[2,3,0,1]):
            try:
                if(type(self.board.tiles[ind[0]][ind[1]])==Relay):
                    if(check.get()==1 and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==1):
                        s=0
                        while(self not in self.board.relay_groups[s]):
                            s+=1

                        if(self.board.tiles[ind[0]][ind[1]] not in self.board.relay_groups[s]):
                            copy_s=self.board.relay_groups[s].copy()
                            self.board.relay_groups.pop(s)

                            k=0
                            while(self.board.tiles[ind[0]][ind[1]] not in self.board.relay_groups[k]):
                                k+=1

                            
                            copy_k=self.board.relay_groups[k].copy()
                            self.board.relay_groups.pop(k)
                            l=[]

                            for x in copy_s:
                                l.append(x)

                            for x in copy_k:
                                l.append(x)

                            assert(len(set(l))==len(l))

                            self.board.relay_groups.append(l)
            except AttributeError:
                print("AttributeError!")

    def input_update(self):

        for side in self.inputs:
            if(side==1):
                self.board.relay_states[self.state_index]=1

        

    def graphic_update(self):


        if(self.board.relay_states[self.state_index]==1):
            self.board.canvas.itemconfig(self.on_box,fill="#00FF00")
        else:
            self.board.canvas.itemconfig(self.on_box,fill="")

        for check, box in zip(self.conector_checks,self.graphic_conectors):
            if(check.get()==1):
                self.board.canvas.itemconfig(box,fill="#FF0000")
            else:
                self.board.canvas.itemconfig(box,fill="")         

        self.label.config(text=str(self)+str(self.inputs[3]))

    def output_update(self):

        for check,ind,direction in zip(self.conector_checks,self.adj_ind,[2,3,0,1]):
            try:
                if(self.board.relay_states[self.state_index]==1 and check.get()==1 
                    and type(self.board.tiles[ind[0]][ind[1]])!=Relay 
                    and ind!=None):
                    self.board.tiles[ind[0]][ind[1]].inputs[direction]=1
            except IndexError:
                print("IndexError")

class Source(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        if(self.x!=0):
            self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        else:
            self.left_box=None
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="#00FF00",outline="")

        self.graphics=[self.on_box,self.top_box,self.bottom_box,self.left_box,self.right_box]

    def output_update(self):

        for ind,direction in zip(self.adj_ind,[2,3,0,1]):
            try:
                if(ind!=None):
                    self.board.tiles[ind[0]][ind[1]].inputs[direction]=1
            except IndexError:
                print("IndexError")

class Flag(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        vcmd = (self.root.register(self.validate), '%P', '%s')


        self.name_string=tk.StringVar()
        self.publish_name=tk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd,invalidcommand=self.invcmd,textvariable=self.name_string)
        self.publish_name.pack()

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")


        self.pub_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#3b9aeF",outline="")
        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")

        self.graphics=[self.on_box,self.pub_box,self.top_box,self.bottom_box,self.left_box,self.right_box]
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


        if(any(map(lambda x:x==1,self.inputs))):

            self.board.canvas.itemconfig(self.on_box,fill="#00FF00")
            self.board.flags[self.name][1]=1


        else:
            self.board.canvas.itemconfig(self.on_box,fill="")
            self.board.flags[self.name][1]=0

class Generator(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        self.bottom=tk.IntVar()
        self.top=tk.IntVar()
        self.left=tk.IntVar()
        self.right=tk.IntVar()

        self.conector_checks=[self.top,self.right,self.bottom,self.left]

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




        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.sub_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#2e2e2e",outline="") 
        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]
        self.graphics=[self.on_box,self.sub_box,self.top_box,self.bottom_box,self.left_box,self.right_box]

        self.name=""

    def graphic_update(self):

        for check, box in zip(self.conector_checks,self.graphic_conectors):
            if(check.get()==1):
                self.board.canvas.itemconfig(box,fill="#FF0000")
            else:
                self.board.canvas.itemconfig(box,fill="")

        try:
            if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get()):
                self.board.canvas.itemconfig(self.on_box,fill="#00FF00")
            else:
                self.board.canvas.itemconfig(self.on_box,fill="")
        except KeyError:
            pass

    def output_update(self):
        try:

            for ind,check,direction in zip(self.adj_ind,self.conector_checks,[2,3,0,1]):
                try:
                    if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() 
                        and check.get()==1
                        and ind!=None):
                        self.board.tiles[ind[0]][ind[1]].inputs[direction]=1
                except IndexError:
                    pass

        except KeyError:
            print('Generator has no input')