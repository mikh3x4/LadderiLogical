from tiles import Tile, Relay, Source, Flag, Generator, Switch, Counter,Pulsar,Timer,Sequencer
import tkinter.ttk as ttk
import tkinter as tk
class TileBoard(ttk.Frame):
    def __init__(self, root,app,tile_size=50):
        ttk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.size_x=self.size_y=400
        self.tile_size=tile_size
        self.total_size_y=1000
        self.total_size_x=1400


        self.canvas = tk.Canvas(self, width=self.size_x, height=self.size_y, background="#7A7A7a")
        self.xsb = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,self.total_size_x,self.total_size_y))


        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.tiles=[[Source(root,self,r,i) if r==0 else Tile(root,self,r,i) for i in range(self.total_size_y//self.tile_size)] for r in range(self.total_size_x//self.tile_size)]

        for a in self.tiles:
            for b in a:
                b.generate_shortcuts()


        self.flags={}
        self.relay_states=[]
        self.relay_groups=[]

        self.canvas.bind("<ButtonPress-1>", self.click)
        self.canvas.bind("<Shift-ButtonPress-1>", self.shift_click)

        self.canvas.bind("<Control-ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<Control-B1-Motion>", self.scroll_move)

        self.canvas.bind("<MouseWheel>", self.on_mousewheel_y)
        self.canvas.bind("<Shift-MouseWheel>", self.on_mousewheel_x)



        self.bind("s", lambda x:self.app.tools.change_tool("select"))
        self.bind("a", lambda x:self.app.tools.change_tool("auto"))
        self.bind("f", lambda x:self.app.tools.change_tool("flag"))
        self.bind("h", lambda x:self.app.tools.change_tool("hswitch"))
        self.bind("x", lambda x:self.app.tools.change_tool("delete"))


        # self.canvas.bind("", lambda event: self.focus_set())

        self.previous_shift_comand=False
        # self.canvas.bind('<Motion>',self.motion)

        #Manual Initial selection
        self.sel_x=1
        self.sel_y=0

        self.canvas.create_rectangle(self.sel_x*self.tile_size,self.sel_y*self.tile_size,
            self.sel_x*self.tile_size+self.tile_size,self.sel_y*self.tile_size+self.tile_size, tags="selection_box",outline="#0000FF")

        self.tiles[self.sel_x][self.sel_y].frame.grid(column=1,row=1, sticky="nsew")


    def on_mousewheel_y(self, event):
        self.canvas.yview_scroll(-1*(event.delta), "units")

    def on_mousewheel_x(self, event):
        self.canvas.xview_scroll(-1*(event.delta), "units")


    def start(self):
        self.reintegrate_tiles()
        self.update_all()
        self.focus_set()

    def load_from_file(self,data):

        self.canvas.configure(scrollregion=(0,0,data["tile_number"][0],data["tile_number"][1]))
        self.total_size_x=data["tile_number"][0]*self.tile_size
        self.total_size_y=data["tile_number"][1]*self.tile_size

        # still no use as tile array non extendable

        tile_decode={"relay":Relay,"source":Source,"flag":Flag,"generator":Generator,
        "switch":Switch,"counter":Counter,"pulsar":Pulsar,"timer":Timer,"sequ":Sequencer}
        for x,col in enumerate(data['board']):
            for y,info in enumerate(col):
                if(info!="blk"):
                    print(info)
                    try:
                        self.convert_tile(x,y,tile_decode[info["0type"]])
                    except KeyError:
                        print("new tile is unsuported")
                    print(type(self.tiles[x][y]))
                    self.tiles[x][y].open_from_file(info)

        if(len(data)!=2): #tile_number board
            print("File contains unimplemented feature in TileBoard")


    def save_to_file(self):

        out={}

        out["tile_number"]=[len(self.tiles),len(self.tiles[0])]


        columns=[]
        for a in self.tiles:
            rows=[]
            for b in a:
                rows.append(b.save_to_file())
            columns.append(rows)

        out['board']=columns

        return out

    def reintegrate_tiles(self):
        self.relay_groups=[]
        self.relay_states=[]

        self.relays=[]
        self.functionals=[]

        for a in self.tiles:
            for b in a:
                if(type(b)==Relay):
                    self.relays.append(b)
                    self.relay_groups.append([b])
                elif(type(b)!=Relay and type(b)!=Tile):
                    self.functionals.append(b)

        for relay in self.relays:
            relay.reintegrate()

        i=0
        for group in self.relay_groups:
            self.relay_states.append(0)

            for relay in group:
                relay.state_index=i

            i+=1


    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)


    def convert_tile(self,x,y,typ):

        self.tiles[x][y].clean_delete()
        self.tiles[x][y]=typ(self.root,self,x,y)
        self.tiles[x][y].generate_shortcuts()

        if(x==self.sel_x and y==self.sel_y):
            self.tiles[x][y].frame.grid(column=1,row=1, sticky="nsew")


    def click(self,event):
        
        if(self.previous_shift_comand):
            self.app.tools.tool="select"

        self.shift_click(event)

        self.app.tools.tool="select"
        self.previous_shift_comand=False


    def shift_click(self,event):
        self.focus_set()
        if(self.app.tools.tool=='select'):
            self.tool_select(event)
        elif(self.app.tools.tool=='hswitch'):
            self.tool_hswitch(event)            

        elif(self.app.tools.tool=='horizontal'):
            self.tool_horizontal(event)
        elif(self.app.tools.tool=='delete'):
            self.tool_delete(event)
        elif(self.app.tools.tool=='flag'):
            self.tool_flag(event)
        elif(self.app.tools.tool=='auto'):
            self.tool_auto(event)
        else:
            print('Unrecognised tool')

        self.previous_shift_comand=True


    def tool_flag(self,event):

        coords=self.find_tile_coords(event)

        x=coords[0]
        y=coords[1]

        self.convert_tile(x,y,Flag)


    def tool_delete(self,event):

        coords=self.find_tile_coords(event)

        x=coords[0]
        y=coords[1]

        self.convert_tile(x,y,Tile)

    def tool_hswitch(self,event):

        coords=self.find_tile_coords(event)

        x=coords[0]
        y=coords[1]

        self.convert_tile(x,y,Switch)

        self.tiles[x][y].left.set(1)
        self.tiles[x][y].right.set(1)


    def tool_horizontal(self,event):

        coords=self.find_tile_coords(event)

        x=coords[0]
        y=coords[1]

        self.convert_tile(x,y,Relay)

        self.tiles[x][y].left.set(1)
        self.tiles[x][y].right.set(1)


    def tool_auto(self,event):

        coords=self.find_tile_coords(event)

        x=coords[0]
        y=coords[1]

        self.convert_tile(x,y,Relay)

        changee=self.tiles[x][y]
        for ind, check, direction in zip(changee.adj_ind,changee.conector_checks,[2,3,0,1]):

            if(ind==None):
                pass
            elif(type(self.tiles[ind[0]][ind[1]])==Relay):
                check.set(1)
                self.tiles[ind[0]][ind[1]].conector_checks[direction].set(1)
            elif(self.tiles[ind[0]][ind[1]].conector_checks[direction].get()==1):
                check.set(1)



    def tool_select(self, event):

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

        print(self.tiles[self.sel_x][self.sel_y])
        self.tiles[self.sel_x][self.sel_y].frame.grid(column=1,row=1, sticky="nsew")

    def find_tile_coords(self,event):
        global_x=event.x+self.xsb.get()[0]*self.total_size_x
        global_y=event.y+self.ysb.get()[0]*self.total_size_y
        print(global_x,global_y,'glob')


        x=int(global_x//self.tile_size)
        y=int(global_y//self.tile_size)

        return (x,y)

    def update_all(self):

        self.reintegrate_tiles()#If moved need to reset all states

        for tile in self.functionals:
            tile.update()


        for tile in self.relays:
            tile.input_update()
        for tile in self.relays:
            tile.inputs=[0,0,0,0]

        for tile in self.relays:
            tile.update()


        for tile in self.functionals:
            tile.input_update()
        for tile in self.functionals:
            tile.inputs=[0,0,0,0]

        try:
            self.app.io.update()
        except AttributeError:
            print('initialy no board existant')


        self.after(10,self.update_all)

        
        # size increase prvision
        # if(global_x>900):
        #     self.canvas.configure(scrollregion=(0,0,1500,1500))
        #     self.total_size_x=self.total_size_y=1500
