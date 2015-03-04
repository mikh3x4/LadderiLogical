#!/usr/local/bin/python3
import tkinter as tk
import sys,os

class App:
	def __init__(self):
		self.root = tk.Tk()
		tk.Label(master=self.root,text="content").pack()
		tk.Button(master=self.root,text="new_window",command=self.open).pack()

	def open(self):
		os.system(sys.argv[0]+"&")

if __name__ == '__main__':
	a=App()
	a.root.mainloop()