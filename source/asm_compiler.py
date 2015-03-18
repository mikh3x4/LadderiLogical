
# from tiles import Tile, Relay, Source, Flag, Generator, Switch, Counter,Pulsar,Timer,Sequencer

import tiles as tile_mod


class Node:

    def __init__(self,board,tile,x,y):

        self.cycles=0
        self.code=[]


        self.board=board

        self.x=x
        self.y=y
        


        self.outputs=[]

        for ind, check, direction in zip(tile.adj_ind,tile.conector_checks,[2,3,0,1]):
            if (ind!=None and check.get()==1):

                if (type(self.board.tiles[ind[0]][ind[1]])==tile_mod.Relay
                    and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==1):
                    self.outputs.extend(self.parse_relays(self.board.tiles[ind[0]][ind[1]]))

                else:
                    potencial_tile=self.parse_non_relay_conections(ind, check, direction)
                    if(potencial_tile!=None):
                        self.outputs.append(potencial_tile)

        self.save_file=tile.save_to_file()

        print(x,y,self.outputs,self.save_file)

    def get_bitflag_names(self):
        out=[self.tile_label(ind[0],ind[1],"con")]

        if(self.save_file['0type']=='timer'):
            out.append(self.tile_label(ind[0],ind[1],"reset"))

        elif(self.save_file['0type']=='counter'):
            out.append(self.tile_label(ind[0],ind[1],"reset"))
            out.append(self.tile_label(ind[0],ind[1],"edge"))

        elif(self.save_file['0type']=='flag'):
            out.append("flag_"+self.save_file["pubname"])


        elif(self.save_file['0type']=='sequ'):
            out.extend(map(lambda x:"flag_"+x,self.save_file["steps"]))


    def set_bit_flag_names(self,bit_reg):
        self.bit_reg=bit_reg



    def Source_generate(self):
        for out in self.outputs:
            self.code.append(" BSF "+out)

        self.cycles=len(self.outputs)

    def Flag_generate(self):

        assert(self.outputs==[])

        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
        flag_name=self.bit_reg["flag_"+self.save_file["pubname"]]

        self.code.append(" BCF "+flag_name)
        self.code.append(" BTFSC "+input_name)
        self.code.append(" BSF "+flag_name)
        self.code.append(" BCF "+input_name)

        self.cycles=4


    def Generator_generate(self):

        flag_read_name=self.bit_reg["flag_"+self.save_file["subname"]]


        if(self.save_file['invert']==1):
            self.code.append(" BTFSS "+flag_read_name)
        else:
            self.code.append(" BTFSC "+flag_read_name)

        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip"))

        for out in self.outputs:
            self.code.append(" BSF "+out)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

        self.code.append(self.tile_label(self.x,self.y,"skip"))
        self.code.extend(self.delay_code(len(self.outputs)+1))

        self.code.append(self.tile_label(self.x,self.y,"end"))


        self.cycles=len(self.outputs)+4

    def Switch_generate(self):

        flag_read_name=self.bit_reg["flag_"+self.save_file["subname"]]
        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]

        self.code.append(" BTFSC "+input_name)


        if(self.save_file['invert']==1):

            self.code.append(" BTFSS "+flag_read_name)
        else:
            self.code.append(" BTFSC "+flag_read_name)


        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip"))

        for out in self.outputs:
            self.code.append(" BSF "+out)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

        self.code.append(self.tile_label(self.x,self.y,"skip"))
        self.code.extend(self.delay_code(len(self.outputs)+1))

        self.code.append(self.tile_label(self.x,self.y,"end"))
        self.code.append(" BCF "+input_name)


        self.cycles=len(self.outputs)+6

    def Counter_generate(self):
        if(self.save_file['reset']==1):
            # auto_reset
            up_tp=self.save_file['up_to']
            edge=self.tile_label(self.x,self.y,"edge")
            input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
            counter_register=self.tile_label(self.x,self.y,"counter")

            if(up_to>255):
                print('counter too big for single register')
                raise UserWarning

            self.code.append(" BTFSS "+edge)
            self.code.append(" BTFSS "+input_name)
            self.code.append(" goto "+self.tile_label(self.x,self.y,"no_act"))

            self.code.append(" INCF "+counter_register+",F")
            self.code.append(" MOVLW d'"+up_to+"'")
            self.code.append(" XORFW "+counter_register+",W")
            self.code.append(" BTFSC STATUS,Z")
            self.code.append(" goto "+self.tile_label(self.x,self.y,"skip"))

            self.code.append("CLRF "+counter_register)
            for out in self.outputs:
                self.code.append(" BSF "+out)
            self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

            self.code.append(self.tile_label(self.x,self.y,"no_act"))
            self.code.extend(self.delay_code(len(self.outputs)+5))
            self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

            self.code.append(self.tile_label(self.x,self.y,"skip"))
            self.code.extend(self.delay_code(len(self.outputs)+2))

            self.code.append(self.tile_label(self.x,self.y,"end"))
            self.code.append(" BCF "+input_name)
            self.code.append(" BCF "+edge)
            self.code.append(" BTFSC "+input_name)
            self.code.append(" BSF "+edge)



            self.cycles=len(self.outputs)+15
            return
        else:
            # manual_reset

            return


    def Pulsar_generate(self):
        pass
    def Timer_generate(self):
        pass
    def Sequencer_generate(self):
        pass




    def propose_code(self,total_cycles):
        self.code=[]
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

            return self.tile_label(ind[0],ind[1],"reset")


        elif(type(self.board.tiles[ind[0]][ind[1]])==tile_mod.Timer
            and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0
            and direction==2):

            return self.tile_label(ind[0],ind[1],"reset")

        elif(self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==2):

            return self.tile_label(ind[0],ind[1],"con")

        return None



    def tile_label(self,x,y,extra=""):
        "Generates BOTH label and bit flag prefixes for tiles"
        return "tile_"+str(x)+"_"+str(y)+("_"+extra if extra!="" else "")


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

        self.register_names={}
        register_base_name="bitflag_reg"
        i=0
        n=1
        for tile in self.tiles_linear:
            if(i==8):
                i=0
                n+=1
            assert(i<8)

            self.register_names[tile.get_bitflag_names()]=register_base_name+'_'+str(n)+","+str(i)
            i+=1

        for tile in self.tiles_linear:
            tile.set_bit_flag_names(self.register_names)

            

        #Remamber about the register substitution



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