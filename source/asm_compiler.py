


class Compiler:

	def __init__(self):
		pass



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