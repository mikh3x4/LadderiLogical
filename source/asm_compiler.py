import tiles as tiles_mod
import math
import tkinter as tk
import tkinter.ttk as ttk
import time

class Node:

    def __init__(self,board,tile,x,y,proc_speed):
        self.proc_speed=proc_speed
        self.code=[]

        self.board=board

        self.x=x
        self.y=y
        
        self.outputs=[]

        for ind, check, direction in zip(tile.adj_ind,tile.conector_checks,[2,3,0,1]):
            if (ind!=None and check.get()==1):

                if (type(self.board.tiles[ind[0]][ind[1]])==tiles_mod.Relay
                    and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==1):
                    self.outputs.extend(self.parse_relays(self.board.tiles[ind[0]][ind[1]]))

                else:
                    potencial_tile=self.parse_non_relay_conections(ind, check, direction)
                    if(potencial_tile!=None):
                        self.outputs.append(potencial_tile)

        self.save_file=tile.save_to_file()

        print(x,y,self.outputs,self.save_file)

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]

        return out

    def get_register_names(self):
        out=[]

        return out


    def set_bit_flag_names(self,bit_reg):
        self.bit_reg=bit_reg


    def parse_relays(self,relay_example):
        i=relay_example.state_index

        out=[]
        for tile in self.board.relay_groups[i]:

            for ind, check, direction in zip(tile.adj_ind,tile.conector_checks,[2,3,0,1]):


                if(ind!=None and check.get()==1
                    and type(self.board.tiles[ind[0]][ind[1]])!=tiles_mod.Tile 
                    and type(self.board.tiles[ind[0]][ind[1]])!=tiles_mod.Relay):


                    potencial_tile=self.parse_non_relay_conections(ind, check, direction)
                    if(potencial_tile!=None):
                        out.append(potencial_tile)

        return out

    def parse_non_relay_conections(self,ind, check, direction):


        if(type(self.board.tiles[ind[0]][ind[1]])==tiles_mod.Counter
            and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0
            and direction==2):

            return self.tile_label(ind[0],ind[1],"reset")


        elif(type(self.board.tiles[ind[0]][ind[1]])==tiles_mod.Timer
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
            return [" MOVLW "+"d'"+str(int(cycles/3)-2)+"'"," CALL delay3_"+str( 3 if cycles%3==0 else cycles%3)]

class SourceNode(Node):

    def get_minimum_cycles(self):
        return len(self.outputs)

    def adjust_cycles(self,proposed_total_cycles):
        return len(self.outputs)



    def generate_code(self,total_cycles):
        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])


class FlagNode(Node):

    def get_minimum_cycles(self):
        return 4

    def adjust_cycles(self,proposed_total_cycles):
        return 4

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]
        out.append("flag_"+self.save_file["pubname"])

        return out

    def generate_code(self,total_cycles):

        assert(self.outputs==[])

        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
        flag_name=self.bit_reg["flag_"+self.save_file["pubname"]]

        self.code.append(" BCF "+flag_name)
        self.code.append(" BTFSC "+input_name)
        self.code.append(" BSF "+flag_name)
        self.code.append(" BCF "+input_name)


class GeneratorNode(Node):

    def get_minimum_cycles(self):
        return len(self.outputs)+4

    def adjust_cycles(self,proposed_total_cycles):
        return len(self.outputs)+4

    def generate_code(self,total_cycles):

        flag_read_name=self.bit_reg["flag_"+self.save_file["subname"]]


        if(self.save_file['invert']==1):
            self.code.append(" BTFSS "+flag_read_name)
        else:
            self.code.append(" BTFSC "+flag_read_name)

        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip"))

        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

        self.code.append(self.tile_label(self.x,self.y,"skip"))
        self.code.extend(self.delay_code(len(self.outputs)+1))

        self.code.append(self.tile_label(self.x,self.y,"end"))


class SwitchNode(Node):

    def get_minimum_cycles(self):
        return len(self.outputs)+6

    def adjust_cycles(self,proposed_total_cycles):
        return len(self.outputs)+6

    def generate_code(self,total_cycles):

        flag_read_name=self.bit_reg["flag_"+self.save_file["subname"]]
        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]

        self.code.append(" BTFSC "+input_name)


        if(self.save_file['invert']==1):

            self.code.append(" BTFSS "+flag_read_name)
        else:
            self.code.append(" BTFSC "+flag_read_name)


        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip"))

        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

        self.code.append(self.tile_label(self.x,self.y,"skip"))
        self.code.extend(self.delay_code(len(self.outputs)+1))

        self.code.append(self.tile_label(self.x,self.y,"end"))
        self.code.append(" BCF "+input_name)



class CounterNode(Node):

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]
        out.append(self.tile_label(self.x,self.y,"reset"))
        out.append(self.tile_label(self.x,self.y,"edge"))

        if(self.save_file['reset']==0):
            out.append(self.tile_label(self.x,self.y,"reset"))

        return out

    def get_minimum_cycles(self):
        return len(self.outputs)+15
        #multibyte

    def adjust_cycles(self,proposed_total_cycles):
        return len(self.outputs)+15
        #multibyte

    def get_register_names(self):
        out=[]
        out.append(self.tile_label(self.x,self.y,"counter"))
         #more registers in multi byte case

        return out

    def generate_code(self,total_cycles):

        if(self.save_file['up_to']>255):
            print('counter too big for single register')
            raise UserWarning


        if(self.save_file['reset']==1):
            self.generate_code_autoreset_sub255(total_cycles)
        elif(self.save_file['reset']==0):
            self.generate_code_manualreset_sub255(total_cycles)
        else:
            print("unimplmented counter configuration")

    def generate_code_manualreset_sub255(self,total_cycles):


        up_to=self.save_file['up_to']
        edge=self.bit_reg[self.tile_label(self.x,self.y,"edge")]
        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]

        reset_name=self.bit_reg[self.tile_label(self.x,self.y,"reset")]

        counter_register=self.tile_label(self.x,self.y,"counter")

        self.code.append(" BTFSC "+reset_name)
        self.code.append(" CLRF "+counter_register)

        self.code.append(" BTFSS "+edge)
        self.code.append(" BTFSS "+input_name)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"no_act"))

        self.code.append(" MOVLW d'"+str(up_to)+"'")
        self.code.append(" XORWF "+counter_register+",W")
        self.code.append(" BTFSS STATUS,Z")
        self.code.append(" goto "+self.tile_label(self.x,self.y,"increment"))

        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

        self.code.extend(self.delay_code(len(self.outputs)+3))
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))


        self.code.append(self.tile_label(self.x,self.y,"increment"))
        self.code.append(" INCF "+counter_register+",F")


        self.code.append(self.tile_label(self.x,self.y,"end"))
        
        self.code.append(" BCF "+edge)
        self.code.append(" BTFSC "+input_name)
        self.code.append(" BSF "+edge)

        self.code.append(" BCF "+input_name)

    def generate_code_autoreset_sub255(self,total_cycles):

        up_to=self.save_file['up_to']
        edge=self.bit_reg[self.tile_label(self.x,self.y,"edge")]
        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]

        counter_register=self.tile_label(self.x,self.y,"counter")


        self.code.append(" BTFSS "+edge)
        self.code.append(" BTFSS "+input_name)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"no_act"))

        self.code.append(" INCF "+counter_register+",F")
        self.code.append(" MOVLW d'"+str(up_to)+"'")
        self.code.append(" XORWF "+counter_register+",W")
        self.code.append(" BTFSS STATUS,Z")
        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip"))

        self.code.append(" CLRF "+counter_register)
        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

        self.code.append(self.tile_label(self.x,self.y,"no_act"))
        self.code.extend(self.delay_code(len(self.outputs)+5))
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))

        self.code.append(self.tile_label(self.x,self.y,"skip"))
        self.code.extend(self.delay_code(len(self.outputs)+2))

        self.code.append(self.tile_label(self.x,self.y,"end"))
        
        self.code.append(" BCF "+edge)
        self.code.append(" BTFSC "+input_name)
        self.code.append(" BSF "+edge)

        self.code.append(" BCF "+input_name)


class TimerNode(Node):

    def get_minimum_cycles(self):
        if(self.save_file['mode']==1):
            #hold 
            return len(self.outputs)+14
        elif(self.save_file['mode']==2):
            #delay monostable
            print("unimplmented timer (delay monostable) configuration")
        elif(self.save_file['mode']==3):
            #manual
            print("unimplmented timer (manual) configuration")
        else:
            print("unimplmented timer configuration")

    def adjust_cycles(self,proposed_total_cycles):

        self.loops_proposed=int((self.save_file['time_to']/1000)/((proposed_total_cycles)/self.proc_speed))

        if(self.save_file['mode']==1):
            #hold config
            if(self.loops_proposed<256):
                return len(self.outputs)+14
            if(self.loops_proposed<65536):
                return len(self.outputs)+24
            else:
                print("timer overflows two bytes")


        elif(self.save_file['mode']==2):
            #delay monostable
            print("unimplmented timer (delay monostable) configuration")
        elif(self.save_file['mode']==3):
            #manual
            print("unimplmented timer (manual) configuration")
        else:
            print("unimplmented timer configuration")

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]

        if(self.save_file['mode']==3):
            #manual mode
            out.append(self.tile_label(self.x,self.y,"reset"))

        return out

    def get_register_names(self):
        out=[]
        out.append(self.tile_label(self.x,self.y,"loop_counter_lo"))
        #more registers in multi byte case
        if(self.loops_proposed>255):
            out.append(self.tile_label(self.x,self.y,"loop_counter_hi"))

        return out

    def generate_code(self,total_cycles):

        #better value for loops using adjusted cycles
        self.loops=int((self.save_file['time_to']/1000)/((total_cycles)/self.proc_speed))

        if(self.save_file['mode']==1):
            #hold config
            if(self.loops_proposed<255):
                self.generate_code_hold_1byte(total_cycles)
            if(self.loops_proposed<65535):
                self.generate_code_hold_2byte(total_cycles)
            else:
                print("timer overflows two bytes")


        elif(self.save_file['mode']==2):
            #delay monostable
            print("unimplmented timer (delay monostable) configuration")
        elif(self.save_file['mode']==3):
            #manual
            print("unimplmented timer (manual) configuration")
        else:
            print("unimplmented timer configuration")


    def generate_code_hold_1byte(self,total_cycles):
        assert(self.loops<256)

        
        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
        counter_register=self.tile_label(self.x,self.y,"loop_counter")  

        self.code.append(" BTFSS "+input_name)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"no_rest"))
        self.code.append(" MOVLW d'"+str(self.loops)+"'")
        self.code.append(" MOVWF "+counter_register)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end_temp"))

        self.code.append(self.tile_label(self.x,self.y,"no_rest"))
        self.code.append([' NOP']*3)
        self.code.append(self.tile_label(self.x,self.y,"end_temp"))

        self.code.append(" CLRF W")
        self.code.append(" XORWF "+counter_register+",W")
        self.code.append(" BTFSC STATUS,Z")
        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip"))
        self.code.append(" DECF "+counter_register+",F")
        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))
        self.code.append(self.tile_label(self.x,self.y,"skip"))
        self.code.extend(self.delay_code(len(self.outputs)+2))
        self.code.append(self.tile_label(self.x,self.y,"end"))
        self.code.append(" BCF "+input_name)


    def generate_code_hold_2byte(self,total_cycles):
        assert(self.loops<256**2)

        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
        counter_register_hi=self.tile_label(self.x,self.y,"loop_counter_hi")
        counter_register_lo=self.tile_label(self.x,self.y,"loop_counter_lo") 

        self.code.append(" BTFSS "+input_name)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"no_rest"))



        self.code.append(" MOVLW d'"+str(self.loops%256)+"'")
        self.code.append(" MOVWF "+counter_register_lo)

        self.code.append(" MOVLW d'"+str(self.loops//256)+"'")
        self.code.append(" MOVWF "+counter_register_hi)

        self.code.append(" goto "+self.tile_label(self.x,self.y,"end_temp"))

        self.code.append(self.tile_label(self.x,self.y,"no_rest"))
        self.code.extend(self.delay_code(5))
        self.code.append(self.tile_label(self.x,self.y,"end_temp"))

        self.code.append(" CLRF W")
        self.code.append(" XORWF "+counter_register_lo+",W")

        self.code.append(" BTFSC STATUS,Z")
        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip1"))

        self.code.append(" CLRF W")
        self.code.append(" XORWF "+counter_register_hi+",W")

        self.code.append(" BTFSC STATUS,Z")
        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip2"))

        self.code.append(" CLRF W")
        self.code.append(" XORWF "+counter_register_lo+",W")
        self.code.append(" BTFSC STATUS,Z")
        self.code.append(" DECF "+counter_register_hi+",F")
        self.code.append(" DECF "+counter_register_lo+",F")

        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])

        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))
        self.code.append(self.tile_label(self.x,self.y,"skip1"))
        self.code.extend(self.delay_code(4))
        self.code.append(self.tile_label(self.x,self.y,"skip2"))
        self.code.extend(self.delay_code(len(self.outputs)+6))

        self.code.append(self.tile_label(self.x,self.y,"end"))
        self.code.append(" BCF "+input_name)



class PulsarNode(Node):

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]
        out.append(self.tile_label(self.x,self.y,"state"))

        return out

    def get_register_names(self):
        out=[]

        for i in range(self.number_of_bytes):
            out.append(self.tile_label(self.x,self.y,"pulsar_counter_"+str(i)))

        return out

    def get_minimum_cycles(self):
        return 22+len(self.outputs)

    def adjust_cycles(self,proposed_total_cycles):

        self.loops_proposed=int((self.save_file['time_to']/1000)/((proposed_total_cycles)/self.proc_speed))

        assert(self.loops_proposed)

        self.number_of_bytes=int(math.log(self.loops_proposed,2)//8)+1
        return 15+len(self.outputs)+7*self.number_of_bytes


    def generate_code(self,total_cycles):


        self.loops=int((self.save_file['time_to']/1000)/((total_cycles)/self.proc_speed))

        if(self.number_of_bytes>5):
            print("Are you sure? Number of bytes used for puslar is over 5!")

        self.generate_kbyte_code(total_cycles)



    def generate_kbyte_code(self,total_cycles):


        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
        out_state=self.bit_reg[self.tile_label(self.x,self.y,"state")]


        loop_vals=[]
        loops=self.loops

        for i in range(self.number_of_bytes):
            loop_vals.append(loops%256)
            loops=loops//256



        self.code.append(" BTFSS "+input_name)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"off"))



        for i in range(self.number_of_bytes):
            self.code.append(" INCF "+self.tile_label(self.x,self.y,"pulsar_counter_"+str(i))+",F")
            
            if(i!=self.number_of_bytes-1):
                self.code.append(" BTFSC STATUS,Z")

        for i in range(self.number_of_bytes):
            self.code.append(" MOVLW d'"+str(loop_vals[i])+"'")
            self.code.append(" XORWF "+self.tile_label(self.x,self.y,"pulsar_counter_"+str(i))+",W")
            self.code.append(" BTFSS STATUS,Z")
            self.code.append(" goto "+self.tile_label(self.x,self.y,"out_"+str(i)))


        self.code.append(" MOVLW "+"d'"+str(2**int(out_state[-1]))+"'")
        self.code.append(" XORWF "+out_state[:-2]+",F")

        self.code.append(self.tile_label(self.x,self.y,"off"))

        for i in range(self.number_of_bytes):
            self.code.append(" CLRF "+self.tile_label(self.x,self.y,"pulsar_counter_"+str(i)))


        self.code.append(" goto "+self.tile_label(self.x,self.y,"mid"))


        for i in range(self.number_of_bytes):
            self.code.append(self.tile_label(self.x,self.y,"out_"+str(i)))

            if(i==self.number_of_bytes-1):
                self.code.extend(self.delay_code(3+self.number_of_bytes))
            else:
                self.code.extend(self.delay_code(4))


        self.code.append(self.tile_label(self.x,self.y,"mid"))

        delay_temp=self.delay_code(6*self.number_of_bytes+1)

        self.code.extend(delay_temp[:-1]) #ensure it is single line (goto forced)

        self.code.append(" BTFSS "+input_name)
        self.code.append(delay_temp[-1]+';ensure it is single line (goto forced)') #ensure it is single line (goto forced)

        self.code.append(" BTFSS "+input_name)
        self.code.append(" BSF "+out_state)

        self.code.append(" BTFSC "+input_name)
        self.code.append(" BTFSS "+out_state)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"skip_out"))

        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])

        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))
        self.code.append(self.tile_label(self.x,self.y,"skip_out"))
        self.code.extend(self.delay_code(len(self.outputs)+1))

        self.code.append(self.tile_label(self.x,self.y,"end"))
        self.code.append(" BCF "+input_name)




class SequencerNode(Node):

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]
        out.append(self.tile_label(self.x,self.y,"edge"))

        out.extend(map(lambda x:"flag_"+x,self.save_file["steps"]))

        return out

    def get_minimum_cycles(self):
        return 3*len(self.save_file['steps'])+10
        

    def adjust_cycles(self,proposed_total_cycles):
        return 3*len(self.save_file['steps'])+10


    def generate_code(self,total_cycles):

        edge=self.bit_reg[self.tile_label(self.x,self.y,"edge")]
        input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]



        self.code.append(" BTFSS "+edge)
        self.code.append(" BTFSS "+input_name)
        self.code.append(" goto "+self.tile_label(self.x,self.y,"no_inc"))



        for position,step in enumerate(self.save_file['steps']):

            seq=self.bit_reg["flag_"+step]
            seq_label="not_seq_"+step


            self.code.append(" BTFSS "+seq)
            # BTFSS seq_1


            # goto not_seq_1
            self.code.append(" goto "+self.tile_label(self.x,self.y,seq_label))

            # BCF seq_1
            # BSF seq_2
            self.code.append(" BCF "+seq)
            self.code.append(" BSF "+self.bit_reg["flag_"+self.save_file['steps'][(position+1)%len(self.save_file['steps'])]])


            # delay start at (n-1)*3 and count down

            self.code.extend(self.delay_code(3*(len(self.save_file['steps'])-1)-position*3))


            self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))
            # goto end

            self.code.append(self.tile_label(self.x,self.y,seq_label))
            # not_seq_1 




        # BTFSS seq_1
        # goto not_seq_1
        # BCF seq_1
        # BSF seq_2
        # delay start at (n-1)*3 and count down
        # goto end
        # not_seq_1 

        # BTFSS seq_2
        # goto not_seq_2
        # BCF seq_2
        # BSF seq_3
        # delay 3
        # goto end
        # not_seq_2

        # BTFSS seq_3
        # goto not_seq_3
        # BCF seq_3
        # BSF seq_1
        # delay 0
        # goto end
        # not_seq_3


        self.code.append(" BSF "+self.bit_reg["flag_"+self.save_file["steps"][0]])
        self.code.append(" goto "+self.tile_label(self.x,self.y,"end"))


        self.code.append(self.tile_label(self.x,self.y,"no_inc"))

        self.code.extend(self.delay_code(3*len(self.save_file['steps'])+2))

        self.code.append(self.tile_label(self.x,self.y,"end"))

        self.code.append(" BCF "+edge)
        self.code.append(" BTFSC "+input_name)
        self.code.append(" BSF "+edge)
        
        self.code.append(" BCF "+input_name)



class Compiler:

    def __init__(self,board,io,typ="plain"):

        self.typ=typ

        self.Tile_Node_Links={tiles_mod.Source: SourceNode,
                            tiles_mod.Flag: FlagNode,
                            tiles_mod.Generator: GeneratorNode,
                            tiles_mod.Switch: SwitchNode,
                            tiles_mod.Counter: CounterNode,
                            tiles_mod.Pulsar: PulsarNode,
                            tiles_mod.Timer: TimerNode,
                            tiles_mod.Sequencer: SequencerNode}

        self.proc_speed=4*10**6
        self.total_cycles=0
        self.board=board
        self.io=io
        self.registers=[]

        self.tiles_linear=[]


        for x,col in enumerate(self.board.tiles):
            for y,tile in enumerate(col):

                if(type(tile)!=tiles_mod.Tile and type(tile)!=tiles_mod.Relay):

                    self.tiles_linear.append(self.Tile_Node_Links[type(tile)](self.board,tile,x,y,self.proc_speed))


        self.get_code()

    def generate_portb_update(self,output_repete):
        out=[]
        print(output_repete)
        for index,lis in enumerate(output_repete):
            for r in lis:
                out.append(' BCF special_temp_PORTB,'+str(r))
                out.append(' BTFSC special_temp_PORTB,'+str(index))
                out.append(' BSF special_temp_PORTB,'+str(r))

        out.extend([' MOVF special_temp_PORTB,W',' MOVWF PORTB'])

        return out

    def get_code(self):

        self.bitflag_register_names={}
        bitflag_base_name="bitflag_reg"

        io_data=self.io.save_to_file()

        output_repete=[[],[],[],[],[],[],[],[]]

        i=0
        for flag in io_data['outputs']:
            try:
                original_out=self.bitflag_register_names["flag_"+flag]
                output_repete[int(original_out[-1])].append(i)

            except KeyError:
                self.bitflag_register_names["flag_"+flag]="special_temp_PORTB,"+str(i)#overwriting higher outputs

                
            i+=1


        portb_copy_code=self.generate_portb_update(output_repete)


        #move before register to register multi byte timers
        proposed_total_cycles=sum(tile.get_minimum_cycles() for tile in self.tiles_linear)+len(portb_copy_code)+2 #plus two due to goto main + multiout
        total_cycles=sum(tile.adjust_cycles(proposed_total_cycles) for tile in self.tiles_linear)+len(portb_copy_code)+2 #plus two due to goto main + multiout

        i=0
        n=1

        self.registers.append(bitflag_base_name+'_0')
        for tile in self.tiles_linear:
            self.registers.extend(tile.get_register_names())
            bits=tile.get_bitflag_names()
            for bit in bits:
                if(i==8):
                    i=0
                    n+=1
                    self.registers.append(bitflag_base_name+'_'+str(n))
                assert(i<8)

                try:
                    self.bitflag_register_names[bit]
                    #some times its forceed to a special register as its in the output
                except KeyError:
                    self.bitflag_register_names[bit]=bitflag_base_name+'_'+str(n)+","+str(i)
                    i+=1

        i=0
        for flag in io_data['inputs']:
            self.bitflag_register_names["flag_"+flag]="PORTA,"+str(i)#garantiude to be unique by GUI
            i+=1

        for tile in self.tiles_linear:
            tile.set_bit_flag_names(self.bitflag_register_names)

        


        for tile in self.tiles_linear:
            tile.generate_code(total_cycles)

        #write code to out
        self.registers.extend(['special_temp_portb'])

        out=[]

        comment_header=''';----------------------------------------------------------;
; Program title: Compiled Result                           ;
;----------------------------------------------------------;
; Code generated by: LadderiLogical                        ;
;----------------------------------------------------------;
; Date:  '''+time.strftime("%c")+'''                          ;
;----------------------------------------------------------;
; Version:          1.0                                    ;
;----------------------------------------------------------;
; Device:  PIC16F627A                                      ;
;----------------------------------------------------------;
; Oscillator: Internal 4  MHz                              ;
;----------------------------------------------------------;
; Cycles per main loop: '''+str(total_cycles)+" "*(35-len(str(total_cycles)))+''';
;----------------------------------------------------------;'''

        comment_char=';'
        if(self.typ=='Debug'):
            self.registers.extend(['porta','portb'])
            comment_header=comment_header.replace(';','#')
            comment_char='#'

        out.append(comment_header)

        out.append('')
        out.append(comment_char+'Registers:')
        out.extend((comment_char+x for x in self.registers))

        out.append('')



        out.append(comment_char+'Bitflags:')
        human_readable_register_names={v: k for k, v in self.bitflag_register_names.items()}

        for io_register in ("PORTA,"+str(i) for i in range(8)):
            try:
                out.append(comment_char+io_register+': '+human_readable_register_names[io_register])
            except KeyError:
                out.append(comment_char+io_register+':')
            else:
                del human_readable_register_names[io_register]

        for io_register in ("special_temp_PORTB,"+str(i) for i in range(8)):
            try:
                out.append(comment_char+io_register+': '+human_readable_register_names[io_register])
            except KeyError:
                out.append(comment_char+io_register+':')
            else:
                del human_readable_register_names[io_register]

        human_readable_register_names={v: k for k, v in human_readable_register_names.items()}
        for tiles_bitflags,other_registers in sorted(human_readable_register_names.items()):
            out.append(comment_char+other_registers+': '+tiles_bitflags)
        out.append('')

        if(self.typ=='MPLab'):
            out.append('''
LIST  P=PIC16F627A ;select device
    ;Tells MPLAB what processor IC is being used
  INCLUDE  c:\program files (x86)\microchip\MPASM Suite\P16F627A.inc
    ;include header file
    ;from default location
    ;tells the MPLAB where to find the files

  __config 0x3F10     ;sets config to; internal  I/O, no watchdog,Power
    ;up timer on, master Reset off,
    ;no brown-out, no LV program, no read protect,
    ;no code protect
;----------------------------------------------------------;
; DEFINE REGISTERS                                         ;
;----------------------------------------------------------;

    cblock  0x20''')
            out.extend((x for x in self.registers))

            out.append('''
    endc

init    
     MOVLW d'07'
     MOVWF CMCON         ;Disable comparators
     BSF STATUS, RP0     ;select bank1 for setup
     BSF PCON, OSCF      ;select 4 MHz
     MOVLW b'01110000'
     MOVWF TRISA         ;set PortA as inputs on designated pins
     MOVLW b'00000000'
     MOVWF TRISB         ;set PortB all outputs
     BCF STATUS, RP0     ;return to bank0 for program operation''')

            out.extend((" CLRF "+x for x in self.registers))


        if(self.typ=='Debug'):
            out.append('from PICclass import run_PIC')
            out.append('reg=[')
            out.extend(("'"+x+"'," for x in self.registers))
            out.append(']')




        out.append('')

        if(self.typ=='Debug'):
            out.append("instructions='''")
        out.append('main')
        for tile in self.tiles_linear:
            out.extend(tile.code)

        #fixs outputs on multyple pins remember about time fixing

        out.append('')
        out.extend(portb_copy_code)
        out.append(' goto main')#plus 2 to cycles
        out.extend(self.delay_footer())
        out.append(' END')

        if(self.typ=='Debug'):
            out.append("'''")
            out.append("run_PIC(reg,instructions)")

        print('\n'.join(out))

        CompilerWindow('\n'.join(out))


    def delay_footer(self):
        return ["small_delay_6 nop",
        "small_delay_5 nop",
        "small_delay_4 return",
        "delay3_3 Nop",
        "delay3_2 Nop",
        "delay3_1 Decfsz W,W",
        " goto delay3_1",
        " return"]

class CompilerSettingsWindow():

    def __init__(self,board,io):
        self.root=tk.Toplevel()
        self.root.title('Compiler Settigs')

        self.plain=ttk.Button(master=self.root,text="Plain",command=lambda:self.run_complier(board,io,typ="plain"))
        self.MPLab=ttk.Button(master=self.root,text="MPLab",command=lambda:self.run_complier(board,io,typ="MPLab"))
        self.Debug=ttk.Button(master=self.root,text="Debug",command=lambda:self.run_complier(board,io,typ="Debug"))

        self.plain.pack()
        self.MPLab.pack()
        self.Debug.pack()

    def run_complier(self,board,io,typ):
        Compiler(board,io,typ=typ)
        self.root.destroy()

        


        

class CompilerWindow:

    def __init__(self,compiled_result):
        self.root=tk.Toplevel()
        self.root.title('Compiler Result')

        self.res=tk.Text(self.root)
        

        self.res.pack(fill=tk.BOTH, expand=1)
        self.res.insert(tk.END, compiled_result)

        self.res.bind("<Command-a>", self.select_all)

    def select_all(self,event):
        self.res.tag_add(tk.SEL, "1.0", tk.END)
        self.res.mark_set(tk.INSERT, "1.0")
        self.res.see(tk.INSERT)
        return 'break'





