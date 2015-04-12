import tiles as tiles_mod


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
            return [" MOVLW "+str(int(cycles/3)-2)," CALL delay3_"+str( 3 if cycles%3==0 else cycles%3)]

class SourceNode(Node):

    def get_minimum_cycles(self):
        return len(self.outputs)

    def adjust_cycles(self,proposed_total_cycles):
        return len(self.outputs)



    def generate_code(self,total_cycles):
        for out in self.outputs:
            self.code.append(" BSF "+self.bit_reg[out])

        self.cycles=len(self.outputs)

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

        self.cycles=4

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


        self.cycles=len(self.outputs)+4

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


        self.cycles=len(self.outputs)+6

class CounterNode(Node):

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]
        out.append(self.tile_label(self.x,self.y,"reset"))
        out.append(self.tile_label(self.x,self.y,"edge"))

        return out

    def get_minimum_cycles(self):
        pass

    def adjust_cycles(self,proposed_total_cycles):
        pass

    def get_register_names(self):
        out=[]
        out.append(self.tile_label(self.x,self.y,"counter"))
         #more registers in multi byte case

        return out

    def generate_code(self,total_cycles):
        if(self.save_file['reset']==1):
            # auto_reset
            up_to=self.save_file['up_to']
            edge=self.bit_reg[self.tile_label(self.x,self.y,"edge")]
            input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]

            counter_register=self.tile_label(self.x,self.y,"counter")

            if(up_to>255):
                print('counter too big for single register')
                raise UserWarning

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



            self.cycles=len(self.outputs)+15
            return
        else:
            # manual_reset
            print("not implemented")

class TimerNode(Node):

    def get_minimum_cycles(self):
        pass

    def adjust_cycles(self,proposed_total_cycles):
        pass

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]
        out.append(self.tile_label(self.x,self.y,"reset"))

        return out

    def get_register_names(self):
        out=[]
        out.append(self.tile_label(self.x,self.y,"loop_counter"))
        #more registers in multi byte case

        return out

    def generate_code(self,total_cycles):

        if(self.previous_total_cycles==total_cycles):
            return

        self.previous_total_cycles=total_cycles
        

        if(self.save_file['mode']==1):
            use_bytes=0
            for byte_number,cycl in zip(range(1,2),[len(self.outputs)+14,len(self.outputs)+24]):
                loops=self.save_file['time_to']/((total_cycles-self.cycles+cycl)/self.proc_speed)
                if(loops<2**byte_number-1):
                    use_bytes=byte_number
                    break
            else:
                #for loop else
                print('timer too big for implemented register nubmers')
                raise UserWarning


            if(use_bytes==1):
                assert(loops<256)

                
                input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
                counter_register=self.tile_label(self.x,self.y,"loop_counter")  

                self.code.append(" BTFSS "+input_name)
                self.code.append(" goto "+self.tile_label(self.x,self.y,"no_rest"))
                self.code.append(" MOVLW d'"+str(loops)+"'")
                self.code.append(" MOVWF "+counter_register)
                self.code.append(" goto "+self.tile_label(self.x,self.y,"end_temp"))

                self.code.append(self.tile_label(self.x,self.y,"no_rest"))
                self.code.append([' NOP']*3)
                self.code.append(self.tile_label(self.x,self.y,"end_temp"))

                self.code.append(" CLRF W")
                self.code.append(" XORLW "+counter_register+",W")
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

                self.cycles=len(self.outputs)+14
            elif(use_bytes==2):
                assert(loops<256**2)

                input_name=self.bit_reg[self.tile_label(self.x,self.y,"con")]
                counter_register_hi=self.tile_label(self.x,self.y,"loop_counter_hi")
                counter_register_lo=self.tile_label(self.x,self.y,"loop_counter_lo") 

                # BTFSS input_state
                # goto no_rest

                # MOVLW time/total_cycles_lo
                # MOVWF counter_lo

                # MOVLW time/total_cycles_hi
                # MOVWF counter_hi

                # goto end_temp

                # no_rest Delay 5
                # end_temp

                # CLEAR W
                # XORLW counter_lo,W

                # BTFSC STATUS,Z
                # goto skip1

                # CLRF W
                # XORLW counter_hi,W

                # BTFSC STATUS,Z
                # goto skip2

                # CLRF W
                # XORWF counter_lo,W
                # BTFSC STAUTS Z
                # DECF counter_hi,F
                # DECF counter_lo,F

                # BSF output
                # BSF outputs...
                # goto end
                # skip1 Delay 4
                # skip2 Delay 6+n

                # end BCF input_state

                self.cycles=len(self.outputs)+24
            else:
                print('unexpected error')
                raise

        elif(self.save_file['mode']==2):
            use_bytes=0

        elif(self.save_file['mode']==3):
            use_bytes=0

        return 1

class PulsarNode(Node):

    def get_minimum_cycles(self):
        pass

    def adjust_cycles(self,proposed_total_cycles):
        pass

    def generate_code(self,total_cycles):
        print("not implemented")

class SequencerNode(Node):

    def get_minimum_cycles(self):
        pass

    def adjust_cycles(self,proposed_total_cycles):
        pass

    def get_bitflag_names(self):
        out=[self.tile_label(self.x,self.y,"con")]
        out.extend(map(lambda x:"flag_"+x,self.save_file["steps"]))

        return out

    def generate_code(self,total_cycles):
        print("not implemented")

class Compiler:

    def __init__(self,board,io):

        self.Tile_Node_Links={tiles_mod.Source: SourceNode,
                            tiles_mod.Flag: FlagNode,
                            tiles_mod.Generator: GeneratorNode,
                            tiles_mod.Switch: SwitchNode,
                            tiles_mod.Counter: CounterNode,
                            tiles_mod.Pulsar: TimerNode,
                            tiles_mod.Timer: PulsarNode,
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

    def get_code(self):

        self.bitflag_register_names={}
        bitflag_base_name="bitflag_reg"

        io_data=self.io.save_to_file()
        i=0
        for flag in io_data['outputs']:
            #move to top to prevent blanch bitflags?
            self.bitflag_register_names["flag_"+flag]="PORTB,"+str(i)#overwriting
            i+=1

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
                except KeyError:
                    self.bitflag_register_names[bit]=bitflag_base_name+'_'+str(n)+","+str(i)
                    i+=1

        i=0
        for flag in io_data['inputs']:
            self.bitflag_register_names["flag_"+flag]="PORTA,"+str(i)
            i+=1

        for tile in self.tiles_linear:
            tile.set_bit_flag_names(self.bitflag_register_names)

        
        #move before register to register multi byte timers
        proposed_total_cycles=sum(tile.get_minimum_cycles() for tile in self.tiles_linear)+2 #plus two due to main loop, fix multiout
        total_cycles=sum(tile.adjust_cycles(proposed_total_cycles) for tile in self.tiles_linear)+2 #plus two due to main loop, fix multiout


        for tile in self.tiles_linear:
            tile.generate_code(total_cycles)

        #write code to out
        out=[]
        out.append(';Code generated by LadderiLogical')
        out.append('')

        human_readable_register_names={v: k for k, v in self.bitflag_register_names.items()}

        for io_register in ("PORTA,"+str(i) for i in range(8)):
            try:
                out.append(';'+io_register+': '+human_readable_register_names[io_register])
            except KeyError:
                out.append(';'+io_register+':')
            else:
                del human_readable_register_names[io_register]

        for io_register in ("PORTB,"+str(i) for i in range(8)):
            try:
                out.append(';'+io_register+': '+human_readable_register_names[io_register])
            except KeyError:
                out.append(';'+io_register+':')
            else:
                del human_readable_register_names[io_register]

        human_readable_register_names={v: k for k, v in human_readable_register_names.items()}
        for tiles_bitflags,other_registers in sorted(human_readable_register_names.items()):
            out.append(';'+other_registers+': '+tiles_bitflags)


        out.append('')
        out.append('main')
        for tile in self.tiles_linear:
            out.extend(tile.code)

        #fix outputs on multyple pins remember about time fixing

        out.append(' goto main')#plus 2 to cycles

        out.extend(self.delay_footer())

        out.append(' END')

        print('\n'.join(out))


    def delay_footer(self):
        return ["small_delay_6 nop",
        "small_delay_5 nop",
        "small_delay_4 return",
        "delay3_3 Nop",
        "delay3_2 Nop",
        "delay3_1 Decfsz W,W",
        " goto delay3_1",
        " return"]

