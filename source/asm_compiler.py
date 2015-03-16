
# from tiles import Tile, Relay, Source, Flag, Generator, Switch, Counter,Pulsar,Timer,Sequencer

import tiles as tile_mod


class Node:

    def __init__(self,board,tile,x,y):

        self.cycles=0
        self.info={}

        self.board=board
        self.info['coords']=[x,y]
        


        self.info['outputs']=[]

        for ind, check, direction in zip(tile.adj_ind,tile.conector_checks,[2,3,0,1]):
            if (ind!=None and check.get()==1):

                if (type(self.board.tiles[ind[0]][ind[1]])==tile_mod.Relay
                    and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==1):
                    self.info['outputs'].extend(self.parse_relays(self.board.tiles[ind[0]][ind[1]]))

                else:
                    potencial_tile=self.parse_non_relay_conections(ind, check, direction)
                    if(potencial_tile!=None):
                        self.info['outputs'].append(potencial_tile)

        


        self.info["save"]=tile.save_to_file()

        print(self.info)

    def Source_generate(self):
        pass
    def Flag_generate(self):
        pass
    def Generator_generate(self):
        pass
    def Switch_generate(self):
        pass
    def Counter_generate(self):
        pass
    def Pulsar_generate(self):
        pass
    def Timer_generate(self):
        pass
    def Sequencer_generate(self):
        pass




    def propose_code(self,total_cycles):

        pass



    def parse_relays(self,relay_example):
        i=relay_example.state_index

        out=[]
        for tile in self.board.relay_groups[i]:

            for ind, check, direction in zip(tile.adj_ind,tile.conector_checks,[2,3,0,1]):


                if(ind!=None and check.get()==1
                    and type(self.board.tiles[ind[0]][ind[1]])!=tile_mod.Tile 
                    and type(self.board.tiles[ind[0]][ind[1]])!=tile_mod.Relay):


                    potencial_tile=self.parse_non_relay_conections(ind, check, direction)
                    if(potencial_tile!=None):
                        out.append(potencial_tile)

        return out




    def parse_non_relay_conections(self,ind, check, direction):


        if(type(self.board.tiles[ind[0]][ind[1]])==tile_mod.Counter
            and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0
            and direction==2):

            return self.tile_coord_label(ind[0],ind[1],"reset")


        elif(type(self.board.tiles[ind[0]][ind[1]])==tile_mod.Timer
            and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0
            and direction==2):

            return self.tile_coord_label(ind[0],ind[1],"reset")

        elif(self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==2):

            return self.tile_coord_label(ind[0],ind[1],"con")





        return None




    def tiles_outputed_to_by_relay(self,index,relay_group):
        pass

    def tile_coord_label(self,x,y,extra=""):
        return "tile_"+str(x)+"_"+str(y)+extra


    def delay_code(self,cycles):

        assert(type(cycles)==int)
        if(cycles==0):
            return [""]

        if(0<cycles<4):
            return [" NOP"]*cycles

        if(3<cycles<7):
            return [" CALL small_delay_"+str(cycles)]

        if(int(cycles/3)-2>255):
            raise OverflowError

        if(6<cycles):
            return [" MOVLW "+str(int(cycles/3)-2)," CALL delay3_"+str( 3 if cycles%3==0 else cycles%3)]


class Compiler:

    def __init__(self,board):

        self.total_cycles=0
        self.board=board

        self.tiles_linear=[]




        for x,col in enumerate(self.board.tiles):
            for y,tile in enumerate(col):

                if(type(tile)!=tile_mod.Tile and type(tile)!=tile_mod.Relay):

                    self.tiles_linear.append(Node(self.board,tile,x,y))




    def get_code(self,ioinfo):

        pass





    def delay_footer(self):
        return ["small_delay_6 nop",
        "small_delay_5 nop",
        "small_delay_4 return",
        "delay3_3 Nop",
        "delay3_2 Nop",
        "delay3_1 Decfsz w,w",
        "goto delay1_0",
        "return"]


if __name__ == '__main__':
    c=Compiler()

    print(c.delay_code(11))
    print(c.delay_footer())