import tkinter.ttk as ttk
import tkinter as tk

from time import time
from extra_ui import DirectionSelector,BiDirectionSelector

class Tile:

    forbiden_chars=["'",'"',"[","]","{","}",","]

    def __init__(self,root,board,x,y):
        self.x=x
        self.y=y
        self.root=root
        self.board=board

        self.inputs=[0,0,0,0]

        self.frame=ttk.Frame(master=root)

        self.bottom=tk.IntVar()
        self.top=tk.IntVar()
        self.left=tk.IntVar()
        self.right=tk.IntVar()

        self.conector_checks=[self.top,self.right,self.bottom,self.left]

        ttk.Label(master=self.frame,text="Convert to:").pack()

        self.tile_convert=ttk.Button(self.frame,text="Tile",command=lambda :self.board.convert_tile(self.x,self.y,Tile))
        self.relay_convert=ttk.Button(self.frame,text="Relay",command=lambda :self.board.convert_tile(self.x,self.y,Relay))
        self.source_convert=ttk.Button(self.frame,text="Source",command=lambda :self.board.convert_tile(self.x,self.y,Source))
        self.flag_convert=ttk.Button(self.frame,text="Flag",command=lambda :self.board.convert_tile(self.x,self.y,Flag))
        self.generator_convert=ttk.Button(self.frame,text="Generator",command=lambda :self.board.convert_tile(self.x,self.y,Generator))
        self.switch_convert=ttk.Button(self.frame,text="Switch",command=lambda :self.board.convert_tile(self.x,self.y,Switch))
        self.counter_convert=ttk.Button(self.frame,text="Counter",command=lambda :self.board.convert_tile(self.x,self.y,Counter))
        self.pulsar_convert=ttk.Button(self.frame,text="Pulsar",command=lambda :self.board.convert_tile(self.x,self.y,Pulsar))
        self.timer_convert=ttk.Button(self.frame,text="Timer",command=lambda :self.board.convert_tile(self.x,self.y,Timer))
        self.sequencer_convert=ttk.Button(self.frame,text="Sequencer",command=lambda :self.board.convert_tile(self.x,self.y,Sequencer))

        self.tile_convert.pack()
        self.relay_convert.pack()
        self.source_convert.pack()
        self.flag_convert.pack()
        self.generator_convert.pack()
        self.switch_convert.pack()
        self.counter_convert.pack()
        self.pulsar_convert.pack()
        self.timer_convert.pack()
        self.sequencer_convert.pack()

        self.graphics=[]

        
    def save_to_file(self):

        return "blk"

    def open_from_file(self,data):
        print("ERROR, blk not ment to be opened")

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


    def input_update(self):
        pass

    def output_update(self):
        pass

    def graphic_update(self):
        pass

class Relay(Tile):

    def __init__(self, *args):

        super().__init__(*args)



        self.state_index=0.5 #Float to throw error if not assigened


        self.dir_selector=DirectionSelector(self.frame,self.conector_checks)
        self.dir_selector.pack()

        for check in self.conector_checks:
            check.trace("w",self.dir_selector.variable_changed)


        self.relay_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]
        self.graphics=[self.on_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.relay_box]


    def save_to_file(self):
        out={"0type":"relay"}
        out['checks']=[x.get() for x in self.conector_checks]
        return out

    def open_from_file(self,data):
        assert(data['0type']=="relay")

        for check,inp in zip(self.conector_checks,data['checks']):
            print(inp)
            check.set(inp)

        if(len(data)!=2): #0type checks
            print("File contains unimplemented feature in a Relay Tile")

    def reintegrate(self):

        for ind, check, direction in zip(self.adj_ind,self.conector_checks,[2,3,0,1]):

            if (ind==None):
                pass
            elif (type(self.board.tiles[ind[0]][ind[1]])==Relay):
                if (check.get()==1 
                    and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==1):
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


    def input_update(self):

        for side,check in zip(self.inputs,self.conector_checks):
            if(side==1 and check.get()==1):
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

    def output_update(self):

        for check,ind,direction in zip(self.conector_checks,self.adj_ind,[2,3,0,1]):

            if(self.board.relay_states[self.state_index]==1 and check.get()==1
                and ind!=None
                and type(self.board.tiles[ind[0]][ind[1]])!=Relay):
                self.board.tiles[ind[0]][ind[1]].inputs[direction]=1

class Source(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        for x in self.conector_checks:
            x.set(1)

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        if(self.x!=0):
            self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        else:
            self.left_box=None

        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="#00FF00",outline="#FFFFFF")

        self.graphics=[self.on_box,self.top_box,self.bottom_box,self.left_box,self.right_box]

    def save_to_file(self):
        out={"0type":"source"}
        out['checks']=[x.get() for x in self.conector_checks]
        return out

    def open_from_file(self,data):
        assert(data['0type']=="source")

        for check,inp in zip(self.conector_checks,data['checks']):
            check.set(inp)

        if(len(data)!=2): #0type checks
            print("File contains unimplemented feature in a Source Tile")


    def output_update(self):

        for ind,direction in zip(self.adj_ind,[2,3,0,1]):

            if(ind!=None):
                self.board.tiles[ind[0]][ind[1]].inputs[direction]=1

class Flag(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        vcmd = (self.root.register(self.validate), '%P', '%s','%S','%d')

        for x in self.conector_checks:
            x.set(2)


        self.publish_name=ttk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd,invalidcommand=self.invcmd)
        self.publish_name.pack()

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#0000FF",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#0000FF",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#0000FF",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF",outline="")


        self.pub_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#3b9aeF",outline="#EEEEEE")
        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")

        self.graphics=[self.on_box,self.pub_box,self.top_box,self.bottom_box,self.left_box,self.right_box]

        self.name=""
        i=1
        try:
            while 1:
                self.board.flags[self.name+str(i)]
                i+=1
        except KeyError:

            self.name=self.name+str(i)
            self.board.flags[self.name]=[self,0]

        self.publish_name.delete(0,tk.END)
        self.publish_name.insert(0,self.name)


    def save_to_file(self):
        out={"0type":"flag"}
        out['checks']=[x.get() for x in self.conector_checks]
        out['pubname']=self.name

        return out

    def open_from_file(self,data):
        assert(data['0type']=="flag")

        for check,inp in zip(self.conector_checks,data['checks']):
            check.set(inp)

        self.name=data['pubname']
        self.publish_name.config(validate="none")
        self.publish_name.delete(0,tk.END)
        self.publish_name.insert(0,self.name)
        self.publish_name.config(validate="key")

        self.board.flags[self.name]=[self,0]

        if(len(data)!=3): #0type checks pubname
            print("File contains unimplemented feature in a Flag Tile")


    def invcmd(self):

        self.publish_name.delete(0,tk.END)
        self.publish_name.insert(0,self.name)
        self.publish_name.config(validate="key")

    def validate(self, P, s,S,d):

        if(d=="1" and S in self.forbiden_chars):
            return False

        del self.board.flags[self.name]
        self.name=P 
        try:
            self.board.flags[self.name]
        except KeyError:
            self.board.flags[self.name]=[self,0]
            return True

        i=1
        try:
            while 1:
                self.board.flags[self.name+"."+str(i)]
                i+=1
        except KeyError:

            self.name=self.name+"."+str(i)
            self.board.flags[self.name]=[self,0]

        return False




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


        self.dir_selector=DirectionSelector(self.frame,self.conector_checks)
        self.dir_selector.pack()

        for check in self.conector_checks:
            check.trace("w",self.dir_selector.variable_changed)

        self.invert=tk.IntVar()
        self.invert_cheack=ttk.Checkbutton(master=self.frame,text="Invert",variable=self.invert,onvalue='0',offvalue='1')

        self.invert.set(1)
        self.invert_cheack.pack()

        vcmd = (self.root.register(self.validate), '%S','%d')

        self.subscribe_name=ttk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd)
        self.subscribe_name.pack()



        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="",outline="")

        self.gen_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#2e2e2e",outline="#EEEEEE") 
        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")
        self.missing_key=self.board.canvas.create_text((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,text="?",fill="")

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]
        self.graphics=[self.on_box,self.gen_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.missing_key]


    def validate(self,S,d):
        if(d=="1" and S in self.forbiden_chars):
            return False
        return True


    def save_to_file(self):
        out={"0type":"generator"}
        out['checks']=[x.get() for x in self.conector_checks]
        out['subname']=self.subscribe_name.get()
        out['invert']=self.invert.get()

        print('created generator')
        return out

    def open_from_file(self,data):
        assert(data['0type']=="generator")

        for check,inp in zip(self.conector_checks,data['checks']):
            check.set(inp)

        self.invert.set(data['invert'])
        # self.subscribe_name.config(validate="none")
        self.subscribe_name.delete(0,tk.END)
        self.subscribe_name.insert(0,data['subname'])
        # self.subscribe_name.config(validate="key")

        if(len(data)!=4): #0type checks subname invert
            print("File contains unimplemented feature in a Generator Tile")

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

                if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() 
                    and check.get()==1
                    and ind!=None):
                    self.board.tiles[ind[0]][ind[1]].inputs[direction]=1
            self.board.canvas.itemconfig(self.missing_key,fill="")

        except KeyError:
            self.board.canvas.itemconfig(self.missing_key,fill="#FF0000")

class Switch(Tile):

    def __init__(self, *args):

        super().__init__(*args)


        self.dir_selector=BiDirectionSelector(self.frame,self.conector_checks)
        self.dir_selector.pack()

        for check in self.conector_checks:
            check.trace("w",self.dir_selector.variable_changed)


        self.invert=tk.IntVar()
        self.invert_cheack=ttk.Checkbutton(master=self.frame,text="Invert",variable=self.invert,onvalue='0',offvalue='1')

        self.invert.set(1)
        self.invert_cheack.pack()



        vcmd = (self.root.register(self.validate), '%S','%d')

        self.subscribe_name=ttk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd)

        self.subscribe_name.pack()


        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="",outline="")

        self.switch_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#AF20CF",outline="#EEEEEE") 

        self.on_box_top=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.2)*self.board.tile_size+1,fill="",outline="")
        self.on_box_bottom=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")
        self.on_box_rigth=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="",outline="")
        self.on_box_left=self.board.canvas.create_rectangle((self.x+0.6)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.2)*self.board.tile_size+1,(self.y+0.6)*self.board.tile_size,fill="",outline="")

        self.missing_key=self.board.canvas.create_text((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,text="?",fill="")

        self.on_conectors=[self.on_box_top,self.on_box_bottom,self.on_box_rigth,self.on_box_left]
        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]


        self.graphics=[self.missing_key,self.switch_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.on_box_top,self.on_box_bottom,self.on_box_rigth,self.on_box_left]


        self.states=0

    def validate(self,S,d):
        if(d=="1" and S in self.forbiden_chars):
            return False
        return True

    def save_to_file(self):
        out={"0type":"switch"}
        out['checks']=[x.get() for x in self.conector_checks]
        out['subname']=self.subscribe_name.get()
        out['invert']=self.invert.get()

        return out

    def open_from_file(self,data):
        assert(data['0type']=="switch")

        for check,inp in zip(self.conector_checks,data['checks']):
            check.set(inp)

        self.invert.set(data['invert'])

        # self.subscribe_name.config(validate="none")
        self.subscribe_name.delete(0,tk.END)
        self.subscribe_name.insert(0,data['subname'])
        # self.subscribe_name.config(validate="key")

        if(len(data)!=4): #0type checks subname invert
            print("File contains unimplemented feature in a Switch Tile")

    def graphic_update(self):

        for check, box in zip(self.conector_checks,self.graphic_conectors):
            if(check.get()==1):
                self.board.canvas.itemconfig(box,fill="#FF0000")

            elif(check.get()==2):
                self.board.canvas.itemconfig(box,fill="#0000FF")
            else:
                self.board.canvas.itemconfig(box,fill="")

        try:
            if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get()):
                for box,check in zip(self.on_conectors,self.conector_checks):
                    if(check.get()!=0):
                        self.board.canvas.itemconfig(box,fill="#FF0000")
            else:
                for box in self.on_conectors:
                    self.board.canvas.itemconfig(box,fill="")
            self.board.canvas.itemconfig(self.missing_key,fill="")
        except KeyError:
            self.board.canvas.itemconfig(self.missing_key,fill="#FFFF00")

    def input_update(self):
        for i in [0,1,2,3]:
            if(self.conector_checks[i].get()==2 and self.inputs[i]==1):
                self.state=1
            else:
                self.state=0


    def output_update(self):
        try:

            if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() and self.state==1):
                for ind,check,direction in zip(self.adj_ind,self.conector_checks,[2,3,0,1]):

                    if(ind!=None and check.get()==1):
                        self.board.tiles[ind[0]][ind[1]].inputs[direction]=1

        except KeyError:
            pass

class Counter(Tile):

    def __init__(self, *args):

        super().__init__(*args)


        self.conector_checks[0].set(0)
        self.conector_checks[1].set(1)
        self.conector_checks[2].set(1)
        self.conector_checks[3].set(2)

        vcmd = (self.root.register(self.validate), '%P', '%s','%S', '%d')

        self.count_upto=ttk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd)
        self.count_upto.pack()
        self.count_upto.insert(0,"1")

        self.upto=1
        self.counter=0
        self.edge=0

        self.auto_reset=tk.IntVar()
        self.auto_reset_cheack=ttk.Checkbutton(master=self.frame,text="Auto Reset",variable=self.auto_reset,onvalue='1',offvalue='0')

        self.auto_reset.set(1)
        self.auto_reset_cheack.pack()

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.counter_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#DDDDDD",outline="#EEEEEE") 

        self.text_box=self.board.canvas.create_text((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,text="00+")



        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]

        self.graphics=[self.counter_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.text_box]


    def save_to_file(self):
        out={"0type":"counter"}
        out['up_to']=self.upto
        out['reset']=self.auto_reset.get()


        return out

    def open_from_file(self,data):
        assert(data['0type']=="counter")
        self.upto=data['up_to']
        self.auto_reset.set(data['reset'])

        self.count_upto.config(validate="none")
        self.count_upto.delete(0,tk.END)
        self.count_upto.insert(0,data['up_to'])
        self.count_upto.config(validate="key")

        if(len(data)!=3): #0type up_to reset
            print("File contains unimplemented feature in a Counter Tile")




    def validate(self,P,s,S,d):

        if(d=="1" and S in self.forbiden_chars):
            return False

        if(P==""):
            self.upto=1
            return True

        try:
            self.upto=int(P)
        except ValueError:
            return False
        print('value updated')
        return True

    def graphic_update(self):

        for check, box in zip(self.conector_checks,self.graphic_conectors):
            if(check.get()==1):
                self.board.canvas.itemconfig(box,fill="#FF0000")

            elif(check.get()==2):
                self.board.canvas.itemconfig(box,fill="#0000FF")
            else:
                self.board.canvas.itemconfig(box,fill="")


        self.board.canvas.itemconfig(self.text_box,text=str(self.counter)+"+")

        if(self.counter>=self.upto):
            self.board.canvas.itemconfig(self.text_box,fill="#00FF00")
        else:
            self.board.canvas.itemconfig(self.text_box,fill="#000000")


    def input_update(self):

        if(self.auto_reset.get()==1):
            self.conector_checks[2].set(0)
        else:
            self.conector_checks[2].set(2)

        if(self.inputs[3]==0):
            self.edge=1
        elif(self.inputs[3]==1):
            
            if(self.edge==1 and self.counter<self.upto):
                self.counter+=1
            self.edge=0

        if(self.inputs[2]==1):
            self.counter=0


    def output_update(self):


        if(self.counter>=self.upto):

            if(self.auto_reset.get()==1):
                self.counter=0

            if(self.adj_ind[1]!=None and self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].conector_checks[3]):
                self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].inputs[3]=1

class Pulsar(Tile):

    def __init__(self, *args):

        super().__init__(*args)


        self.conector_checks[0].set(0)
        self.conector_checks[1].set(1)
        self.conector_checks[2].set(0)
        self.conector_checks[3].set(2)

        vcmd = (self.root.register(self.validate), '%P', '%s','%S', '%d')

        self.time_in=ttk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd)
        self.time_in.pack()
        self.time_in.insert(0,"1000")

        self.time=time()



        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.pulsar_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#DDDDDD",outline="#EEEEEE") 

        self.pulsar_lines=[]
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.7)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.4)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.4)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.6)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))

        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.4)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#0000FF"))
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.4)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#0000FF"))
        self.pulsar_lines.append(self.board.canvas.create_line((self.x+0.6)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))

        self.time_to=1000
        self.state=0
        self.prev=0

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]

        self.graphics=[self.pulsar_box,self.top_box,self.bottom_box,self.left_box,self.right_box]
        self.graphics.extend(self.pulsar_lines)

    def save_to_file(self):
        out={"0type":"pulsar"}
        out['time_to']=self.time_to

        return out

    def open_from_file(self,data):
        assert(data['0type']=="pulsar")
        self.time_to=data['time_to']
        self.time_in.config(validate="none")
        self.time_in.delete(0,tk.END)
        self.time_in.insert(0,str(self.time_to))
        self.time_in.config(validate="key")

        if(len(data)!=2): #0type time_to
            print("File contains unimplemented feature in a Pulsar Tile")

    def validate(self,P,s,S,d):


        if(d=="1" and S in self.forbiden_chars):
            return False        

        if(P==""):
            self.time_to=100
            return True

        try:
            self.time_to=int(P)
        except ValueError:
            return False
        print('value updated')
        return True

    def graphic_update(self):

        for check, box in zip(self.conector_checks,self.graphic_conectors):
            if(check.get()==1):
                self.board.canvas.itemconfig(box,fill="#FF0000")

            elif(check.get()==2):
                self.board.canvas.itemconfig(box,fill="#0000FF")
            else:
                self.board.canvas.itemconfig(box,fill="")

    def input_update(self):
        if(self.inputs[3]==1):
            self.state=1
        else:
            self.state=0
            
    def output_update(self):

        if(1000*(time()-self.time)>int(self.time_to)):

            if(self.prev==0):
                self.prev=1
            else:
                self.prev=0

            self.time=time()

        if(self.adj_ind[1]!=None 
            and self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].conector_checks[3]
            and self.prev==1
            and self.state==1):
            self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].inputs[3]=1

class Timer(Tile):

    def __init__(self, *args):

        super().__init__(*args)


        self.conector_checks[0].set(0)
        self.conector_checks[1].set(1)
        self.conector_checks[2].set(0)
        self.conector_checks[3].set(2)

        vcmd = (self.root.register(self.validate), '%P', '%s','%S', '%d')


        self.timer_mode = tk.IntVar()
        self.timer_mode.set(1)

        ttk.Radiobutton(master=self.frame, text="Hold", variable=self.timer_mode, value=1).pack()
        ttk.Radiobutton(master=self.frame, text="Delay Monostable", variable=self.timer_mode, value=2).pack()
        ttk.Radiobutton(master=self.frame, text="Manaul", variable=self.timer_mode, value=3).pack()



        self.time_dalay=ttk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd)
        self.time_dalay.pack()
        self.time_dalay.insert(0,"1000")

        self.time=time()

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.timer_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#888888",outline="#EEEEEE") 
        self.timer_shield=self.board.canvas.create_oval((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#DDDDDD",outline="#EEEEEE") 
        self.timer_tick=self.board.canvas.create_line((self.x+0.5)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="#111111") 
        self.timer_tock=self.board.canvas.create_line((self.x+0.6)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="#111111") 


        self.input_update=self.input_update_1

        self.time_to=1000
        self.state=0
        self.prev=0
        self.edge=0
        self.latch=0

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]

        self.graphics=[self.timer_box,self.timer_shield,self.timer_tick,self.timer_tock,
                        self.top_box,self.bottom_box,self.left_box,self.right_box]


    def save_to_file(self):
        out={"0type":"timer"}
        out['time_to']=self.time_to
        out['mode']=self.timer_mode.get()

        return out

    def open_from_file(self,data):
        assert(data['0type']=="timer")
        self.time_to=data['time_to']
        self.time_dalay.config(validate="none")
        self.time_dalay.delete(0,tk.END)
        self.time_dalay.insert(0,str(self.time_to))
        self.time_dalay.config(validate="key")
        self.timer_mode.set(data['mode'])

        if(len(data)!=3): #0type time_to mode
            print("File contains unimplemented feature in a Timer Tile")

    def validate(self,P,s,S,d):

        self.prev=0
        if(d=="1" and S in self.forbiden_chars):
            return False        

        if(P==""):
            self.time_to=1000
            return True

        try:
            self.time_to=int(P)
        except ValueError:
            return False
        print('value updated')
        return True

    def graphic_update(self):


        for check, box in zip(self.conector_checks,self.graphic_conectors):
            if(check.get()==1):
                self.board.canvas.itemconfig(box,fill="#FF0000")

            elif(check.get()==2):
                self.board.canvas.itemconfig(box,fill="#0000FF")
            else:
                self.board.canvas.itemconfig(box,fill="")

    def update(self):

        if(self.timer_mode.get()==1):
            self.conector_checks[2].set(0)
            self.output_update_1()
            self.input_update=self.input_update_1

        elif(self.timer_mode.get()==2):
            self.conector_checks[2].set(0)
            self.output_update_2()
            self.input_update=self.input_update_2

        elif(self.timer_mode.get()==3):
            self.conector_checks[2].set(2)
            self.output_update_3()
            self.input_update=self.input_update_3

        self.graphic_update()



    def input_update_1(self):

        if(self.inputs[3]==1 and self.state==0):
            self.state==1
            self.prev=time()
        else:
            self.state=0
            
    def output_update_1(self):

        if(1000*(time()-self.prev)<int(self.time_to)):

            if(self.adj_ind[1]!=None and self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].conector_checks[3]):
                self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].inputs[3]=1


    def input_update_2(self):

        #Add Ignore or replace extra input "and self.edge==0 on next line"

        if(self.inputs[3]==1 and self.state==0):
            self.edge=1
            self.prev=time()

        if(self.inputs[3]==1):
             self.state=1
        else:
            self.state=0

            
    def output_update_2(self):
        if(self.edge==1 and 1000*(time()-self.prev)>int(self.time_to)):

            if(self.adj_ind[1]!=None and self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].conector_checks[3]):
                self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].inputs[3]=1

            self.edge=0

    def input_update_3(self):

        if(self.inputs[3]==1 and self.state==0):
            self.edge=1
            self.prev=time()

        if(self.inputs[2]==1):
            self.latch=0

        if(self.inputs[3]==1):
             self.state=1
        else:
            self.state=0

            
    def output_update_3(self):

        if(self.latch==1):
            if(self.adj_ind[1]!=None and self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].conector_checks[3]):
                self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].inputs[3]=1
        
        if(self.edge==1 and 1000*(time()-self.prev)>int(self.time_to)):

            if(self.adj_ind[1]!=None and self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].conector_checks[3]):
                self.board.tiles[self.adj_ind[1][0]][self.adj_ind[1][1]].inputs[3]=1

            self.edge=0
            self.latch=1

class Sequencer(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        vcmd = (self.root.register(self.validate), '%P', '%s','%S','%d')

        for x in self.conector_checks:
            x.set(2)

        self.add_field_button=ttk.Button(master=self.frame,text="Add",command=self.add_field)
        self.del_field_button=ttk.Button(master=self.frame,text="Remove",command=self.del_field)

        self.add_field_button.pack()
        self.del_field_button.pack()

        self.sequence_steps=[]


        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#0000FF",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#0000FF",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#0000FF",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF",outline="")


        self.seq_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#DDDDDD",outline="#EEEEEE")

        stairs=[]
        stairs.append(self.board.canvas.create_line((self.x+0.2)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.4)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#0000FF"))
        stairs.append(self.board.canvas.create_line((self.x+0.4)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.4)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="#0000FF"))
        stairs.append(self.board.canvas.create_line((self.x+0.4)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,fill="#0000FF"))
        stairs.append(self.board.canvas.create_line((self.x+0.6)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#0000FF"))
        stairs.append(self.board.canvas.create_line((self.x+0.6)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#0000FF"))

        self.graphics=[self.seq_box,self.top_box,self.bottom_box,self.left_box,self.right_box]

        self.graphics.extend(stairs)

        self.edge=0
        self.index=0

    def add_field(self,name_arg="seq"):

        x=len(self.sequence_steps)

        vcmd = (self.root.register(self.validate), '%P','%S','%d',x)

        def temp(r):
            def invcmd():
                self.sequence_steps[r][0].delete(0,tk.END)
                self.sequence_steps[r][0].insert(0,self.sequence_steps[r][1])
                self.sequence_steps[r][0].config(validate="key")
            return invcmd

        entry=ttk.Entry(master=self.frame,width=10,validate="none",validatecommand=vcmd,invalidcommand=temp(x))
        entry.pack()

        name=name_arg


        i=1
        try:
            self.board.flags[name]
            while 1:
                self.board.flags[name]
                i+=1
                name=name_arg+str(i)
        except KeyError:
            self.board.flags[name]=[self,0]

        entry.delete(0,tk.END)
        entry.insert(0,name)

        self.sequence_steps.append([entry,name])
        entry.config(validate="key")

    def del_field(self):
        x=len(self.sequence_steps)-1
        if(x<0):
            print('Nothing to remove')
            return 0
        self.sequence_steps[x][0].pack_forget()
        del self.board.flags[self.sequence_steps[x][1]]
        self.sequence_steps.pop(x)


    def validate(self, P,S,d,n):

        if(d=="1" and S in self.forbiden_chars):
            return False

        n=int(n)
        del self.board.flags[self.sequence_steps[n][1]]
        self.sequence_steps[n][1]=P
        try:
            self.board.flags[self.sequence_steps[n][1]]
        except KeyError:
            self.board.flags[self.sequence_steps[n][1]]=[None,0]
            return True

        i=1
        try:
            while 1:
                self.board.flags[self.sequence_steps[n][1]+"."+str(i)]
                i+=1
        except KeyError:
            self.sequence_steps[n][1]=self.sequence_steps[n][1]+"."+str(i)
            self.board.flags[self.sequence_steps[n][1]]=[None,0]


        return False


    def save_to_file(self):
        out={"0type":"sequ"}
        out['checks']=[x.get() for x in self.conector_checks]
        out['steps']=[step[1] for step in self.sequence_steps]

        return out

    def open_from_file(self,data):
        assert(data['0type']=="sequ")

        for check,inp in zip(self.conector_checks,data['checks']):
            check.set(inp)

        for step in data['steps']:
            self.add_field(name_arg=step)

        if(len(data)!=3): #0type checks steps
            print("File contains unimplemented feature in a Sequencer Tile")


    def clean_delete(self):
        r=1
        while r!=0:
            r=self.del_field()
        super().clean_delete()

    def input_update(self):

        on=any(map(lambda x:x==1,self.inputs))

        if(on and self.edge==0):
            self.prev=time()
            self.index=(self.index+1)%len(self.sequence_steps)

        if(on):
            self.edge=1
        else:
            self.edge=0

        for x in range(len(self.sequence_steps)):
            if(x==self.index):
                self.board.flags[self.sequence_steps[x][1]][1]=1
            else:
                self.board.flags[self.sequence_steps[x][1]][1]=0






