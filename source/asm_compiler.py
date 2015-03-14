
from tiles import Tile, Relay, Source, Flag, Generator, Switch, Counter,Pulsar,Timer,Sequencer

class Compiler:

	def __init__(self,tiles):

		self.tiles_linearlised

		for x,col in enumerate(tiles):
			for y,tile in enumerate(col):

				if(tile!=Tile and tile!=Relay):

					single={}

        # tile_decode={"relay":Relay,"source":Source,"flag":Flag,"generator":Generator,
        # "switch":Switch,"counter":Counter,"pulsar":Pulsar,"timer":Timer,"sequ":Sequencer}
        			single['type']=tile
					single['coords']=[x,y]
					single['outputs']=[]
					single['options']=[]


					for ind, check, direction in zip(self.adj_ind,self.conector_checks,[2,3,0,1]):
						if (ind!=None and check.get()==1):

							if (type(self.board.tiles[ind[0]][ind[1]])==Relay
								and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==1):

								single['outputs'].append(self.board.tiles[ind[0]][ind[1]].state_index)

							elif(type(self.board.tiles[ind[0]][ind[1]])==Flag
								and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0):

								single['outputs'].append([ind[0],ind[1]])


							elif(type(self.board.tiles[ind[0]][ind[1]])==Switch
								and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()==2):

								single['outputs'].append([ind[0],ind[1]])


							elif(type(self.board.tiles[ind[0]][ind[1]])==Counter
								and direction==3):

								single['outputs'].append([ind[0],ind[1]])

							elif(type(self.board.tiles[ind[0]][ind[1]])==Counter
								and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0
								and direction==2):

								single['outputs'].append([ind[0],ind[1]],"Reset_Code")


							elif(type(self.board.tiles[ind[0]][ind[1]])==Timer
								and direction==3):

								single['outputs'].append([ind[0],ind[1]],self.board.tiles[ind[0]][ind[1]].timer_mode.get())

							elif(type(self.board.tiles[ind[0]][ind[1]])==Timer
								and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0
								and direction==2):

								single['outputs'].append([ind[0],ind[1]],"Reset_Code")



							elif(type(self.board.tiles[ind[0]][ind[1]])==Pulsar
								and direction==3):

								single['outputs'].append([ind[0],ind[1]])


							elif(type(self.board.tiles[ind[0]][ind[1]])==Sequencer
								and self.board.tiles[ind[0]][ind[1]].conector_checks[direction].get()!=0):

								single['outputs'].append([ind[0],ind[1]])
	
					self.tiles_linearlised.append(single)





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