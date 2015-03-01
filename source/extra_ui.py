import tkinter as tk

class IOBoard(tk.Frame):


    def __init__(self,root,app):
        tk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.output_list=[]

        for x in range(8):
            a=tk.Entry(master=self,width=10)
            a.grid(column=0,row=x)
            b=tk.Label(master=self,text='0')
            b.grid(column=1,row=x)
            self.output_list.append([a,b])


    def update(self):

        for x in self.output_list:
            try:
                x[1].config(text=str(self.app.board.flags[x[0].get()][1]))
            except KeyError:
                # print(x[0].get()+" flag non existant")
                pass

class ToolBox(tk.Frame):


    def __init__(self,root,app):
        tk.Frame.__init__(self, root)
        self.root=root
        self.app=app

        self.tool="select"

        self.select=tk.Button(master=self,text="Select",command=lambda:self.change_tool("select"))
        self.horizontal=tk.Button(master=self,text="Horizontal",command=lambda:self.change_tool("horizontal"))
        self.hswitch=tk.Button(master=self,text="HSwitch",command=lambda:self.change_tool("hswitch"))

        self.select.grid(row=0,column=0)
        self.horizontal.grid(row=0,column=1)
        self.hswitch.grid(row=0,column=2)


    def change_tool(self,name):
        print("changed to "+name)
        self.tool=name

