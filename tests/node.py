
class node:

	def __init__(self):
		self.outputs=[]

	def set(self):
		for out in self.outputs:
			out.set()

	def clear(self):
		for out in self.outputs:
			out.clear()


class switch:

	def __init__(self):
		self.outputs=[]
		self.state=False
		self.input=False

	def set(self):
		self.input=True
		if(self.state):
			for out in self.outputs:
				out.set()

	def clear(self):
		self.input=False
		for out in self.outputs:
			out.clear()

	def open(self):
		self.state=False
		for out in self.outputs:
			out.clear()

	def close(self):
		self.input=True
		if(self.input):
			for out in self.outputs:
				out.set()

class light:

	def __init__(self):
		self.outputs=[]

	def set(self):
		print('light set')
		for out in self.outputs:
			out.set()

	def clear(self):
		print('light cleared')
		for out in self.outputs:
			out.clear()




if __name__ == '__main__':
	a=node()
	s=switch()
	b=node()
	l=light()


	a.outputs.append(s)
	s.outputs.append(b)
	b.outputs.append(l)


	a.set()

	s.close()

	print('switch close')

	s.open()