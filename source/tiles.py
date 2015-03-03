import tkinter as tk
from time import time

class Tile:

    def __init__(self,root,board,x,y):
        self.x=x
        self.y=y
        self.root=root
        self.board=board

        self.inputs=[0,0,0,0]

        self.frame=tk.Frame(master=root)

        self.bottom=tk.IntVar()
        self.top=tk.IntVar()
        self.left=tk.IntVar()
        self.right=tk.IntVar()

        self.conector_checks=[self.top,self.right,self.bottom,self.left]

        tk.Label(master=self.frame,text="Convert to:").pack()

        self.tile_convert=tk.Button(self.frame,text="Tile",command=lambda :self.board.convert_tile(self.x,self.y,Tile))
        self.relay_convert=tk.Button(self.frame,text="Relay",command=lambda :self.board.convert_tile(self.x,self.y,Relay))
        self.source_convert=tk.Button(self.frame,text="Source",command=lambda :self.board.convert_tile(self.x,self.y,Source))
        self.flag_convert=tk.Button(self.frame,text="Flag",command=lambda :self.board.convert_tile(self.x,self.y,Flag))
        self.generator_convert=tk.Button(self.frame,text="Generator",command=lambda :self.board.convert_tile(self.x,self.y,Generator))
        self.switch_convert=tk.Button(self.frame,text="Switch",command=lambda :self.board.convert_tile(self.x,self.y,Switch))
        self.counter_convert=tk.Button(self.frame,text="Counter",command=lambda :self.board.convert_tile(self.x,self.y,Counter))
        self.pulsar_convert=tk.Button(self.frame,text="Pulsar",command=lambda :self.board.convert_tile(self.x,self.y,Pulsar))


        self.tile_convert.pack()
        self.relay_convert.pack()
        self.source_convert.pack()
        self.flag_convert.pack()
        self.generator_convert.pack()
        self.switch_convert.pack()
        self.counter_convert.pack()
        self.pulsar_convert.pack()

        self.graphics=[]

        
    def save_to_file(self):

    	return "blk"

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


        self.relay_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")

        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]
        self.graphics=[self.on_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.relay_box]


    def save_to_file(self):
    	out=["relay,check:"]
    	out.append("[")
    	for check in self.conector_checks:
    		out.append(str(check.get()))
    		out.append('.')
    	out.pop(len(out)-1)
    	out.append(']')
    	return ''.join(out)


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

        self.label.config(text=str(self)+str(self.inputs[3]))

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
    	out=["source,check:"]
    	out.append("[")
    	for check in self.conector_checks:
    		out.append(str(check.get()))
    		out.append('.')
    	out.pop(len(out)-1)
    	out.append(']')
    	return ''.join(out)

    def output_update(self):

        for ind,direction in zip(self.adj_ind,[2,3,0,1]):

            if(ind!=None):
                self.board.tiles[ind[0]][ind[1]].inputs[direction]=1

class Flag(Tile):

    def __init__(self, *args):

        super().__init__(*args)

        vcmd = (self.root.register(self.validate), '%P', '%s')

        for x in self.conector_checks:
            x.set(1)


        self.publish_name=tk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd,invalidcommand=self.invcmd)
        self.publish_name.pack()

        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="#FF0000",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="#FF0000",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="#FF0000",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="#FF0000",outline="")


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
    	out=["flag,check:"]
    	out.append("[")
    	for check in self.conector_checks:
    		out.append(str(check.get()))
    		out.append('.')
    	out.pop(len(out)-1)
    	out.append('],pubname:'+self.name)

    	return ''.join(out)

    def invcmd(self):

        self.publish_name.delete(0,tk.END)
        self.publish_name.insert(0,self.name)
        self.publish_name.config(validate="key")

    def validate(self, P, s):
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



        self.top_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y)*self.board.tile_size,fill="",outline="")
        self.bottom_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+0.7)*self.board.tile_size,(self.y+1)*self.board.tile_size,fill="",outline="")
        self.left_box=self.board.canvas.create_rectangle((self.x+0.7)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,(self.x)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,fill="",outline="")
        self.right_box=self.board.canvas.create_rectangle((self.x+0.3)*self.board.tile_size,(self.y+0.3)*self.board.tile_size,(self.x+1)*self.board.tile_size,(self.y+0.7)*self.board.tile_size,fill="",outline="")

        self.gen_box=self.board.canvas.create_rectangle((self.x+0.2)*self.board.tile_size,(self.y+0.2)*self.board.tile_size,(self.x+0.8)*self.board.tile_size,(self.y+0.8)*self.board.tile_size,fill="#2e2e2e",outline="#EEEEEE") 
        self.on_box=self.board.canvas.create_rectangle((self.x+0.4)*self.board.tile_size,(self.y+0.4)*self.board.tile_size,(self.x+0.6)*self.board.tile_size,(self.y+0.6)*self.board.tile_size,fill="",outline="")
        self.missing_key=self.board.canvas.create_text((self.x+0.5)*self.board.tile_size,(self.y+0.5)*self.board.tile_size,text="?",fill="")

        self.graphic_conectors=[self.top_box,self.right_box,self.bottom_box,self.left_box]
        self.graphics=[self.on_box,self.gen_box,self.top_box,self.bottom_box,self.left_box,self.right_box,self.missing_key]

        self.name=""

    def save_to_file(self):
    	out=["gen,check:"]
    	out.append("[")
    	for check in self.conector_checks:
    		out.append(str(check.get()))
    		out.append('.')
    	out.pop(len(out)-1)
    	out.append('],subname:'+self.name+',invert:'+str(self.invert.get()))

    	return ''.join(out)

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
            print('Generator has no input')

class Switch(Tile):

    def __init__(self, *args):

        super().__init__(*args)


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

        self.name=""
        self.state=0

    def save_to_file(self):
    	out=["switch,check:"]
    	out.append("[")
    	for check in self.conector_checks:
    		out.append(str(check.get()))
    		out.append('.')
    	out.pop(len(out)-1)
    	out.append('],subname:'+self.name+',invert:'+str(self.invert.get()))

    	return ''.join(out)

    def graphic_update(self):

        for check, box in zip(self.conector_checks,self.graphic_conectors):
            if(check.get()==1):
                self.board.canvas.itemconfig(box,fill="#FF0000")
            else:
                self.board.canvas.itemconfig(box,fill="")

        try:
            if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get()):
                for box,check in zip(self.on_conectors,self.conector_checks):
                    if(check.get()==1):
                        self.board.canvas.itemconfig(box,fill="#FF0000")
            else:
                for box in self.on_conectors:
                    self.board.canvas.itemconfig(box,fill="")
            self.board.canvas.itemconfig(self.missing_key,fill="")
        except KeyError:
            self.board.canvas.itemconfig(self.missing_key,fill="#FFFF00")

    def input_update(self):
        if(self.inputs[1]==1 or self.inputs[3]==1):
            self.state=1
        else:
            self.state=0


    def output_update(self):
        try:

            if(self.state==1):
                for ind,check,direction in zip(self.adj_ind,self.conector_checks,[2,3,0,1]):

                    if(self.board.flags[self.subscribe_name.get()][1]==self.invert.get() 
                        and check.get()==1
                        and ind!=None):
                        self.board.tiles[ind[0]][ind[1]].inputs[direction]=1


        except KeyError:
            pass

class Counter(Tile):

    def __init__(self, *args):

        super().__init__(*args)


        self.conector_checks[0].set(0)
        self.conector_checks[1].set(1)
        self.conector_checks[2].set(1)
        self.conector_checks[3].set(1)

        vcmd = (self.root.register(self.validate), '%P', '%s')

        self.count_upto=tk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd)
        self.count_upto.pack()
        self.count_upto.insert(0,"1")

        self.upto=1
        self.counter=0
        self.edge=0

        self.auto_reset=tk.IntVar()
        self.auto_reset_cheack=tk.Checkbutton(master=self.frame,text="Auto Reset",variable=self.auto_reset,onvalue='1',offvalue='0')

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
    	out=["counter,up_to:"+str(self.upto)]
    	out.append(',reset:'+str(self.auto_reset.get()))


    def validate(self,P,s):

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
            else:
                self.board.canvas.itemconfig(box,fill="")


        self.board.canvas.itemconfig(self.text_box,text=str(self.counter)+"+")

        if(self.counter>=self.upto):
            self.board.canvas.itemconfig(self.text_box,fill="#00FF00")
        else:
            self.board.canvas.itemconfig(self.text_box,fill="#000000")


    def input_update(self):

        if(self.auto_reset.get()==1):
            self.bottom.set(0)
        else:
            self.bottom.set(1)

        if(self.inputs[3]==0):
            self.edge=1
        elif(self.inputs[3]==1):
            
            if(self.edge==1 and self.counter<self.upto):
                self.counter+=1
            self.edge=0

        if(self.inputs[2]==1):
            self.counter=0


    def output_update(self):
        print(self.counter)

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
        self.conector_checks[3].set(1)

        vcmd = (self.root.register(self.validate), '%P', '%s')

        self.time_in=tk.Entry(master=self.frame,width=10,validate="key",validatecommand=vcmd)
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
    	out=["pulsar,time_to:"+str(self.time_to)]
    	return ''.join(out)

    def validate(self,P,s):

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

        
